
# Imports
from datetime import datetime
from flask import request
from flask_restx import Namespace, Resource, fields
from src.config import config

# API documentation init
namespace = Namespace('settings', description="Bot user settings' API")

# Model for Authentication post
auth_model = namespace.model('Authentication', {
    'public_key': fields.String(description="Public key, given by the bot"),
})

# Model for Settings update
settings_model = namespace.model('Settings update', {
    'public_id': fields.String(description="Public id, send by the /auth route"),
    'becode_token': fields.String(description="Your personal token retrieved on My BeCode"),
    'send_notification': fields.Boolean(description="If you want to receive notifications or not")
})


@namespace.route('/auth')
class Authentication(Resource):

    @namespace.doc(
        body=auth_model,
        responses={
            200: 'Success',
            400: 'Validation Error'
        })
    def post(self):
        """
        Authenticate the API and get user details.
        Return a JSON object with the user credentials.
        """

        # Check if a non-empty JSON was been send
        if content := request.get_json():

            # Check if an auth_key was been send
            if public_key := content['public_key']:

                # Retrieve the user data from the auth key
                user_data = config.db.get_data_from_public_key(public_key)

                return user_data


@namespace.route('/update')
class UpdateSettings(Resource):

    @namespace.doc(
        body=settings_model,
        responses={
            200: 'Success',
            400: 'Validation Error'
        })
    def post(self):
        """
        Update the user details
        """

        # Check if a non-empty JSON was been send
        if content := request.get_json():

            # Check if an public_id was been send
            if public_id := content['public_id']:

                # Retrieve the date included in the public_key
                raw_date: str = public_id.split(".")[1]
                date = datetime.strptime(raw_date, "%Y%m%d%H%M%S")

                # Check if the date is valid
                if datetime.now() < date:
                    config.db.update({'public_id': public_id},
                                     send_notification=content['send_notification'],
                                     becode_token=content['becode_token'])

                    # Return a success status message
                    return {
                        'status': True,
                        'message': 'User settings were correctly updated'
                    }

        # Return an error status message
        return {
            'status': False,
            'message': 'An error occurred during the update of the user settings'
        }, 400
