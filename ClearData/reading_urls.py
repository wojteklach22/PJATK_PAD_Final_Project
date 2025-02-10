from typing import Any


class ReadingURLs:
    @staticmethod
    def read_urls(file_path: Any) -> list[str]:
        with open(file_path, 'r') as file:
            urls = file.readlines()
        # Usuń ewentualne białe znaki (np. nową linię) z każdej linii
        return [url.strip() for url in urls]
