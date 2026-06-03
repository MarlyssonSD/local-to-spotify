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
    print(f"✅ Total de playlists encontradas: {len(playlists)}")
    for p in playlists:
        print(f"- {p['nome']} (ID: {p['id']}, Total de músicas: {p['total_musicas']})")
        
    return playlists

def jaccard_sim(a, b):
    '''Calcula a similaridade de Jaccard entre duas strings.
    A similaridade de Jaccard é definida como o tamanho da interseção dividido pelo tamanho da união dos conjuntos de palavras.
    '''
    a_set = set(a.lower().split())
    b_set = set(b.lower().split())
    intersec = a_set.intersection(b_set)
    union = a_set.union(b_set)
    return len(intersec) / len(union) if union else 0

# # teste de ler listar playlists
# if __name__ == "__main__":
#     from backend.core import autenticar_spotify as connect
#     sp = connect.autentica_spotify()
#     listar_playlists(sp)