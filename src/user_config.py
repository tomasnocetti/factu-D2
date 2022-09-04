from datetime import datetime


class UserConfig:
    def __init__(
        self,
        name: str,
        address: str,
        ia: datetime,
        pto_v: int,
    ) -> None:
        self.name = name
        self.ia = ia
        self.address = address
        self.pto_v = pto_v

    def get_address(self):
        return self.address

    def get_name(self):
        return self.name

    def get_ia(self):
        return self.ia

    def get_pto_vta(self):
        return self.pto_v
