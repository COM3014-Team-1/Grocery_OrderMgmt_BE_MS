class Response:
    def __init__(self, message, data=None):
        self.message = message
        self.data = data
    
    def to_dict(self):
        response={"message" : self.message}

        if self.data is not None:
            response={
                    "message" : self.message,
                    "object" : self.data
                }
        return response