from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

# Configurações
SCOPE = "user-read-private"

def jaccard_sim(a, b):
    a_set = set(a.lower().split())
    b_set = set(b.lower().split())
    intersec = a_set.intersection(b_set)
    union = a_set.union(b_set)
    return len(intersec) / len(union) if union else 0

def buscar_musica(sp, titulo, artista=""):
    query = f"{titulo} {artista}".strip()
    print(f"\n🔎 Buscando: {query}")

    resultado = sp.search(q=query, type="track", limit=5)
    items = resultado.get("tracks", {}).get("items", [])

    if not items:
        print("❌ Nenhum resultado encontrado.")
        return

    print("✅ Resultados ranqueados por similaridade (Jaccard):")
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

    resultados_com_score.sort(key=lambda x: x["score"], reverse=True)

    for i, r in enumerate(resultados_com_score, 1):
        print(f"{i}. {r['nome']} - {r['artistas']} (Score: {r['score']}) - ID: {r['id']}")

def main():
    sp = Spotify(auth_manager=SpotifyOAuth(scope=SCOPE, cache_path=".cache"))

    while True:
        titulo = input("\n🎵 Digite o título da música (ou 'sair' pra encerrar): ").strip()
        if titulo.lower() == "sair":
            print("👋 Encerrando...")
            break

        artista = input("🎤 Digite o nome do artista (ou deixe em branco): ").strip()
        buscar_musica(sp, titulo, artista)

if __name__ == "__main__":
    main()
