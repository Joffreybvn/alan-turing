
import random
import datetime
from typing import Tuple


class DatabaseUtils:

    def __init__(self):
        pass

    @staticmethod
    def _generate_public_id(delay: int = 5) -> Tuple[str, str]:
        """
        Generate a public_id, based on a random number and a timestamp.
        The public_id will be useless if a request is made with it after
        the timestamp.

        :param delay: The delay used to create a timestamp.
        :type delay: int

        :return: The public_id, usable only during the following minutes,
            defined by the delay parameter.
        :rtype: str
        """

        # Generate a timestamp of 5 minutes later
        date = datetime.datetime.now() + datetime.timedelta(minutes=delay)

        # Generate a long random number
        number = random.getrandbits(128)

        # Return the public_id and the date
        return f'{number}.{date.strftime("%Y%m%d%H%M%S")}', date.isoformat()
