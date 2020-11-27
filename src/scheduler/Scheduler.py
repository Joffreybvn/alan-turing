
from src.scheduler import Reminder
from src.scheduler.messages import AttendanceMessage as AttendanceMsg
from src.scheduler.messages import GoogleMeetMessage as MeetMsg
from src.scheduler.messages import PauseMessage as PauseMsg
from src.web.becode import Periods


class Scheduler:

    def __init__(self):
        pass

    def initialize(self):

        # Morning reunions and attendances
        Reminder("Pointage 9h - Becode", 'tue, wed, thu', 8, 50, True, [AttendanceMsg(Periods.MORNING)])
        Reminder("Pointage 9h - Home", 'mon, fri', 8, 50, True, [MeetMsg("réunion", 10), AttendanceMsg(Periods.MORNING)])

        # Pauses
        Reminder("Pause 11h - All", 'mon-fri', 11, 0, True, [PauseMsg(15)])
        Reminder("Pause 15h - All", 'mon-fri', 15, 0, True, [PauseMsg(15)])

        # Lunch attendances
        Reminder("Pointage 12h30 - Becode", 'tue, wed, thu', 12, 30, True, [AttendanceMsg(Periods.LUNCH)])
        Reminder("Pointage 12h30 - Home", 'mon, fri', 12, 30, True, [AttendanceMsg(Periods.LUNCH)])

        # Noon attendances
        Reminder("Pointage 13h30 - Becode", 'tue, wed, thu', 13, 20, True, [AttendanceMsg(Periods.NOON)])
        Reminder("Pointage 13h30 - Home", 'mon, fri', 13, 20, True, [MeetMsg("veille", 10), AttendanceMsg(Periods.NOON)])

        # Evening reunions
        Reminder("Débriefing 16h45 - Home", 'mon', 16, 35, False, [MeetMsg("débriefing", 10)])
        Reminder("Kahoot 16h40 - Home", 'fri', 16, 30, False, [MeetMsg("kahoot", 10)])

        # Evening attendances
        Reminder("Pointage 17h00 - Becode", 'tue, wed, thu', 17, 00, True, [AttendanceMsg(Periods.EVENING)])
        Reminder("Pointage 17h00 - Home", 'mon, fri', 17, 00, True, [AttendanceMsg(Periods.EVENING)])

        return self

    @staticmethod
    def start():
        Reminder.start()
