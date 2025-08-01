# AskAfrica - Local AI Q&A Application
<img width="1056" height="904" alt="image" src="https://github.com/user-attachments/assets/686fff1f-14c3-4524-a62c-4dea11493a64" />

<img width="900" height="845" alt="image" src="https://github.com/user-attachments/assets/e165104e-eddc-4d32-bcc8-33ee3bbf3d90" />

A full-stack AI Q&A application powered by local LLM via Ollama. AskAfrica provides a simple, beautiful interface for interacting with your local AI model.

## 🚀 Features

- **Local AI Processing**: Uses Ollama for offline AI capabilities
- **Modern UI**: Beautiful, responsive interface built with Next.js and TailwindCSS
- **Real-time Q&A**: Instant responses from your local LLM
- **Recent Questions**: Automatically saves and displays recent conversations
- **Error Handling**: Robust error handling and loading states
- **Swagger Documentation**: Complete API documentation

## 🏗️ Tech Stack

- **Frontend**: Next.js 15 + TypeScript + TailwindCSS
- **Backend**: FastAPI (Python) + Pydantic + httpx
- **LLM**: Local model via Ollama
- **Storage**: localStorage for recent questions

## 📋 Prerequisites

1. **Ollama**: Install and set up Ollama
   ```bash
   # Install Ollama (follow instructions at https://ollama.ai)
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Start Ollama service
   ollama serve
   
   # Pull a model (e.g., llama3)
   ollama pull llama3
   ```

2. **Python**: Python 3.8+ for the backend
3. **Node.js**: Node.js 18+ for the frontend

## 🛠️ Installation & Setup

### 1. Clone and Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.template .env

# Edit .env file to set your Ollama model (optional, defaults to "llama3")
```

### 2. Setup Frontend

```bash
cd frontend

# Install dependencies
npm install
```

## 🚀 Running the Application

### 1. Start Ollama (if not already running)

```bash
ollama serve
```

### 2. Start the Backend

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at:
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 3. Start the Frontend

```bash
cd frontend
npm run dev
```

The frontend will be available at:
- http://localhost:3000

## 📖 Usage

1. Open http://localhost:3000 in your browser
2. Type your question in the text area
3. Click "Ask AI" or press Enter
4. View the AI response
5. Your recent questions will be saved automatically

## 🔧 Configuration

### Backend Configuration

Edit `backend/.env` file:
```env
OLLAMA_MODEL=llama3  # Change to your preferred model
```

### Available Models

You can use any model available in Ollama:
- `llama3` (default)
- `llama2`
- `codellama`
- `mistral`
- `gemma`
- And many more...

To see available models:
```bash
ollama list
```

## 📚 API Endpoints

- `GET /` - Health check
- `GET /health` - API status and model info
- `POST /ask` - Send a question to the LLM

### Example API Usage

```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is artificial intelligence?"}'
```

## 🎨 Features

### Frontend Features
- **Responsive Design**: Works on desktop and mobile
- **Loading States**: Visual feedback during AI processing
- **Error Handling**: Clear error messages
- **Recent Questions**: Automatic storage of conversation history
- **Modern UI**: Beautiful gradient design with smooth animations

### Backend Features
- **FastAPI**: High-performance async API
- **Swagger Documentation**: Interactive API docs
- **CORS Support**: Configured for frontend integration
- **Error Handling**: Comprehensive error responses
- **Environment Configuration**: Flexible model selection

## 🔍 Troubleshooting

### Common Issues

1. **Ollama Connection Error**
   - Make sure Ollama is running: `ollama serve`
   - Check if the model is installed: `ollama list`

2. **Backend Connection Error**
   - Ensure the backend is running on port 8000
   - Check CORS configuration if needed

3. **Model Not Found**
   - Pull the model: `ollama pull <model-name>`
   - Update the `.env` file with the correct model name

### Debugging

- Backend logs: Check the terminal running uvicorn
- Frontend logs: Check browser developer console
- Ollama logs: Check `ollama logs` command

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai) for local LLM capabilities
- [Next.js](https://nextjs.org) for the frontend framework
- [FastAPI](https://fastapi.tiangolo.com) for the backend framework
- [TailwindCSS](https://tailwindcss.com) for styling 
