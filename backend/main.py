from fastapi import FastAPI

# Comando pra rodar: uvicorn backend.main:app --reload 
# url: http://127.0.0.1:8000
app = FastAPI()

@app.get("/")
def home():
    return {"mensagem": "Olá mundo"}