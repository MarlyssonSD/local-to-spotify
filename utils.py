def obter_nome_playlist_id(sp, playlist_id):
    try:
        playlist = sp.playlist(playlist_id)
        return playlist["name"]
    except Exception as e:
        print(f"❌ Erro ao obter nome da playlist: {e}")
        return "playlist_desconecida"