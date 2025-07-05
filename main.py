import json
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()

# Configurações
ARQUIVO_MUSICAS = "musicas.json"
NOME_PLAYLIST = "Tudo"

# Escopo para criar playlists privadas
SCOPE = "playlist-modify-private"

def ler_musicas(arquivo):
    with open(arquivo, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    sp = Spotify(auth_manager=SpotifyOAuth(scope=SCOPE, cache_path=".cache"))

    user_id = sp.current_user()["id"]
    print(f"Usuário autenticado: {user_id}")

    # Cria a playlist (privada)
    playlist = sp.user_playlist_create(user=user_id, name=NOME_PLAYLIST, public=False, description="Playlist migrada de músicas locais.")
    playlist_id = playlist["id"]
    print(f"Playlist criada: {NOME_PLAYLIST} (ID: {playlist_id})")

    musicas = ler_musicas(ARQUIVO_MUSICAS)
    track_ids = []

    nao_encontradas = []

    for m in musicas:
        query = f"{m['title']} {m['artist']}".strip()
        print(f"Buscando: {query}")
        resultado = sp.search(q=query, type="track", limit=1)
        items = resultado.get("tracks", {}).get("items", [])
        
        if items:
            track = items[0]
            track_id = track["id"]
            nome = track["name"]
            artista = track["artists"][0]["name"]
            print(f"  ✅ Encontrado: {nome} - {artista}")
            track_ids.append(track_id)
        else:
            print(f"  ❌ Não encontrado: {query}")
            nao_encontradas.append(m)

    # Salva as não encontradas em JSON
    if nao_encontradas:
        with open("nao_encontradas.json", "w", encoding="utf-8") as f:
            json.dump(nao_encontradas, f, indent=2, ensure_ascii=False)
        print(f"\n⚠️ {len(nao_encontradas)} músicas não foram encontradas e foram salvas em 'nao_encontradas.json'")


    # Adiciona as faixas na playlist (em blocos de 100, limite da API)
    for i in range(0, len(track_ids), 100):
        sp.playlist_add_items(playlist_id, track_ids[i:i+100])

    print(f"\n✔️ Total de músicas adicionadas: {len(track_ids)}")

if __name__ == "__main__":
    main()
