
```shell
python3 -m venv venv
```

```shell
source venv/bin/activate
```

```shell
pip install fastapi uvicorn
```

Для тестирования API:

```shell
pip install requests
```

```shell
python -m app
```

```shell
uvicorn app:app --reload --port 8899
```

Open: http://127.0.0.1:8899/endpoint

Swagger: http://localhost:8899/docs