import logging

# Configurações
ARQUIVO_MUSICAS = "database/musicas_nomes_organizados.json"
NOME_PLAYLIST = "X-Tudinho"

# Escopos Spotify
SCOPE_PRIVATE = (
    "user-library-read "
    "playlist-read-private "
    "playlist-read-collaborative "
    "playlist-modify-private "
    "playlist-modify-public "
    "user-read-private "
    "user-read-email "
    "user-top-read "
    "user-read-recently-played "
    "user-follow-read "
    "user-follow-modify"
)

# Logging
LOG_LEVEL = logging.INFO

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(levelname)s | %(name)s | %(message)s"
)