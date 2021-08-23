from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
from random import randint
import event_types
import logging


class Client:
    def __init__(self, token: str):
        session = vk_api.VkApi(token=token)
        self.api = session.get_api()
        self.longpoll = VkLongPoll(session)

    def send_message(self, peer_id, text, reply_to=None):
        random_id = randint(1, 9999999999)
        self.api.messages.send(peer_id=peer_id, message=text, random_id=random_id,
                               reply_to=reply_to)


class Bot:
    def __init__(self, token):
        self.logger = logging.getLogger("bot")
        self.me = Client(token)
        self.incoming_message_handlers = []
        self.outgoing_message_handlers = []
        self.every_message_handlers = []
        self.online_handlers = []
        self.offline_handlers = []
        self.read_outgoing_handlers = []

    def polling(self):
        while True:
            try:
                for event in self.me.longpoll.check():
                    self.process_event(event)
            except Exception as e:
                print(e)
                self.logger.error(e)

    def process_event(self, event):
        if event.type == VkEventType.MESSAGE_NEW:
            self.process_message(event)
        elif event.type == VkEventType.USER_ONLINE:
            pass
        elif event.type == VkEventType.USER_OFFLINE:
            pass
        elif event.type == VkEventType.READ_ALL_OUTGOING_MESSAGES:
            pass

    def process_message(self, event):
        message = event_types.Message(self, event)
        message.print()
        self.process_every_message(message)
        if message.from_me:
            self.process_outgoing_message(message)
        else:
            self.process_incoming_message(message)

    def process_incoming_message(self, message):
        for handler in self.incoming_message_handlers:
            filters = handler[1]
            if all([filter(message) for filter in filters]):
                handler[0](message)

    def process_outgoing_message(self, message):
        for handler in self.outgoing_message_handlers:
            filters = handler[1]
            if all([filter(message) for filter in filters]):
                handler[0](message)

    def process_every_message(self, message):
        for handler in self.every_message_handlers:
            filters = handler[1]
            if all([filter(message) for filter in filters]):
                handler[0](message)

    def register_incoming_message_handler(self, handler, filters):
        self.incoming_message_handlers.append([handler, filters])

    def register_outgoing_message_handler(self, handler, filters):
        self.outgoing_message_handlers.append([handler, filters])

    def register_every_message_handler(self, handler, filters):
        self.every_message_handlers.append([handler, filters])

    def register_online_handler(self, handler, filters):
        self.online_handlers.append([handler, filters])

    def register_offline_handler(self, handler, filters):
        self.offline_handlers.append([handler, filters])

    def register_read_outgoing_handler(self, handler, filters):
        self.read_outgoing_handlers.append([handler, filters])

    def incoming_message_handler(self, commands: list = None, func: list = None):
        if func is None:
            func = []
        if commands is None:
            commands = []
        filters = func
        for command in commands:
            filters.append(lambda m: m.text.split()[0] == f".{command}")

        def decorator(callback):
            self.register_incoming_message_handler(callback, filters)
            return callback
        return decorator

    def outgoing_message_handler(self, commands: list = None, func: list = None):
        if func is None:
            func = []
        if commands is None:
            commands = []
        filters = func
        for command in commands:
            filters.append(lambda m: m.text.split()[0] == f".{command}")

        def decorator(callback):
            self.register_outgoing_message_handler(callback, filters)
            return callback
        return decorator

    def every_message_handler(self, commands: list = None, func: list = None):
        if func is None:
            func = []
        if commands is None:
            commands = []
        filters = func
        for command in commands:
            filters.append(lambda m: m.text.split()[0] == f".{command}")

        def decorator(callback):
            self.register_every_message_handler(callback, filters)
            return callback
        return decorator
