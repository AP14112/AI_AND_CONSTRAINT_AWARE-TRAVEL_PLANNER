import sys
import traceback

class CustomException(Exception):
    def __init__(self, error: Exception):
        self.error = error
        self.traceback = traceback.format_exc()
        super().__init__(str(error))

    def __str__(self):
        return f"{self.error}\nTraceback:\n{self.traceback}"
