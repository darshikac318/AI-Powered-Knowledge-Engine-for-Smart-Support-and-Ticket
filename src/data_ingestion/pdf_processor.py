import os
import PyPDF2
import pdfplumber
import fitz
from typing import List, Dict
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer, util
import torch

class PDFProcessor:
    def __init__(self):
        self.raw_data_path = os.path.join("data", "raw")
        
        print("Loading semantic models...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        self.semantic_splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
            tokenizer=self.embedding_model.tokenizer,
            chunk_size=512,
            chunk_overlap=0,
            separators=["\n\n", "\n", ". ", " ", ""],
            keep_separator=True
        )
        
        print("Semantic models loaded")
    
    def extract_with_pypdf2(self, pdf_path: str) -> str:
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except:
            pass
        return text
    
    def extract_with_pdfplumber(self, pdf_path: str) -> str:
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                    
                    tables = page.extract_tables()
                    if tables:
                        for table in tables:
                            for row in table:
                                if row:
                                    text += " ".join([str(cell) if cell else "" for cell in row]) + "\n"
        except:
            pass
        return text
    
    def extract_with_pymupdf(self, pdf_path: str) -> str:
        text = ""
        try:
            doc = fitz.open(pdf_path)
            for page in doc:
                text += page.get_text()
            doc.close()
        except:
            pass
        return text
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        methods = [
            ("PDFPlumber", self.extract_with_pdfplumber),
            ("PyMuPDF", self.extract_with_pymupdf),
            ("PyPDF2", self.extract_with_pypdf2)
        ]
        
        best_text = ""
        best_method = ""
        
        for method_name, method_func in methods:
            text = method_func(pdf_path)
            if len(text.strip()) > len(best_text.strip()):
                best_text = text
                best_method = method_name
        
        return best_text, best_method
    
    def semantic_chunk_with_coherence(self, text: str) -> List[str]:
        initial_chunks = self.semantic_splitter.split_text(text)
        
        if len(initial_chunks) <= 1:
            return initial_chunks
        
        embeddings = self.embedding_model.encode(initial_chunks, convert_to_tensor=True)
        
        final_chunks = []
        current_group = [initial_chunks[0]]
        current_embedding = embeddings[0]
        
        for i in range(1, len(initial_chunks)):
            similarity = util.cos_sim(current_embedding, embeddings[i]).item()
            
            if similarity > 0.7:
                current_group.append(initial_chunks[i])
                current_embedding = torch.mean(torch.stack([current_embedding, embeddings[i]]), dim=0)
            else:
                if current_group:
                    final_chunks.append(" ".join(current_group))
                current_group = [initial_chunks[i]]
                current_embedding = embeddings[i]
        
        if current_group:
            final_chunks.append(" ".join(current_group))
        
        return [chunk for chunk in final_chunks if len(chunk.strip()) > 100]
    
    def process_all_pdfs(self) -> List[Dict]:
        if not os.path.exists(self.raw_data_path):
            raise Exception(f"Directory not found: {self.raw_data_path}")
        
        pdf_files = [f for f in os.listdir(self.raw_data_path) if f.lower().endswith('.pdf')]
        
        if not pdf_files:
            raise Exception(f"No PDF files found in {self.raw_data_path}")
        
        print(f"\nFound {len(pdf_files)} PDF files")
        print("="*70)
        
        all_documents = []
        successful = 0
        failed = 0
        
        for pdf_file in pdf_files:
            pdf_path = os.path.join(self.raw_data_path, pdf_file)
            
            print(f"\nProcessing: {pdf_file}")
            
            raw_text, method = self.extract_text_from_pdf(pdf_path)
            
            if not raw_text or len(raw_text.strip()) < 100:
                print(f"  Status: FAILED - Insufficient text")
                failed += 1
                continue
            
            print(f"  Extraction method: {method}")
            print(f"  Performing automatic semantic chunking...")
            
            chunks = self.semantic_chunk_with_coherence(raw_text)
            
            if not chunks:
                print(f"  Status: FAILED - No valid chunks")
                failed += 1
                continue
            
            print(f"  Characters extracted: {len(raw_text)}")
            print(f"  Semantic chunks created: {len(chunks)}")
            print(f"  Avg chunk size: {sum(len(c) for c in chunks) // len(chunks)} chars")
            print(f"  Status: SUCCESS")
            
            file_id = pdf_file.lower().replace('.pdf', '').replace(' ', '_').replace('-', '_')
            
            for idx, chunk in enumerate(chunks):
                all_documents.append({
                    'id': f"{file_id}_chunk_{idx}",
                    'content': chunk,
                    'source': pdf_file,
                    'metadata': {
                        'source_file': pdf_file,
                        'chunk_index': idx,
                        'total_chunks': len(chunks),
                        'extraction_method': method,
                        'chunk_method': 'semantic_ai'
                    }
                })
            
            successful += 1
        
        print("\n" + "="*70)
        print(f"Processing Summary:")
        print(f"  Total PDFs: {len(pdf_files)}")
        print(f"  Successful: {successful}")
        print(f"  Failed: {failed}")
        print(f"  Total semantic chunks: {len(all_documents)}")
        print("="*70)
        
        if not all_documents:
            raise Exception("No documents were successfully processed")
        
        return all_documents