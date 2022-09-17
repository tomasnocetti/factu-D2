class PtoVta:
    def __init__(self, nro: int, description: str) -> None:
        self.nro = nro
        self.description = description

    def get_nro(self):
        return self.nro

    def __str__(self):
        return f'Pto Vta {self.nro} - {self.description}'
