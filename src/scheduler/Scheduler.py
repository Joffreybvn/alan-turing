
from src.scheduler import Reminder
from src.scheduler.messages import AttendanceMessage as Attendance
from src.scheduler.messages import GoogleMeetMessage as Meet
from src.scheduler.messages import PauseMessage as Pause
from src.web.becode import Periods


class Scheduler:

    def __init__(self):
        pass

    def initialize(self):

        # Morning reunions and attendances
        Reminder("Pointage 9h - Becode", 'tue, wed, thu', 8, 50, True, [Attendance(Periods.MORNING)])
        Reminder("Pointage 9h - Home", 'mon, fri', 8, 50, True, [Meet("réunion", 10), Attendance(Periods.MORNING)])

        # Pauses
        Reminder("Pause 11h - All", 'mon-fri', 11, 0, True, [Pause(15)])
        Reminder("Pause 15h - All", 'mon-fri', 15, 0, True, [Pause(15)])

        # Lunch attendances
        Reminder("Pointage 12h30 - Becode", 'tue, wed, thu', 12, 30, True, [Attendance(Periods.LUNCH)])
        Reminder("Pointage 12h30 - Home", 'mon, fri', 12, 30, True, [Attendance(Periods.LUNCH)])

        # Noon attendances
        Reminder("Pointage 13h30 - Becode", 'tue, wed, thu', 13, 20, True, [Attendance(Periods.NOON)])
        Reminder("Pointage 13h30 - Home", 'mon, fri', 13, 20, True, [Meet("veille", 10), Attendance(Periods.NOON)])

        # Evening reunions
        Reminder("Débriefing 16h45 - Home", 'mon', 16, 35, False, [Meet("débriefing", 10)])
        Reminder("Kahoot 16h40 - Home", 'fri', 16, 30, False, [Meet("kahoot", 10)])

        # Evening attendances
        Reminder("Pointage 17h00 - Becode", 'tue, wed, thu', 17, 00, True, [Attendance(Periods.EVENING)])
        Reminder("Pointage 17h00 - Home", 'mon, fri', 17, 00, True, [Attendance(Periods.EVENING)])

        return self

    @staticmethod
    def start():
        Reminder.start()
