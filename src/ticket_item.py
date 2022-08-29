class TicketItem:
    def __init__(
        self,
        description: str,
        unit_price: float,
        units: int = 1,
        code: str = ''
    ) -> None:
        self.description = description
        self.unit_price = unit_price
        self.units = units
        self.code = code

    def get_code(self):
        return self.code

    def get_description(self):
        return self.description

    def get_unit_price(self):
        return self.unit_price

    def get_units(self):
        return self.units

    def get_subtotal(self):
        return self.units * self.unit_price
