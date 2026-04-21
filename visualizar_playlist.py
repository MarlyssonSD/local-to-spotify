from datetime import datetime

from pyautogui import sleep
from dotenv import load_dotenv
import autentica_spotify as conect
import utils
import json

load_dotenv()

SCOPE = "playlist-read-private playlist-read-collaborative"
sp = conect.autentica_spotify()
def listar_musicas_da_playlist(playlist_id):
    musicas = []

    # pega info da playlist (nome, dono etc)
    playlist_info = sp.playlist(playlist_id)

    resultados = sp.playlist_items(
        playlist_id,
        fields="items.track.name,items.track.artists.name,next",
        additional_types=["track"]
    )

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

    metadata = {
        "playlist_id": playlist_id,
        "playlist_nome": playlist_info["name"],
        "total_musicas": len(musicas)
    }

    return musicas, metadata

def salvar_em_txt(musicas, metadata, nome_arquivo):
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        metadata["exportado_em"] = datetime.now().isoformat()
        
        # Cabeçalho
        f.write(f"Playlist: {metadata['playlist_nome']}\n")
        f.write(f"ID: {metadata['playlist_id']}\n")
        f.write(f"Gerado em: {metadata['exportado_em']}\n")
        f.write(f"Total de músicas: {metadata['total_musicas']}\n")
        f.write("-" * 40 + "\n")

        # Lista (teu código original)
        for i, (nome, artista) in enumerate(musicas, 1):
            f.write(f"{i}. {nome} — {artista}\n")

    print(f"✅ Arquivo .txt salvo em: {nome_arquivo}")

def salvar_em_json(musicas, metadata, nome_arquivo):
    lista_dict = [
        {"id": i + 1, "title": nome, "artist": artista}
        for i, (nome, artista) in enumerate(musicas)
    ]
    
    metadata["exportado_em"] = datetime.now().isoformat()
    estrutura_final = {
        "metadata": metadata,
        "musicas": lista_dict
    }

    with open(nome_arquivo, "w", encoding="utf-8") as f:
        json.dump(estrutura_final, f, indent=2, ensure_ascii=False)

    print(f"✅ Arquivo .json salvo em: {nome_arquivo}")

def exibir_musicas(nome_playlist, musicas):
    print(f"\nMúsicas da playlist {nome_playlist} \n🎵 Total de músicas: {len(musicas)}\n")
    sleep(2)

    for i, (nome, artista) in enumerate(musicas, 1):
        print(f"{i:02d}. {nome} — {artista}")

def exporta_musicas_playlist():
    print("🔍 Analisando músicas da playlist...")
    playlist_id = "2b8DSYBpxpmOssYkNOIzC9"  # troque pela sua
    nome_playlist = utils.obter_nome_playlist_id(sp, playlist_id)
    musicas, metadata = listar_musicas_da_playlist(playlist_id)
    print(f"✅ Análise concluída para a playlist: {nome_playlist} ({len(musicas)} músicas)")
    while True:
        print("\nEscolha uma opção:")
        print("1 - Salvar como TXT")
        print("2 - Salvar como JSON")
        print("3 - Apenas exibir no terminal")
        print("4 - Sair")

        escolha = input("Digite o número da opção: ")

        if escolha == "1":
            salvar_em_txt(musicas, metadata, f"database/musicas_da_playlist_{nome_playlist}.txt")
        elif escolha == "2":
            salvar_em_json(musicas, metadata, f"database/musicas_da_playlist_{nome_playlist}.json")
        elif escolha == "3":
            exibir_musicas(nome_playlist,musicas)
        elif escolha == "4":
            print("✅ Saindo...")
            return
        else:
            print("❌ Opção inválida.")

# exporta_musicas_playlist()