# AskAfrica Backend

FastAPI backend for the AskAfrica AI Q&A application.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy the environment template:
```bash
cp .env.template .env
```

4. Edit `.env` file to set your Ollama model name (optional, defaults to "llama3")

## Running the Backend

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

- `GET /` - Health check
- `GET /health` - API status and model info
- `POST /ask` - Send a question to the LLM

## Prerequisites

Make sure Ollama is running with your desired model:
```bash
ollama serve
ollama pull llama3  # or your preferred model
``` 