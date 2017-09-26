# -*- coding: utf-8 -*-
import logging
import random
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger(__name__)


class Messenger(object):
    def __init__(self, slack_clients):
        self.clients = slack_clients

    def send_message(self, channel_id, msg):
        # in the case of Group and Private channels, RTM channel payload is a complex dictionary
        if isinstance(channel_id, dict):
            channel_id = channel_id['id']
        logger.debug('Sending msg: %s to channel: %s' % (msg, channel_id))
        channel = self.clients.rtm.server.channels.find(channel_id)
        channel.send_message(msg)

    def write_help_message(self, channel_id):
        bot_uid = self.clients.bot_user_id()
        txt = '{}\n{}\n{}\n{}\n\n{}'.format(
            "Hi! I'm Renato! You're friendly Slack bot to help you learn Maltese. I'll *_respond_* to the following commands:\n",
            "> `hi <@" + bot_uid + ">` - I'll respond with a randomized greeting mentioning your user. :wave:\r",
            "> `motd <@" + bot_uid + ">` - I'll reply back with the Maltese word of the day. :flag-mt:\r",
            "> `kantali <@" + bot_uid + ">` - I'll load a suggested song from my very own favourite playlist. :musical_note: \r",
            "Disclaimer: Any resemblance between this bot and any persons, living or dead, is purely unintentional.")
            #"I'm your friendly Slack bot written in Python.  I'll *_respond_* to the following commands:",
            #"> `hi <@" + bot_uid + ">` - I'll respond with a randomized greeting mentioning your user. :wave:",
            #"> `<@" + bot_uid + "> joke` - I'll tell you one of my finest jokes, with a typing pause for effect. :laughing:",
            #"> `<@" + bot_uid + "> attachment` - I'll demo a post with an attachment using the Web API. :paperclip:"
        self.send_message(channel_id, txt)

    def write_greeting(self, channel_id, user_id):
        greetings = ['Hi', 'Hello', 'Nice to meet you', 'Howdy', 'Salutations', 'Bonġu', 'X\'għandna ġisem']
        txt = '{}, <@{}>!'.format(random.choice(greetings), user_id)
        self.send_message(channel_id, txt)

    def write_song(self, channel_id):
        song = ['https://www.youtube.com/watch?v=A-pcwbVl_qc',
           'https://www.youtube.com/watch?v=X5-C1Kx_JNA',
           'https://www.youtube.com/watch?v=Qg_AhuBqQUI',
           'https://www.youtube.com/watch?v=l407bnafnlU']
        txt = '{}'.format(random.choice(song))
        self.send_message(channel_id, txt)

    def write_prompt(self, channel_id):
        bot_uid = self.clients.bot_user_id()
        idiom = ['Toni taghni tina talli taghjtu tuta tajba, talli taghjtu tuta tajba Toni taghni tina.',
           'Dari rari tara re, tara lira tara re.',
           'Ħija tagħni ħawħa u qalli: "Ħa, ħi, ħudha u ħawwilha fil-ħamrija ħamra taħt il-ħitan tà Ħal Għargħur.',
           'Trakk fuq trakk. Trakk taħt trakk.',
           'Ġorġ raġa’ ġà mill-gaġġa tal-ġgant.',
           'Platt fuq platt, platt taħt platt.',
           'Qafas tal-qasab imdendel mas-saqaf.',
           'Patri minn Napli mar Kapri għall-papri; Mela f\'Napli m\'hemmx papri; Biex patri minn Napli mar Kapri għall-papri',
           'Tqaħqaħt tqaħqieqa u t-tqaħqieha li tqaħqaht kienet tqaħqieha kbira.',
           'Il-pespus pespes pespisa lil pespusa tal-pespus u l-pespusa tal-pespus għat-tpespisa tal-pespus, pespset.',
           'Platti ċatti platti fondi, int u tiekol tikkonfondi.']
        txt = '{}'.format(random.choice(idiom))
        self.send_message(channel_id, txt)
        self.clients.send_user_typing_pause(channel_id)
        error = "\rI'm sorry, that means 'I didn't quite understand'... Try this `<@" + bot_uid + "> help`"
        self.send_message(channel_id, error)


    def write_joke(self, channel_id):
        question = "Why did the python cross the road?"
        self.send_message(channel_id, question)
        self.clients.send_user_typing_pause(channel_id)
        answer = "To eat the chicken on the other side! :laughing:"
        self.send_message(channel_id, answer)

    def write_motd2 (self, channel_id, example_phrase):
        attachment = {
            "pretext": "We bring bots to life. :sunglasses: :thumbsup:",
            "title": "Host, deploy and share your bot in seconds.",
            "text": example_phrase,
            "image_url": "https://storage.googleapis.com/beepboophq/_assets/bot-1.22f6fb.png",
            "color": "#7CD197",
        }
        self.clients.web.chat.post_message(channel_id, example_phrase, attachments=[attachment], as_user='true')

    def write_motd(self, channel_id, file, example_phrase):
        txt = "Here is the Maltism of the Day (motd)"
        self.send_message(channel_id, txt)
        self.clients.web.chat.post_image(filename=file, token=slack_token, channels=channel_id)
        self.send_message(channel_id, example_phrase)

    def write_error(self, channel_id, err_msg):
        txt = ":face_with_head_bandage: my maker didn't handle this error very well:\n>```{}```".format(err_msg)
        self.send_message(channel_id, txt)

    def demo_attachment(self, channel_id):
        txt = "Beep Beep Boop is a ridiculously simple hosting platform for your Slackbots."
        attachment = {
            "pretext": "We bring bots to life. :sunglasses: :thumbsup:",
            "title": "Host, deploy and share your bot in seconds.",
            "title_link": "https://beepboophq.com/",
            "text": txt,
            "fallback": txt,
            "image_url": "https://storage.googleapis.com/beepboophq/_assets/bot-1.22f6fb.png",
            "color": "#7CD197",
        }
        self.clients.web.chat.post_message(channel_id, txt, attachments=[attachment], as_user='true')
