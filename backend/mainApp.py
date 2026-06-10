from fastapi import FastAPI
from backend.services.buscar_musicas import buscar_musica
import backend.core.autenticar_spotify as connect

    
# Comando pra rodar: uvicorn backend.mainApp:app --reload 
# url: http://127.0.0.1:8000
app = FastAPI()

@app.get("/")
def home():
    return {"mensagem": "Olá mundo"}

@app.get("/buscar-musica")
def buscar(titulo: str, artista: str = ""):

    sp = connect.autentica_spotify()
    resultados = buscar_musica(sp, titulo, artista)
    return {"resultados": resultados}

# Listar playlists do usuário
@app.get("/listar-playlists")
def listar_playlists_user():
    sp = connect.autentica_spotify()
    playlists = listar_playlists(sp)
    return {"playlists": playlists}
