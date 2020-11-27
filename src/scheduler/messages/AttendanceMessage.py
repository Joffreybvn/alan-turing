
from copy import copy
from src.scheduler.messages import Message, Card, MessageWeight
from src.web.becode import Periods

# my.becode.org URL
URL = "https://my.becode.org"


class AttendanceMessage(Message):

    card = Card(
        title="My BeCode",
        url=URL,
        description=f"In Attendance We Trust ! Pointez maintenant sur [my.becode.org]({URL}). Ou cliquez directement sur l'une des réactions ci-dessous.",
        color=5747135,
        thumbnail="https://i.imgur.com/ixU2HdV.gif",  # "https://i.imgur.com/cg4xd66.png",
    )

    message = f"c'est le moment de **pointer** sur My BeCode"

    def __init__(self, period: Periods) -> None:
        """
        Attendance message: used in a reminder that need to reminds to go to my.becode.org
        """
        super().__init__(AttendanceMessage.message, URL)

        self.weight = MessageWeight.ATTENDANCE
        self.period = period

    def get_card(self) -> Card:
        return copy(AttendanceMessage.card)

    def get_attendance_details(self) -> Periods:
        return self.period
