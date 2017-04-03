import hashlib
import requests
import string

domain = 'example.com'
mailgun_api_key = None
send_to = 'someone@example.com'
initialized = False

def init(domain, mailgun_api_key, send_to):
    global_vars = globals()
    global_vars['domain'] = domain
    global_vars['mailgun_api_key'] = mailgun_api_key
    global_vars['send_to'] = send_to
    global initialized
    initialized = True

def senderify(sender):
    if not initialized:
        raise ValueError('must call init first')
    valid_chars = string.ascii_letters + string.digits + '-_'
    max_len = 64 - len('euphoria+')
    sender_addr = ''.join(char for char in sender if char in valid_chars)[:max_len] or hashlib.md5(sender.encode('utf-8')).hexdigest()[:8]
    return '%s (Euphoria) <euphoria+%s@%s>' % (sender, sender_addr, domain)

def mail(sender, message):
    if not initialized:
        raise ValueError('must call init first')
    return requests.post(
            'https://api.mailgun.net/v3/%s/messages' % domain,
            auth=('api', mailgun_api_key),
            data={
                'from': senderify(sender),
                'to': send_to,
                'subject': '%s from %s at Euphoria' % ('Message' if message else 'Ping', sender),
                'text': message or 'Check Euphoria to see what they have to say.'
            })
