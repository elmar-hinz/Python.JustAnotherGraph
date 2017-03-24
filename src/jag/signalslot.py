from collections import defaultdict


class SignalSlot:
    def __init__(self):
        self._slots = defaultdict(list)

    def slot(self, name, method):
        """Registry of methods (slots) to be triggered by signals.
        
        :param name: Name of the signal to subscribe to. 
        :param method: The method to be triggered.
        :return: 
        """
        self._slots[name].append(method)

    def signal(self, name, *args, **kwargs):
        """Trigger all methods (slots) registered for the signal.
        
        :param name: Name of the signal to send. 
        :param args: Arguments to be inserted into the slots.
        :param kwargs: Keyword arguments to be inserted into the slots.
        :return: 
        """
        for method in self._slots[name]:
            method(*args, **kwargs)
