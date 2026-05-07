def obter_nome_playlist_id(sp, playlist_id):
    try:
        playlist = sp.playlist(playlist_id)
        return playlist["name"]
    except Exception as e:
        print(f"❌ Erro ao obter nome da playlist: {e}")
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
        print(f"❌ Erro ao verificar música na playlist: {e}")
        return False