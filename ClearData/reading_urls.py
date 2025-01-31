class ReadingURLs:
    @staticmethod
    def read_urls(file_path):
        with open(file_path, 'r') as file:
            urls = file.readlines()
        # Usuń ewentualne białe znaki (np. nową linię) z każdej linii
        return [url.strip() for url in urls]
