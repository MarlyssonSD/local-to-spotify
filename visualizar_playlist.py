from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import json

load_dotenv()

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

def salvar_em_txt(musicas, nome_arquivo):
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        for i, (nome, artista) in enumerate(musicas, 1):
            f.write(f"{i}. {nome} — {artista}\n")
    print(f"✅ Arquivo .txt salvo em: {nome_arquivo}")

def salvar_em_json(musicas, nome_arquivo):
    lista_dict = [{"id": i + 1, "title": nome, "artist": artista} for i, (nome, artista) in enumerate(musicas)]
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        json.dump(lista_dict, f, indent=2, ensure_ascii=False)
    print(f"✅ Arquivo .json salvo em: {nome_arquivo}")

def exibir_musicas(musicas):
    print(f"\n🎵 Total de músicas: {len(musicas)}\n")
    for i, (nome, artista) in enumerate(musicas, 1):
        print(f"{i:02d}. {nome} — {artista}")

def main():
    print("🔍 Analisando músicas da playlist...")
    playlist_id = "0dlooFr2cdwtQ7ODoglBXR"  # troque pela sua
    musicas = listar_musicas_da_playlist(playlist_id)

    print("\nEscolha uma opção:")
    print("1 - Salvar como TXT")
    print("2 - Salvar como JSON")
    print("3 - Apenas exibir no terminal")

    escolha = input("Digite o número da opção: ")

    if escolha == "1":
        salvar_em_txt(musicas, "database/musicas_da_playlist.txt")
    elif escolha == "2":
        salvar_em_json(musicas, "database/musicas_da_playlist.json")
    elif escolha == "3":
        exibir_musicas(musicas)
    else:
        print("❌ Opção inválida.")

if __name__ == "__main__":
    main()
