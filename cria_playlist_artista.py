from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

SCOPE = "playlist-read-private playlist-modify-private playlist-read-collaborative playlist-modify-public"
sp = Spotify(auth_manager=SpotifyOAuth(scope=SCOPE, cache_path=".cache"), requests_timeout=15)
user_id = sp.current_user()["id"]

def buscar_musicas_por_nome_ou_artista(playlist_id, termo):
    musicas = []
    resultados = sp.playlist_items(playlist_id, fields="items.track.name,items.track.id,items.track.artists.name,next", additional_types=["track"])

    while resultados:
        for item in resultados["items"]:
            track = item["track"]
            if not track:
                continue

            nome = track["name"]
            artistas = [a["name"] for a in track["artists"]]
            # Verifica se o termo aparece no nome da música ou de algum artista
            # print(f"Verificando: {nome} - {', '.join(artistas)}")
            
            if termo.lower() in nome.lower() or any(termo.lower() in a.lower() for a in artistas):
                print(f"Verificando: {nome} - {', '.join(artistas)}")

                musicas.append(track["id"])

        if resultados.get("next"):
            resultados = sp.next(resultados)
        else:
            break
    print(f"Total de músicas encontradas: {len(musicas)}")
    return musicas


def criar_playlist_com_musicas(playlist_name, track_ids):
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
    sp.playlist_add_items(playlist["id"], track_ids)
    print(f"✅ Playlist '{playlist_name}' criada com {len(track_ids)} faixas.")

def main():
    playlist_origem_id = "0dlooFr2cdwtQ7ODoglBXR"  # Substitua pelo ID da playlist origem
    artista_desejado = "Virgingod"  # Substitua pelo nome do artista desejado

    faixas = buscar_musicas_por_nome_ou_artista(playlist_origem_id, artista_desejado)
    if not faixas:
        print(f"❌ Nenhuma música encontrada com o artista '{artista_desejado}'.")
    else:
        criar_playlist_com_musicas(artista_desejado, faixas)

if __name__ == "__main__":
    main()