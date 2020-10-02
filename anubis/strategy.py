import itertools
from dataclasses import dataclass


@dataclass
class Server:
    url: str = "localhost:8080"  # localhost:8080
    alive: bool = True  # dead or alive

def get_alive_servers(servers):
    return [server for server in servers if server.alive is True]


def go_round(servers):
    yield from itertools.cycle(servers)


def least_connections(servers):
    return [server for server in servers if server.alive is True]


class Strategy:
    def __init__(self, servers):
        self.servers = get_alive_servers(servers)
        self.round_iterator = go_round(self.servers)

    def round_robin(self):
        allocated_server = next(self.round_iterator)
        return allocated_server


server1 = Server(url="http://web1:80")
server2 = Server(url="http://web2:80")
server3 = Server(url="http://web3:80")

Strategy = Strategy(servers=[server1, server2, server3])
