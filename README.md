# 🎵 Local to Spotify

Transfere suas músicas locais (MP3, M4A etc.) para playlists no Spotify, com funções de limpeza de metadados, busca inteligente e tratamento de músicas não encontradas.

---

## 📂 Estrutura

- **`extrair_metadados.py`**  
  Lê os arquivos locais (`.mp3`, `.m4a`) e extrai título, artista e nome do arquivo, salvando tudo em um JSON.

- **`organiza_nomes.py`**  
  Processa os títulos/artistas, removendo emojis, parênteses, marcações como `feat.` ou `prod.`, espaços extras etc. Gera um JSON “organizado”, pronto para ser usado na busca.

- **`main.py`**  
  Função principal que cria uma playlist no Spotify e adiciona as músicas encontradas a partir do JSON organizado. As músicas não encontradas são salvas em um novo JSON.

- **`atualizar_playlist_existente.py`**  
  Atualiza uma playlist já existente no Spotify, lendo um JSON de músicas, buscando por elas e adicionando as encontradas à playlist.

- **`busca_musicas.py`**  
  Realiza buscas usando a API do Spotify. Dado um título e/ou artista, retorna os resultados da pesquisa no terminal (padrão: 5 resultados).

- **`cria_playlist_artista.py`**  
  Filtra músicas de um artista específico dentro de uma playlist existente e cria uma nova playlist apenas com essas faixas. Útil para separar músicas de artistas favoritos.

- **`visualizar_playlist.py`**  
  Lista todas as músicas de uma playlist e permite exportá-las como `.txt` ou `.json`. Pode ser útil para migração entre plataformas ou análise pessoal.

- **`.env`**  
  Armazena as credenciais de acesso à API do Spotify (ID e secret).

- **`database/`**  
  Pasta onde ficam os arquivos `.json` com os dados extraídos, organizados ou não encontrados.

---

## 🧰 Tecnologias e dependências

Desenvolvido em **Python 3.10+**, utilizando:

- [Mutagen](https://pypi.org/project/mutagen/) – leitura de metadados de áudio
- [Spotipy](https://spotipy.readthedocs.io/) – Spotify Web API
- [dotenv](https://pypi.org/project/python-dotenv/) – variáveis de ambiente

Instale com:
```bash
pip install mutagen spotipy python-dotenv
```

---

## ⚙️ Configuração

Copie o arquivo `.env.example` para `.env` e adicione:

```
SPOTIPY_CLIENT_ID=seu_id
SPOTIPY_CLIENT_SECRET=seu_secret
SPOTIPY_REDIRECT_URI=http://localhost:8888/callback
```

👉 No [Spotify Developer Dashboard](https://developer.spotify.com), crie uma app e configure essa URI (mesmo que seja `http://localhost:8888/callback`). Exclua o cache (`.cache`) após adicionar novos escopos.

---

## 🚀 Como usar
### 1. Extraia os metadados das músicas locais:
```bash
python extrair_metadados.py
```
> Lê os arquivos `.mp3` ou `.m4a` da pasta e gera um JSON (`musicas.json`) com título, artista e nome do arquivo.

### 2. Organize os nomes extraídos:
```bash
python organiza_nomes.py
```
> Remove emojis, textos extras, espaços duplos, etc., gerando um novo arquivo (`musicas_nomes_organizados.json`) mais limpo para busca.

### 3. Crie uma nova playlist no Spotify com as músicas encontradas:
```bash
python main.py
```
> Utiliza o JSON organizado para buscar cada música e adicioná-las à nova playlist. As músicas não encontradas são salvas separadamente.

### 4. Adicione músicas a uma playlist existente:
```bash
python adiciona_na_playlist.py
```
> Altere o ID da playlist no código para indicar qual playlist atualizar com as músicas do JSON.

### 5. Visualize as músicas de uma playlist no Spotify:
```bash
python visualizar_playlist.py
```
> Insira o ID da sua playlist no código e visualize todas as músicas que estão nela, poderá salvar em um TXT ou Json para analisar ou até trocar para outra plataforma se desejado.

### 6. Crie uma playlist do seu artista favorito:
```bash
python cria_playlist_artista.py
```
> Separe as músicas que mais gosta daquele artista favorito. Em uma playlist com músicas de diversos artistas, será possível criar uma nova playlist apenas escrevendo o nome do artista nessa função e todas as músicas do artistas que estiverem naquela playlist, irão para uma nova playlist.

### 7. Pesquise a sua música pela API e analise os resultados:
```bash
python busca_musicas.py
```
> Colocando o título e/ou artista de uma música, será retornado pela API resultados da pesquisa juntamente com o *SCORE* do algoritmo *Jaccard* ordenado pela maior pontuação, dessa forma podemos analisar resultados e realizar testes.
---

💡 Lembre-se de configurar corretamente seu arquivo `.env` com as credenciais da API do Spotify (client ID, secret e redirect URI).


---

## 🗂️ Arquivos de saída

- `musicas.json` – dados brutos extraídos
- `musicas_nomes_organizados.json` – meta dados tratados
- `nao_encontradas.json` – músicas que não foram encontradas no Spotify (com `score` e `id`)
- `musicas_playlist.txt/json` – lista de músicas importadas

---

## 💡 Melhorias futuras

- Interface gráfica (Tkinter, Web, outros)
- Melhor heurística de similaridade (`Levenshtein`, etc.)
- Aceito sugestões :D

---

## 📄 Licença

MIT — veja o arquivo `LICENSE` para detalhes.
