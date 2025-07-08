import json
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import time
import os

load_dotenv()

# Configurações
ARQUIVO_MUSICAS = "database/nao_encontradas1.json"
ID_PLAYLIST_EXISTENTE = "2b8DSYBpxpmOssYkNOIzC9"  # 👈 Coloque o ID da playlist aqui
SCOPE = SCOPE = "playlist-modify-private playlist-modify-public"

def jaccard_sim(a, b):
    a_set = set(a.lower().split())
    b_set = set(b.lower().split())
    intersec = a_set.intersection(b_set)
    union = a_set.union(b_set)
    return len(intersec) / len(union) if union else 0

def ler_musicas(arquivo):
    with open(arquivo, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    inicio = time.time()
    sp = Spotify(auth_manager=SpotifyOAuth(scope=SCOPE, cache_path=".cache"), requests_timeout=15)

    user_id = sp.current_user()["id"]
    print(f"Usuário autenticado: {user_id}")
    playlist_id = ID_PLAYLIST_EXISTENTE
    print(f"Usando playlist existente (ID: {playlist_id})")

    musicas = ler_musicas(ARQUIVO_MUSICAS)
    track_ids = []
    nao_encontradas = []

    for m in musicas:
        query = m['title'].strip()
        print(f"Buscando: {query}")
        resultado = sp.search(q=query, type="track", limit=3)
        melhor_match = None
        melhor_score = 0

        for track in resultado.get("tracks", {}).get("items", []):
            nome = track["name"].lower()
            print(f"  Verificando: {nome} - {track['artists'][0]['name']}")
            score = jaccard_sim(m["title"], track["name"])
            if score > melhor_score:
                melhor_score = score
                melhor_match = track

        if melhor_match and melhor_score > 0.09:
            print(f"  ✅ Encontrado: {melhor_match['name']} - {melhor_match['artists'][0]['name']}")
            track_ids.append(melhor_match["id"])
        else:
            print(f"  ❌ Não encontrado: {query}")
            m["score"] = round(melhor_score, 2)
            nao_encontradas.append(m)

        print(f"Score: {melhor_score:.2f}")

    if nao_encontradas:
        with open("database/nao_encontradas.json", "w", encoding="utf-8") as f:
            json.dump(nao_encontradas, f, indent=2, ensure_ascii=False)
        print(f"\n⚠️ {len(nao_encontradas)} músicas não foram encontradas e foram salvas em 'nao_encontradas.json'")

    for i in range(0, len(track_ids), 100):
        sp.playlist_add_items(playlist_id, track_ids[i:i+100])

    print(f"\n✔️ Total de músicas adicionadas: {len(track_ids)}")
    print(f"\n🕒 Tempo de execução: {time.time() - inicio:.2f} segundos")

if __name__ == "__main__":
    main()
