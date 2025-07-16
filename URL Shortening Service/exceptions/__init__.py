class AppException(Exception):
    def __init__(self, message="Internal Server Error", status_code=500):
        self.message = message
        self.status_code = self.status_code or status_code
        super().__init__(self.message)
