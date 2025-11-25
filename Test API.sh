curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain AI automation", "max_new_tokens": 200}'