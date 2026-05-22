from backend.utils.utils import jaccard_sim

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