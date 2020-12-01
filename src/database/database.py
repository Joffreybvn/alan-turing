
from typing import Union, List
from pymongo import MongoClient
from pymongo.errors import AutoReconnect, ConnectionFailure, DuplicateKeyError, ExecutionTimeout, OperationFailure
from src.database import DatabaseUtils


class Database(DatabaseUtils):
    """
    Small database used to store the becode token and
    if a user want to receive notifications or not.
    """

    def __init__(self, db_host: str, db_password: str) -> None:
        super().__init__()

        # Connect to MongoDB
        self.client = MongoClient(f"mongodb+srv://dbUser:{db_password}@{db_host}")
        self.db = self.client.discord_db

    def create(self, user_id: int, send_notification: bool = False,
               becode_token: str = None, public_key: str = None,
               public_id: int = None) -> bool:
        """
        Create a new user to the database.

        :param public_id:
        :param public_key:
        :param becode_token:
        :param send_notification:
        :param user_id: The user to add to the database.
        :return: True if the user was added. False if not.
        """

        # Avoid send_notification to be None:
        if send_notification is None:
            send_notification = False

        # Insert a new user into the database
        try:
            self.db.users.insert_one({
                "_id": user_id,
                "send_notification": send_notification,
                "becode_token": becode_token,
                "public_id": public_id,
                "public_key": public_key
            })

        # TODO: Write a decorator
        # Return False if the operation fail
        except (AutoReconnect, ConnectionFailure, DuplicateKeyError,
                ExecutionTimeout, OperationFailure):
            return False

        return True

    def update(self, dict_id: dict, send_notification: bool = None,
               becode_token: str = None, public_key: str = None) -> bool:
        """Update a given user with the given values."""

        # If the given dictionary has only an _id
        if ('_id' in dict_id and len(dict_id) == 1

                # If the user doesn't exists
                and self.db.users.find_one(dict_id) is None):

            # Create a new user to the database
            return self.create(dict_id['_id'], send_notification, becode_token)

        else:
            # Create the update dictionary
            to_set = dict()

            # Add send_notification to the update
            if send_notification is not None:
                to_set['send_notification'] = send_notification

            # Add becode_token to the update
            if becode_token is not None:
                to_set['becode_token'] = becode_token

            # Add auth_key to the update
            if public_key is not None:
                to_set['public_key'] = public_key

            # Update the user
            self.db.users.update_one(dict_id, {'$set': to_set})
            return True  # TODO: Implement a return of the request's outcome

    def get_users_to_mention(self) -> List[int]:
        """Return a list of all user to notify on reminders."""

        # Get the users' _id with "send_notification" to True
        notified = self.db.users.find(
            {'send_notification': True},
            {'_id': 1}
        )

        # Return a list of all users' _id
        return [entry['_id'] for entry in list(notified)]

    def get_token(self, user_id: int) -> Union[str, None]:
        """Return the token of a given user."""

        # Query the given user and get the token
        result = self.db.users.find_one(
            {'_id': user_id},
            {'_id': 0, 'becode_token': 1}
        )

        # Return the token or None if missing
        return result.get('becode_token', None)

    def get_data_from_public_key(self, public_key: str) -> dict:
        """Remove the auth_key of the user that own the given auth_key."""

        # Get the user send_notification and becode_token data
        user = self.db.users.find_one(
            {'public_key': public_key},
            {'_id': 1, 'send_notification': 1, 'becode_token': 1}
        )

        print(user)

        # Create a random public id and a maximum date of response
        user['public_id'], user['date'] = self._generate_public_id()

        # Update the user: remove the auth_key and save the public_id
        self.db.users.update_one(
            {'_id': user['_id']},
            {'$set': {'auth_key': None, 'public_id': user['public_id']}}
        )

        # Remove the user _id from the returned dictionary
        del user['_id']

        return user
