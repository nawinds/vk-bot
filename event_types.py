class Event:
    def __init__(self, bot, event):
        self.bot = bot
        self.message = event.message

        self.raw = event.raw

        self.from_user: bool = event.from_user
        self.from_chat: bool = event.from_chat
        self.from_group: bool = event.from_group
        self.from_me: bool = event.from_me
        self.to_me: bool = event.to_me

        self.attachments: dict = event.attachments
        self.message_data = event.message_data

        self.message_id: int = event.message_id
        self.timestamp: int = event.timestamp
        self.datetime = event.datetime
        self.peer_id: int = event.peer_id
        self.flags: int = event.flags
        self.extra = event.extra
        self.extra_values = event.extra_values
        self.type_id = event.type_id


class Message(Event):
    def __init__(self, bot, event):
        super().__init__(bot, event)

        self.__delattr__("raw")
        self.__delattr__("message_data")
        self.__delattr__("extra")
        self.__delattr__("extra_values")
        self.__delattr__("type_id")

        self.__delattr__("message")
        self.text = event.message
        self.__delattr__("message_id")
        self.id = event.message_id

    def print(self):
        print("----- MESSAGE -----")
        print(f"text: {self.text}")
        print(f"from user: {self.from_user}")
        print(f"from chat: {self.from_chat}")
        print(f"from group: {self.from_group}")
        print(f"from me: {self.from_me}")
        print(f"to me: {self.to_me}")
        print(f"attachments: {self.attachments}")
        print(f"id: {self.id}")
        print(f"timestamp: {self.timestamp}")
        print(f"peer id: {self.peer_id}")
        print(f"flags: {self.flags}")
        print("----- END -----")
        print()

    def delete(self):
        self.bot.me.api.messages.delete(peer_id=self.peer_id, message_ids=self.id)

    def edit(self, text):
        self.bot.me.api.messages.edit(peer_id=self.peer_id, message_id=self.id, message=text)

    def reply(self, text):
        self.bot.me.send_message(self.peer_id, text, reply_to=self.id)
