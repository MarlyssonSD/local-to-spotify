from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

# Autenticação com escopos de leitura de playlist
SCOPE = "playlist-read-private playlist-read-collaborative"
sp = Spotify(auth_manager=SpotifyOAuth(scope=SCOPE, cache_path=".cache"))

def listar_musicas_da_playlist(playlist_id):
    musicas = []
    resultados = sp.playlist_items(playlist_id, fields="items.track.name,items.track.artists.name,next", additional_types=["track"])

    while resultados:
        for item in resultados["items"]:
            track = item["track"]
            if track:
                nome = track["name"]
                artista = track["artists"][0]["name"]
                musicas.append((nome, artista))
        if resultados.get("next"):
            resultados = sp.next(resultados)
        else:
            break
    return musicas

def exibir_musicas(musicas):
    print(f"🎵 Total de músicas: {len(musicas)}\n")
    for i, (nome, artista) in enumerate(musicas, 1):
        print(f"{i:02d}. {nome} — {artista}")

def main():
    # Substitua pelo ID da sua playlist (ex: da URL do Spotify)
    playlist_id = "0dlooFr2cdwtQ7ODoglBXR"
    musicas = listar_musicas_da_playlist(playlist_id)
    exibir_musicas(musicas)

if __name__ == "__main__":
    main()