import sys
import re
import json
import argparse

import euphoria as eu

import emailbot.mailer as mailer
from emailbot.emailbot import EmailBot
from emailbot.euphutils import EuphUtils

room_name = 'testing'
password = None
nickname = None
for_user = None

help_text = '''\
@nickname will email @for_user if you have something to say.
"!email @for_user [message]" or "!email @nickname [message]" to send a message.
"!join @nickname &[room]" will clone me to another room, and "!leave @nickname" will make me leave the room.\
'''

short_help_text = '''\
@nickname will email @for_user if you have something to say.\
'''

def main():
    emailbot = EmailBot(room_name, password, nickname, for_user, help_text=help_text, short_help_text=short_help_text)
    eu.executable.start(emailbot)

def get_args():
    parser = argparse.ArgumentParser(prog='emailbot', description='A notifier bot for Euphoria.', epilog='For details, read the README.md file at https://github.com/ArkaneMoose/EmailBot/blob/master/README.md')
    parser.add_argument('config-file', help='path to a JSON configuration file')
    parser.add_argument('-r', '--room', help='primary room in Euphoria where the bot should reside')
    parser.add_argument('-p', '--password', help='password for room if necessary')
    parser.add_argument('-n', '--nickname', help='custom nickname for the bot')
    parser.add_argument('-u', '--for-user', help='custom nickname to whom the bot is sending messages')
    return parser.parse_args()

if __name__ == '__main__':
    args = vars(get_args())
    with open(args.get('config-file')) as f:
        config = json.load(f)
    try:
        mailer.init(config['domain'], config['mailgunApiKey'], config['sendTo'])
    except KeyError as e:
        raise ValueError('invalid configuration') from e
    room_name = args['room'] or config.get('room', room_name)
    password = args['password'] or config.get('password', password)
    nickname = args['nickname'] or config.get('nickname', nickname)
    for_user = args.get('for-user') or config.get('forUser', for_user)
    help_text = config.get('helpText', help_text.replace('@nickname', EuphUtils.mention(nickname)).replace('@for_user', EuphUtils.mention(for_user)))
    short_help_text = config.get('shortHelpText', short_help_text.replace('@nickname', EuphUtils.mention(nickname)).replace('@for_user', EuphUtils.mention(for_user)))
    main()
