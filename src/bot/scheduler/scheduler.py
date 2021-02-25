
from src.bot.scheduler import Reminder
from src.bot.scheduler.messages import AttendanceMessage as Attendance
from src.bot.becode import Periods


class Scheduler:

    def __init__(self):
        pass

    def initialize(self):

        # Morning reunions and attendances
        Reminder("Pointage 09h00", 'mon, tue, wed, thu, fri', 8, 50, True, [Attendance(Periods.MORNING)])

        # Lunch attendances
        Reminder("Pointage 12h30", 'mon, tue, wed, thu, fri', 12, 30, True, [Attendance(Periods.LUNCH)])

        # Noon attendances
        Reminder("Pointage 13h30", 'mon, tue, wed, thu, fri', 13, 20, True, [Attendance(Periods.NOON)])

        # Evening attendances
        Reminder("Pointage 17h00", 'mon, tue, wed, thu, fri', 17, 00, True, [Attendance(Periods.EVENING)])
        return self

    @staticmethod
    def start():
        Reminder.start()
