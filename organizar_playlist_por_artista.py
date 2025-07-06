from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from collections import defaultdict
import os

load_dotenv()

# Escopo para leitura e criação de playlists
SCOPE = "playlist-read-private playlist-modify-private playlist-modify-public"

sp = Spotify(auth_manager=SpotifyOAuth(scope=SCOPE, cache_path=".cache"))
user_id = sp.current_user()["id"]

# ID da playlist que você quer organizar (pega da URL do Spotify)
PLAYLIST_ORIGINAL_ID = "0dlooFr2cdwtQ7ODoglBXR"

# 1. Buscar músicas da playlist
def buscar_musicas(playlist_id):
    musicas = []
    resultados = sp.playlist_items(playlist_id, fields="items.track.id,items.track.name,items.track.artists(name,id),next", additional_types=["track"])

    while resultados:
        for item in resultados["items"]:
            track = item["track"]
            if track:
                musicas.append({
                    "id": track["id"],
                    "nome": track["name"],
                    "artista_nome": track["artists"][0]["name"],
                    "artista_id": track["artists"][0]["id"]
                })
        if resultados["next"]:
            resultados = sp.next(resultados)
        else:
            break

    return musicas

# 2. Criar playlists por artista
def criar_playlists_por_artista(musicas):
    por_artista = defaultdict(list)
    for m in musicas:
        por_artista[m["artista_nome"]].append(m["id"])

    for artista, faixas in por_artista.items():
        nome_playlist = f"{artista} - AutoPlaylist"
        nova = sp.user_playlist_create(user=user_id, name=nome_playlist, public=False)
        sp.playlist_add_items(nova["id"], faixas)
        print(f"✅ Criada: {nome_playlist} ({len(faixas)} faixas)")

if __name__ == "__main__":
    musicas = buscar_musicas(PLAYLIST_ORIGINAL_ID)
    print(f"Total de músicas lidas: {len(musicas)}")
    criar_playlists_por_artista(musicas)
