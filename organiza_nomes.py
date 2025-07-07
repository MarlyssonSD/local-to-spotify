import json
import re
import os

# Carrega o JSON original
with open("database/musicas.json", "r", encoding="utf-8") as f:
    musicas = json.load(f)

def remover_emoji(texto):
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "\U00002700-\U000027BF"
        "\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub(r"", texto)

def limpar_titulo(titulo):
    titulo = remover_emoji(titulo)

    # Remove conteúdo entre parênteses ou colchetes
    titulo = re.sub(r"\(.*?\)", "", titulo)
    titulo = re.sub(r"\[.*?\]", "", titulo)

    # Remove qualquer abertura de parêntese ou colchete não fechada
    titulo = re.sub(r"[\(\[\{].*$", "", titulo)

    # Remove "prod.", "feat.", etc.
    titulo = re.sub(r"prod\.?.*?(?=$|[-|,])", "", titulo, flags=re.I)
    titulo = re.split(r"\s(feat|ft|featuring)[\.:]?\s", titulo, flags=re.I)[0]

    # Limpeza geral
    titulo = re.sub(r'["“”‘’\']', '', titulo)
    titulo = re.sub(r"[|_;]", "", titulo)
    titulo = re.sub(r"\s{2,}", " ", titulo)
    titulo = re.sub(r"^\s*\d+[\.\-\s]+", "", titulo)
    titulo = re.sub(r"[-\s]+$", "", titulo)  # Traços ou espaços finais

    return titulo.strip()

def limpar_filename(nome):
    nome = limpar_titulo(nome)
    # Remove espaços antes da extensão .mp3, .wav etc.
    nome = re.sub(r"\s+(\.[^.]+)$", r"\1", nome)
    return nome.strip()

# Aplica a limpeza nos campos
musicas_limpas = [
    {
        "title": limpar_titulo(m["title"]),
        "artist": limpar_titulo(m["artist"]),
        "filename": limpar_filename(m["filename"])
    }
    for m in musicas
]

# Cria a pasta se não existir
os.makedirs("database", exist_ok=True)

# Salva o novo JSON
with open("database/musicas_nomes_organizados.json", "w", encoding="utf-8") as f:
    json.dump(musicas_limpas, f, indent=2, ensure_ascii=False)
