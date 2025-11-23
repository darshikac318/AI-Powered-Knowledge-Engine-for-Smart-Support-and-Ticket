import pytest

def test_db_connection_mock():
    # placeholder: in real project, you'd mock your DB connector here
    class FakeDB:
        def __init__(self):
            self.connected = True

        def fetch_docs(self):
            return [{"id": "d1", "text": "hello"}]
    db = FakeDB()
    docs = db.fetch_docs()
    assert isinstance(docs, list)
    assert docs[0]["id"] == "d1"
