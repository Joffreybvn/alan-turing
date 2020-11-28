
from typing import Union, List
from pymongo import MongoClient
from pymongo.errors import AutoReconnect, ConnectionFailure, DuplicateKeyError, ExecutionTimeout, OperationFailure


class Database:
    """
    Small database used to store the becode token and
    if a user want to receive notifications or not.
    """

    def __init__(self, db_host: str, db_password: str) -> None:

        # Connect to MongoDB
        self.client = MongoClient(f"mongodb+srv://dbUser:{db_password}@{db_host}")
        self.db = self.client.discord_db

    def create(self, user_id: int, send_notification: bool = False, becode_token: str = None) -> bool:
        """
        Create a new user to the database.

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
                "becode_token": becode_token
            })

        # TODO: Write a decorator
        # Return False if the operation fail
        except (AutoReconnect, ConnectionFailure, DuplicateKeyError,
                ExecutionTimeout, OperationFailure):
            return False

        return True

    def update(self, user_id: int, send_notification: bool = None, becode_token: str = None) -> bool:
        """Update a given user with the given values."""

        # If the user doesn't exists, create it
        if self.db.users.find_one({'_id': user_id}) is None:
            return self.create(user_id, send_notification, becode_token)

        else:
            # Create the update dictionary
            to_set = dict()

            # Add send_notification to the update
            if send_notification is not None:
                to_set['send_notification'] = send_notification

            # Add becode_token to the update
            if send_notification is not None:
                to_set['becode_token'] = becode_token

            # Update the user
            self.db.users.update_one({'_id': user_id}, {'$set': to_set})
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

