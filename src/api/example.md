1. start api: ```uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 8008```

1. get prediction: ```commandline curl --header "Content-Type: application/json" --request POST --data '{"input": [0, 0, 0, 1, 125, 1]}' http://localhost:8008/predict```

1. train model: ```curl --header "Content-Type: application/json" --request POST http://localhost:8008/train```