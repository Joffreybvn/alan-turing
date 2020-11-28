
from src import Database

from discord.ext.commands import Bot
from os import environ


class Config:

    def __init__(self):

        # ENV variables
        self.DISCORD_TOKEN = environ.get('DISCORD_TOKEN')
        self.DISCORD_CHANNEL_ID = int(environ.get('DISCORD_CHANNEL'))
        self.WEBHOOK = environ.get('WEBHOOK')

        # Discord client
        self.discord = Bot(command_prefix='!')

        # Database
        db_host = environ.get('DB_HOST')
        db_password = environ.get('DB_PASSWORD')
        self.db = Database(db_host, db_password)

        # Attendance globals
        self.last_message = None
        self.last_attendance = None  # Period, see >> AttendanceMessage.py


config = Config()
