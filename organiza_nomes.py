import json
import re
import os
import emoji

# Carrega o JSON original
with open("database/musicas.json", "r", encoding="utf-8") as f:
    musicas = json.load(f)


def remover_emoji(texto):
    return emoji.replace_emoji(texto, replace='')

def remover_bom(texto):
    return texto.replace("\ufeff", "")

# def remover_emoji(texto):
#     emoji_pattern = re.compile(
#         "["
#         u"\U0001F600-\U0001F64F"  # Emoticons
#         u"\U0001F300-\U0001F5FF"  # Símbolos e pictogramas
#         u"\U0001F680-\U0001F6FF"  # Transporte e mapas
#         u"\U0001F1E0-\U0001F1FF"  # Bandeiras
#         u"\U00002702-\U000027B0"  # Diversos
#         u"\U000024C2-\U0001F251"
#         u"\U0001F900-\U0001F9FF"  # Emojis adicionais
#         u"\U0001FA70-\U0001FAFF"  # Símbolos e emojis extra
#         u"\U00002600-\U000026FF"  # Símbolos variados (tipo ⏳)
#         "]+",
#         flags=re.UNICODE
#     )
#     return emoji_pattern.sub(r"", texto)


def limpar_titulo(titulo):
    titulo = remover_bom(titulo)
    titulo = remover_emoji(titulo)

    # Remove conteúdo entre parênteses ou colchetes
    titulo = re.sub(r"\(.*?\)", "", titulo)
    titulo = re.sub(r"\[.*?\]", "", titulo)

    # Remove qualquer abertura de parêntese ou colchete não fechada
    titulo = re.sub(r"[\(\[\{\)\]\}].*$", "", titulo)

    # Remove "prod.", "feat.", etc.
    titulo = re.sub(r"prod\.?.*?(?=$|[-|,])", "", titulo, flags=re.I)
    titulo = re.sub(r"\b(feat\.?|ft\.?|featuring)\b\.?", "", titulo, flags=re.I)


    # Limpeza geral
    titulo = re.sub(r'["“”‘’\']', '', titulo)
    titulo = re.sub(r"[|_;*+｡･:]", "", titulo)
    titulo = re.sub(r"^\s*\d+[\.\-\s]+", "", titulo)
    titulo = re.sub(r"[-\s]+$", "", titulo)  # Traços ou espaços finais
    titulo = titulo.replace("-", "")  # Remove traços restantes após outras limpezas
    titulo = re.sub(r"\s{2,}", " ", titulo)

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
