import logging

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import config as c

load_dotenv()

def autentica_spotify():
    logger = logging.getLogger(__name__)
    sp = Spotify(auth_manager=SpotifyOAuth(scope=c.SCOPE_PRIVATE, cache_path=".cache"), requests_timeout=15)
    logger.info(f"Usuário autenticado: {sp.current_user()['id']}")
    return sp

# logging.basicConfig(level=getattr(logging, c.LOG_LEVEL))
# teste = autentica_spotify()