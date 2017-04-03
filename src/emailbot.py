#Standard library modules
import sys
import threading

import re
import time
import datetime
import traceback

#Additional modules
import euphoria as eu
from emailbot.euphutils import EuphUtils

#Project modules
import emailbot.mailer as mailer
import emailbot.logger as logger
import emailbot.longmessage_room as longmessage_room
from emailbot.botcollection import BotCollection

log = logger.Logger()

class EmailBot(eu.ping_room.PingRoom, eu.chat_room.ChatRoom, longmessage_room.LongMessageRoom):
    def __init__(self, room_name, password, nickname, for_user, help_text="", short_help_text=""):
        super().__init__(room_name, password)

        self.room_name = room_name.lower()
        self.nickname = nickname
        self.password = password

        self.help_text = help_text
        self.short_help_text = short_help_text
        self.for_user = for_user

        self.start_time = time.time()

        self.bots = BotCollection(self)
        self.botthread = threading.Thread(target=self.bots.run)

        self.initialized = False

    def init(self):
        log.write(EuphUtils.mention(self.nickname) + ' has started.')

    def ready(self):
        super().ready()
        if not self.initialized:
            self.initialized = True
            self.init()

    def run(self):
        self.botthread.start()
        super().run()

    def handle_chat(self, message):
        if message.get('truncated'):
            return
        if message['content'].startswith('!'):
            command = message['content'][1:]
            sender = message['sender']['name']
            msg_id = message['id']
            # !ping [@nickname]
            match = (EuphUtils.command('ping', '').match(command)
                     or EuphUtils.command('ping', self.nickname).match(command))
            if match:
                self.send_chat('Pong!', msg_id)
                return
            # !uptime @nickname
            match = EuphUtils.command('uptime', self.nickname).match(command)
            if match:
                self.send_chat(EuphUtils.uptime_str(self.start_time), msg_id)
                return
            # !help
            match = EuphUtils.command('help', '').match(command)
            if match:
                self.send_chat(self.short_help_text, msg_id)
                return
            # !help @nickname
            match = EuphUtils.command('help', self.nickname).match(command)
            if match:
                self.send_chat(self.help_text, msg_id)
                return
            # !email {@nickname, @for_user}
            match = (EuphUtils.command('email', self.nickname).match(command)
                     or EuphUtils.command('email', self.for_user).match(command))
            if match:
                if mailer.mail(sender, match.group(1)):
                    self.send_chat('Email sent!', msg_id)
                else:
                    self.send_chat('Sorry, email failed to send. Please try again later.', msg_id)
            # !join @nickname
            match = EuphUtils.command('join', self.nickname).match(command)
            if match:
                match = re.match(r'&(\S+)', match.group(1))
                if match:
                    room_name = match.group(1).lower()
                    if room_name == self.room_name:
                        self.send_chat('I\'m already here!', msg_id)
                    else:
                        try:
                            self.bots.create(room_name)
                            self.send_chat('I\'ve made a clone of myself and put it in &%s.' % room_name, msg_id)
                        except ValueError:
                            self.send_chat('I\'m already in &%s!' % room_name, msg_id)
                else:
                    self.send_chat('To add me to a room, use "!join %s &room".' % EuphUtils.mention(self.nickname), msg_id)
                return
            # !leave @nickname
            match = EuphUtils.command('leave', self.nickname).match(command)
            if match:
                self.send_chat('I can\'t leave this room because &%s is my primary room. Sorry.\n'
                               'If you\'d like me to move elsewhere, send @for_user a message. Perhaps through this bot!' % self.room_name, msg_id)
            # !restart @nickname
            match = EuphUtils.command('restart', self.nickname).match(command)
            if match:
                self.send_chat('/me is restarting...', msg_id)
                self.quit()

    def quit(self):
        super().quit()
        self.bots.quit()
        self.botthread.join()
