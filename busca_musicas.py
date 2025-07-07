import os
import difflib
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

# Configurações
SCOPE = "user-read-private"

def buscar_musica(titulo, artista=""):
    sp = Spotify(auth_manager=SpotifyOAuth(scope=SCOPE, cache_path=".cache"))

    query = f"{titulo} {artista}".strip()
    print(f"🔎 Buscando: {query}")

    resultado = sp.search(q=query, type="track", limit=5)
    items = resultado.get("tracks", {}).get("items", [])

    if not items:
        print("❌ Nenhum resultado encontrado.")
        return

    print("✅ Resultados ranqueados por similaridade:")
    resultados_com_score = []
    for item in items:
        nome = item["name"]
        artistas = ", ".join(a["name"] for a in item["artists"])
        score = difflib.SequenceMatcher(None, titulo.lower(), nome.lower()).ratio()
        resultados_com_score.append({
            "nome": nome,
            "artistas": artistas,
            "id": item["id"],
            "score": round(score, 2)
        })

    # Ordena pelo score (maior primeiro)
    resultados_com_score.sort(key=lambda x: x["score"], reverse=True)

    # Exibe
    for i, r in enumerate(resultados_com_score, 1):
        print(f"{i}. {r['nome']} - {r['artistas']} (Score: {r['score']}) - ID: {r['id']}")

if __name__ == "__main__":
    # Exemplo: altere aqui pra testar outras músicas
    titulo = "te ver"
    artista = "virgingod"

    buscar_musica(titulo, artista)
