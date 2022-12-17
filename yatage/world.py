import yaml


class World:
    def __init__(self, version: int, name: str, description: str = None, author: str = None):
        self.version = version
        self.name = name
        self.description = description
        self.author = author

    @classmethod
    def load(cls, filename: str):
        with open(filename, 'rb') as f:
            data = yaml.safe_load(f)

        ret = cls(
            data.get('version'),
            data.get('name'),
            data.get('description'),
            data.get('author')
        )

        return ret
