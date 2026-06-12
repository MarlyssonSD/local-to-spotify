from fastapi import FastAPI
import backend.service.playlist_service as sv
import backend.core.autenticar_spotify as connect

    
# Comando pra rodar: uvicorn backend.mainApp:app --reload 
# url: http://127.0.0.1:8000
app = FastAPI()

@app.get("/")
def home():
    return {"mensagem": "Olá mundo"}

@app.get("/buscar-musica")
def get_buscar_musica(titulo: str, artista: str = ""):

    sp = connect.autentica_spotify()
    resultados = sv.buscar_musica(sp, titulo, artista)
    return {"resultados": resultados}

# Listar playlists do usuário
@app.get("/listar-playlists")
def get_playlists_usuario():
    sp = connect.autentica_spotify()
    playlists = sv.listar_playlists(sp)
    return {"playlists": playlists}
