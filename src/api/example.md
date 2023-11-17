```uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 8008```

```commandline curl --header "Content-Type: application/json" --request POST --data '{"input": [0, 0, 0, 1, 125, 1]}' http://localhost:8008/predict```