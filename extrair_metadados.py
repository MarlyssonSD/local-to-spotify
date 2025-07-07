import os
import json
from mutagen import File

PASTA_MUSICAS = r"E:\Geral\Músicas"
SAIDA_ARQUIVO = "database/musicas.json"
FORMATOS_SUPORTADOS = (".mp3", ".m4a")

def extrair_metadados(pasta):
    musicas = []
    arquivos = [f for f in os.listdir(pasta) if f.lower().endswith(FORMATOS_SUPORTADOS)]

    for arquivo in arquivos:
        caminho = os.path.join(pasta, arquivo)
        title = None
        artist = None

        try:
            audio = File(caminho, easy=True)
            if audio is not None:
                title = audio.get("title", [None])[0]
                artist = audio.get("artist", [None])[0]
        except Exception as e:
            print(f"Erro ao ler {arquivo}: {e}")

        # Fallback
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
