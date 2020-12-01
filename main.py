
import os
from threading import Thread
from functools import partial
from src.bot import Bot
from src.api.api import create_api

port = int(os.environ.get("PORT", 3000))


if __name__ == "__main__":

    print("[i] Alan Turing webserver started !")
    partial_run = partial(create_api().run, host="0.0.0.0", port=port, debug=False, use_reloader=False)
    Thread(target=partial_run).start()

    print("[i] Alan Turing bot started !")
    Bot().start()
