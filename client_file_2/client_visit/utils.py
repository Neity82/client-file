def client_normalize(client: str) -> str:
    client = "".join(c for c in client if c != '.' and not c.isdigit())
    return client

