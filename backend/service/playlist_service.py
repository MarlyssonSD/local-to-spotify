
import backend.core.config as config 
import logging

from backend.utils.utils import jaccard_sim

logger = logging.getLogger(__name__)

def buscar_musica(sp, titulo, artista=""):
    query = f"{titulo} {artista}".strip()

    resultado = sp.search(q=query, type="track", limit=5)
    items = resultado.get("tracks", {}).get("items", [])

    if not items:
        return []

    resultados_com_score = []

    for item in items:
        nome = item["name"]
        artistas = ", ".join(a["name"] for a in item["artists"])

        score = jaccard_sim(titulo, nome)

        resultados_com_score.append({
            "nome": nome,
            "artistas": artistas,
            "id": item["id"],
            "score": round(score, 2)
        })

    resultados_com_score.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return resultados_com_score

def obter_nome_playlist_id(sp, playlist_id):
    try:
        playlist = sp.playlist(playlist_id)
        return playlist["name"]
    except Exception as e:
        logger.error(f"❌ Erro ao obter nome da playlist: {e}")
        return "playlist_desconecida"
    
def verificar_musica_na_playlist(sp, playlist_id, track_id):
    try:
        resultados = sp.playlist_items(playlist_id, fields="items.track.id,next", additional_types=["track"])
        while resultados:
            for item in resultados["items"]:
                track = item["track"]
                if track and track["id"] == track_id:
                    return True
            if resultados.get("next"):
                resultados = sp.next(resultados)
            else:
                break
        return False
    except Exception as e:
        logger.error(f"❌ Erro ao verificar música na playlist: {e}")
        return False
    
def listar_playlists(sp):
    playlists = []

    resultados = sp.current_user_playlists()

    while resultados:
        for item in resultados["items"]:
            playlists.append({
                "id": item["id"],
                "nome": item["name"],
                "total_musicas": item["tracks"]["total"]
            })

        if resultados["next"]:
            resultados = sp.next(resultados)
        else:
            break
    logger.info(f"✅ Total de playlists encontradas: {len(playlists)}")
    for p in playlists:
        logger.info(f"- {p['nome']} (ID: {p['id']}, Total de músicas: {p['total_musicas']})")
        
    return playlists

def listar_musicas_curtidas(sp):
    musicas = []

    resultados = sp.current_user_saved_tracks()

    while resultados:
        for item in resultados["items"]:
            track = item["track"]

            musicas.append({
                "nome": track["name"],
                "artista": track["artists"][0]["name"],
                "id": track["id"]
            })

        if resultados["next"]:
            resultados = sp.next(resultados)
        else:
            break
    logger.info(f"✅ Total de músicas curtidas encontradas: {len(musicas)}")
    for m in musicas:
        logger.info(f"- {m['nome']} - {m['artista']} (ID: {m['id']})")
    return musicas

# Verifica se tem música duplicada na playlist 
def verificar_musica_existente_playlist(sp, playlist_id, track_id):
    ''''''
    try:
        resultados = sp.playlist_items(playlist_id, fields="items.track.id,next", additional_types=["track"])
        while resultados:
            for item in resultados["items"]:
                track = item["track"]
                if track and track["id"] == track_id:
                    return True
            if resultados.get("next"):
                resultados = sp.next(resultados)
            else:
                break
        return False
    except Exception as e:
        logger.error(f"❌ Erro ao verificar música duplicada na playlist: {e}")
        return False

# teste de ler listar playlists
if __name__ == "__main__":
    from backend.core import autenticar_spotify as connect
    sp = connect.autentica_spotify()
    # listar_playlists(sp)
    listar_musicas_curtidas(sp)