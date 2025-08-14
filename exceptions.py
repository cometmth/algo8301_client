class Algo8301Error(Exception):
    pass

class RequestError(Algo8301Error):
    def __init__(self, status_code: int, message: str = ""):
        super().__init__(f"Request failed with status {status_code}: {message}")
