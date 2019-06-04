class StatusManager:
    """
    Class for managing turn status messages.
    """

    def __init__(self):
        self.message = None

    def register_message(self, message: str):
        """
        Sets current status message.
        :param message:
            New message
        """
        self.message = message

    def get_status_message(self):
        """
        Returns current status message.
        :return:
            Current status message
        """
        return self.message

    def get_status_message_and_reset(self):
        """
        Returns current status message and sets it to None.
        :return:
            Current status message
        """
        msg = self.message
        self.message = None
        return msg
