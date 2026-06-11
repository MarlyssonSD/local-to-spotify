from dataclasses import dataclass

@dataclass
class Playlist:
    id: str
    nome: str
    total_musicas: int