class Broadcast:

    """
    Handles EventDispatcher instances.  Serves as a service locator.
    EventDispatchers are registered by opening channels.  If a channel is
    opened multiple times (e.g., by subsequent scenes), they are put onto the
    stack for that channel.  Closing a channel removes the top dispatcher.

    Scenes that need a local channel should open/close it properly.  Any global
    channels should be opened at the top level, or by preceding scenes.
    Channels can be referenced for listening/speaking like a dictionary.

    ::

        >>> from pyglet.event import EventDispatcher
        >>> b = Broadcast()
        >>> b.open('channel', EventDispatcher())
        >>> isinstance(b['channel'], EventDispatcher)
        True

    """

    def __init__(self):
        self.channels = {}

    def __getitem__(self, key):
        return self.channels[key][-1]

    def open(self, channel, dispatcher):
        try:
            a = self.channels[channel]
        except KeyError:
            self.channels[channel] = [dispatcher]
        else:
            a.append(dispatcher)

    def close(self, channel):
        try:
            a = self.channels[channel]
        except KeyError:
            pass
        else:
            a.pop()
            if len(a) < 1:
                del self.channels[channel]
