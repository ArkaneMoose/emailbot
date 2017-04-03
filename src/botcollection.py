from emailbot.euphutils import EuphUtils
from emailbot.secondarybot import SecondaryEmailBot

import euphoria as eu
import threading

class BotCollection(eu.execgroup.ExecGroup):
    def __init__(self, emailbot):
        super().__init__(autostop=False)

        self.parent = emailbot
        self.bots = {emailbot.room_name: emailbot}

    def remove(self, bot):
        self.bots.pop(bot.room_name, None)
        try:
            self.execs.remove(bot)
        except ValueError:
            pass

    def create(self, room_name):
        if room_name in self.bots:
            raise ValueError('bot already exists in &%s' % room_name)
        bot = SecondaryEmailBot(room_name, self)
        self.bots[room_name] = bot
        self.add(bot)
        return bot
