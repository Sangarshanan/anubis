import itertools
from server import Server

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

server1 = Server(url="http://localhost:8000")
server2 = Server(url="http://localhost:8001")
server3 = Server(url="http://localhost:8002")

strategy = Strategy(servers=[server1, server2, server3])
