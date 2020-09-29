"""Server."""

from dataclasses import dataclass

@dataclass
class Server:
    url: str = 'localhost:8080' # localhost:8080
    alive: bool = True # dead or alive