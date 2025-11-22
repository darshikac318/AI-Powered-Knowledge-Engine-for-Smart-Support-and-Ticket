# Recommendation Project (Auto-generated)

## Structure
- `src/recommendations` - core code
- `tests` - pytest test suite
- `performance` - locust load test

## Run tests
```bash
pip install -r requirements.txt
pytest -q
```

## Run locust
```bash
locust -f performance/locustfile.py --host=http://localhost:8000
```
