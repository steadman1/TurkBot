import requests
from enum import Enum

class BayQuery:
    def __init__(self, id, name, info_hash, leechers, seeders, num_files, size, username, added, status, category, imdb, total_found=None):
        self.id = id
        self.name = name
        self.info_hash = info_hash
        self.leechers = leechers
        self.seeders = seeders
        self.num_files = num_files
        self.size = size
        self.username = username
        self.added = added
        self.status = status
        self.category = category
        self.imdb = imdb
        self.total_found = total_found

class Category(Enum):
    ALL = 'all'
    AUDIO = 'audio'
    VIDEO = 'video'
    ADULT = 'xxx'
    APPLICATIONS = 'applications'
    GAMES = 'games'
    OTHER = 'other'

class OrderBy(Enum):
    NAME = 'name'
    DATE = 'date'
    SIZE = 'size'
    SEEDS = 'seeds'
    LEECHES = 'leeches'

class SortBy(Enum):
    ASCEND = 'asc'
    DESCEND = 'desc'

class ApiBay:
    def __init__(self) -> None:
        self.base_url = "https://apibay.org/"

    def search(self, query, results_count=10, category: Category=Category.VIDEO, verified=True, page=1, orderBy: OrderBy=OrderBy.LEECHES, sortBy: SortBy=SortBy.ASCEND):
        try:
            url = f"{self.base_url}q.php?q={query}&category={category}&verified={verified}"
            if verified is not None:
                url += f"&verified={verified}"
            if page is not None:
                url += f"&page={page}"
            if orderBy is not None:
                url += f"&orderBy={orderBy}"
            if sortBy is not None:
                url += f"&sortBy={sortBy}"
            
            response = requests.get(url)
            if response.status_code == 200:
                results = response.json()[:results_count]
                bay_queries = []
                for result in results:
                    bay_query = BayQuery(**result)
                    bay_queries.append(bay_query)
                return bay_queries
            else:
                print(f"Failed to send request. Status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error sending request: {e}")
            return None
