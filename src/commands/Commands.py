
from src import config
from src.web.becode import AttendanceRequest, Locations

import re
from typing import Union
from discord import Reaction, User, Member


class Commands:

    def __init__(self) -> None:
        pass

    def initialize(self):

        @config.discord.event
        async def on_ready():
            print(f'[+] Discord.py: {config.discord.user} has connected to Discord!')

        @config.discord.command(name="adduser", pass_context=True)
        async def add_user(context) -> None:
            """User command to activate mentions on appointment reminders."""

            # Retrieve the user
            mention: str = context.message.author.mention
            author: int = self.get_author_id(mention)

            # Update the database
            config.db.update(author, send_notification=True)

            # Log and send a confirmation to user
            print(f"[!] Mention added: {author} will receive mentions on reminders.")
            await context.send(f"{mention} Tu n'as plus besoin de ton cerveau, je te mentionnerai à chaque pointage !")

        @config.discord.command(name="removeuser", pass_context=True)
        async def remove_user(context) -> None:
            """User command to deactivate mentions on appointment reminders."""

            # Retrieve the user
            mention: str = context.message.author.mention
            author: int = self.get_author_id(mention)

            # Update the database
            config.db.update(author, send_notification=False)

            # Log and send a confirmation to user
            print(f"[!] Mention added: {author} will stop receiving mentions on reminders.")
            await context.send(f"{mention} L'oiseau prend son envol ! Je ne te mentionnerai plus les pointages.")

        @config.discord.command(name="addtoken", pass_contexr=True)
        async def add_token(context, token: str) -> None:
            """User command to add its token to the database."""

            # Retrieve the user
            mention: str = context.message.author.mention
            author: int = self.get_author_id(mention)

            if len(token) > 1:

                # Update the database
                config.db.update(author, becode_token=token)

                # Log and send a confirmation to user
                print(f"[!] Token added: {author} added token: {token}")
                await context.send(f"{mention}, le token '{token}' a bien été ajouté")

            else:
                await context.send(f"{mention}, ton token n'est pas valide.")

        @config.discord.event
        async def on_reaction_add(reaction: Reaction, user: Union[User, Member]):
            """Event triggered when a user click a reaction to send an attendance to Becode."""

            if reaction.message.id == config.last_message and not user.bot:
                location = None

                # Emoji: House
                if str(reaction.emoji == "\U0001F3E0"):
                    location = Locations.HOME

                # Emoji: City
                elif str(reaction.emoji == "\U0001F307"):
                    location = Locations.BECODE

                if location:
                    print("[!] User added reaction.")

                    # Retrieve the token from the database
                    mention: str = user.mention
                    author: int = self.get_author_id(mention)

                    # Retrieve the token and check if it's not None
                    if token := config.db.get_token(author):
                        print(token)

                        # Send an attendance request to Becode
                        if config.last_attendance:

                            # Init and send the request
                            attendance = config.last_attendance
                            request = AttendanceRequest(attendance, location, token)

                            request.start()
                            request.join()

                            if request.get_status():

                                print(f"[!] Attendance was correctly send for {author}.")
                                await user.send(f"{mention} J'ai bien pointé pour toi sur Becode !")

                            else:
                                print(f"[!] Attendance was NOT correctly send for {author}.")
                                await user.send(f"{mention} OUPS ! Une **erreur** s'est produite... Passe par https://my.becode.org pour pointer.")

                    else:
                        print(f"[!] Missing token for {author}.")
                        await user.send(f"{mention} OUPS ! Une **erreur** s'est produite: Je n'ai pas trouvé ton token... Ajoute un token avec la commande **!addtoken**.")

        return self

    @staticmethod
    def start() -> None:
        config.discord.run(config.DISCORD_TOKEN)

    @staticmethod
    def get_author_id(mention) -> int:
        return int(re.sub(r'[<>!@]', '', mention))
