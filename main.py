import json
import autentica_spotify as connect
from dotenv import load_dotenv
import time

load_dotenv()

# Configurações
ARQUIVO_MUSICAS = "database/musicas_nomes_organizados.json"
NOME_PLAYLIST = "X-Tudinho"

# Escopo para criar playlists privadas
SCOPE = "playlist-modify-private"


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
    inicio = time.time() # Marca o início da execução
    sp = connect.autentica_spotify()

    user_id = sp.current_user()["id"]
    print(f"Usuário autenticado: {user_id}")

    # Cria a playlist (privada/pública)
    playlist = sp.user_playlist_create(user=user_id, name=NOME_PLAYLIST, public=False, description="Playlist migrada de músicas locais.")
    playlist_id = playlist["id"]
    print(f"Playlist criada: {NOME_PLAYLIST} (ID: {playlist_id})")

    musicas = ler_musicas(ARQUIVO_MUSICAS)
    track_ids = []

    nao_encontradas = []
    id_nao_encontradas = 1  # ID para as músicas não encontradas
    # musicas = musicas[:300]  # Limita a 600 músicas para testes
    for m in musicas:
        query = m['title'].strip()  # só título, sem artista
        print(f"Buscando: {query}")
        resultado = sp.search(q=query, type="track", limit=3)
        melhor_match = None
        melhor_score = 0
        for track in resultado.get("tracks", {}).get("items", []):
            nome = track["name"].lower()
            print(f"  Verificando: {nome} - {track['artists'][0]['name']}") # Mostra o nome da música e artista
            score = jaccard_sim(m["title"], track["name"])
            if score > melhor_score:
                melhor_score = score
                melhor_match = track

        if melhor_match and melhor_score > 0.09:
            print(f"  ✅ Encontrado: {melhor_match['name']} - {melhor_match['artists'][0]['name']}")
            track_ids.append(melhor_match["id"])
        else:
            print(f"  ❌ Não encontrado: {query}")
            m["score"] = round(melhor_score, 2)  # adiciona o score no JSON
            m["id"] = id_nao_encontradas  
            id_nao_encontradas += 1       
            nao_encontradas.append(m)

        print(f"Score: {melhor_score:.2f}")

    # Salva as não encontradas em JSON
    if nao_encontradas:
        with open("database/nao_encontradas.json", "w", encoding="utf-8") as f:
            json.dump(nao_encontradas, f, indent=2, ensure_ascii=False)
        print(f"\n⚠️ {len(nao_encontradas)} músicas não foram encontradas e foram salvas em 'nao_encontradas.json'")


    # Adiciona as faixas na playlist (em blocos de 100, limite da API)
    for i in range(0, len(track_ids), 100):
        sp.playlist_add_items(playlist_id, track_ids[i:i+100])

    print(f"\n✔️ Total de músicas adicionadas: {len(track_ids)}")

    fim = time.time() # Mostra o tempo de execução
    duracao = fim - inicio
    print(f"\n🕒 Tempo de execução: {duracao:.2f} segundos")

if __name__ == "__main__":
    main()
