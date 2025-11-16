class Cupon:
    code:str
    value:str
    used:bool
    def __init__(self, code:str, value:str, used:bool):
        self.code=code
        self.value=value
        self.used=used