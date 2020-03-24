from .repository_yahoo import YahooRepository

REPOSITORIES = [
    YahooRepository()
]

def find_repository_by_name(name: str):
    repo = None
    for item in REPOSITORIES:
        if name == item.name:
            repo = item
            break
    return repo
