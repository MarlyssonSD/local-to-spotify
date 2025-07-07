import os
import json
from mutagen.easyid3 import EasyID3
from mutagen import File

PASTA_MUSICAS = "E:\Geral\Músicas"
SAIDA_ARQUIVO = "database/musicas.json"

def extrair_metadados(pasta):
    musicas = []
    arquivos = [f for f in os.listdir(pasta) if f.endswith(".mp3")]

    for arquivo in arquivos:
        caminho = os.path.join(pasta, arquivo)
        try:
            # Tenta ler com ID3
            audio = EasyID3(caminho)
            title = audio.get("title", [None])[0]
            artist = audio.get("artist", [None])[0]
        except Exception:
            # Se falhar, tenta outro formato
            audio = File(caminho)
            title = None
            artist = None

        # Fallback: usa o nome do arquivo se não tiver tag
        if not title:
            title = os.path.splitext(arquivo)[0]
        if not artist:
            artist = ""

        musicas.append({
            "title": title,
            "artist": artist,
            "filename": arquivo
        })

    return musicas

def salvar_em_json(musicas, arquivo_saida):
    with open(arquivo_saida, "w", encoding="utf-8") as f:
        json.dump(musicas, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    musicas = extrair_metadados(PASTA_MUSICAS)
    salvar_em_json(musicas, SAIDA_ARQUIVO)
    print(f"✅ {len(musicas)} músicas salvas em '{SAIDA_ARQUIVO}'")
