from datetime import datetime


class UserConfig:
    def __init__(
        self,
        name: str,
        address: str,
        ia: datetime,
    ) -> None:
        self.name = name
        self.ia = ia
        self.address = address

    def get_address(self):
        return self.address

    def get_name(self):
        return self.name

    def get_ia(self):
        return self.ia
