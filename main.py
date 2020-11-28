
from threading import Thread
from src import Bot
from src.webserver import partial_run


if __name__ == "__main__":

    print("[i] Alan Turing webserver started !")
    Thread(target=partial_run).start()

    print("[i] Alan Turing bot started !")
    Bot().start()
