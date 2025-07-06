from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

SCOPE = "playlist-read-private playlist-modify-private playlist-read-collaborative playlist-modify-public"
sp = Spotify(auth_manager=SpotifyOAuth(scope=SCOPE, cache_path=".cache"))
user_id = sp.current_user()["id"]

def buscar_musicas_por_artista(playlist_id, artista_alvo):
    musicas = []
    resultados = sp.playlist_items(playlist_id, fields="items.track.name,items.track.id,items.track.artists.name,next", additional_types=["track"])

    while resultados:
        for item in resultados["items"]:
            track = item["track"]
            if not track:
                continue

            nome = track["name"]
            artistas = [a["name"] for a in track["artists"]]
            if any(artista_alvo.lower() in a.lower() for a in artistas):
                musicas.append(track["id"])

        if resultados.get("next"):
            resultados = sp.next(resultados)
        else:
            break

    return musicas

def criar_playlist_com_musicas(playlist_name, track_ids):
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
    sp.playlist_add_items(playlist["id"], track_ids)
    print(f"✅ Playlist '{playlist_name}' criada com {len(track_ids)} faixas.")

def main():
    playlist_origem_id = "0dlooFr2cdwtQ7ODoglBXR"  # Substitua pelo ID da playlist origem
    artista_desejado = "Krawk"  # Substitua pelo nome do artista desejado

    faixas = buscar_musicas_por_artista(playlist_origem_id, artista_desejado)
    if not faixas:
        print(f"❌ Nenhuma música encontrada com o artista '{artista_desejado}'.")
    else:
        criar_playlist_com_musicas(artista_desejado, faixas)

if __name__ == "__main__":
    main()