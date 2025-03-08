class PesopolistException(Exception):
    def __init__(self, description: str = "Unknown pesopolist error", status_code: int = 500):
        self.description = description
        self.status_code = status_code
        super().__init__(self.description)
