from datetime import datetime
from typing import List
from env import constants

from src.auth import AuthSession
from src.service import request_last_ticket_emitted, request_ticket
from src.ticket import Ticket

from src.ticket_item import TicketItem
from src.user_config import UserConfig


class TicketGenerator():
    def __init__(
        self,
        user: UserConfig,
        auth: AuthSession,
    ) -> None:
        self.auth = auth
        self.user = user

    def __date_format(self, date: datetime):
        return int(date.strftime("%Y%m%d"))

    def get_previous_ticket_n(self):
        return request_last_ticket_emitted(self.auth.generate_auth_header(), self.user.get_pto_vta())

    def authorize_ticket(
        self,
        ticket=Ticket
    ):
        prev_ticket_n = self.get_previous_ticket_n() + 1

        req = {
            'FeCabReq': {
                'CantReg': 1,
                'PtoVta': self.user.get_pto_vta(),
                'CbteTipo': self.user.get_cbe_type()
            },
            'FeDetReq': {
                'FECAEDetRequest': {
                    'Concepto': int(ticket.get_type_of_ticket()),
                    'DocTipo': ticket.get_rec_doc_code(),
                    'DocNro': ticket.get_rec_doc_nr(),
                    'CbteDesde': prev_ticket_n,
                    'CbteHasta': prev_ticket_n,
                    'CbteFch': self.__date_format(ticket.get_emission_date()),
                    'ImpTotal': ticket.get_total(),
                    'ImpTotConc': 0,  # debe ser 0
                    'ImpNeto': ticket.get_total(),
                    'ImpOpEx': 0,  # debe ser 0
                    'ImpIVA': ticket.get_taxes(),
                    'ImpTrib': ticket.get_taxes(),
                    'FchServDesde': self.__date_format(ticket.get_since()),
                    'FchServHasta': self.__date_format(ticket.get_to()),
                    'FchVtoPago': self.__date_format(ticket.get_payment_vto()),
                    'MonId': constants['MON_ID'],
                    'MonCotiz': constants['MON_COTZ'],
                }
            }
        }

        recipt = request_ticket(auth=self.auth.generate_auth_header(), req=req)
        ticket.set_recipt(recipt)
