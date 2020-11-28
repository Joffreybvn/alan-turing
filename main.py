
from threading import Thread
from src.bot import Bot
from src.api.api import partial_run


if __name__ == "__main__":

    print("[i] Alan Turing webserver started !")
    Thread(target=partial_run).start()

    print("[i] Alan Turing bot started !")
    Bot().start()
