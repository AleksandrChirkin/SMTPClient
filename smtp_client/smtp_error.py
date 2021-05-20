class SMTPError(Exception):
    def __init__(self, message: str):
        self.message = f'SMTP Error {message}'

    def __str__(self) -> str:
        return self.message
