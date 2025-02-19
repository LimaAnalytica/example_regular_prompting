# example_regular_prompting
This is an example of regular prompting, which is the most basic form of interacting with a language model, where you simply ask  a question or give a direct instruction. For example, "What is the capital of France?" "Write a poem about the sea".

# Prompt Project

This project presents the implementation of simple web interface to interact with a Hugging Face models via prompts.

## Requirements
- Docker
- Docker Compose

## Configuration
1. Create a `.env` file in the root of the project:
```
HUGGINGFACE_TOKEN=your_secret_token_here
```

## Execution
1. Build and start the containers:
```bash
docker-compose up --build
```

2. To enter the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## Structure
- `backend/`: API FastAPI to interact with Hugging Face
- `frontend/`: A React web interface.