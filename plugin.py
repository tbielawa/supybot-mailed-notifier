###
# Copyright (c) 2009, Ricky Zhou
# All rights reserved.
#
#
###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import supybot.world as world
import supybot.ircmsgs as ircmsgs
import threading
import SocketServer
import select

class NotifyServerHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        try:
            while 1:
                line = self.rfile.readline()
                if not line:
                    break
                line = line.strip()
                (channel, text) = line.split(' ', 1)
                if not channel or not text:
                    continue
                if self.server.channel_states.get(channel, "on") == "on":
                    msg = ircmsgs.privmsg(channel, text)
                    for irc in world.ircs:
                        if channel in irc.state.channels:
                            irc.queueMsg(msg)
        except:
            pass

class StoppableThreadingTCPServer(SocketServer.ThreadingTCPServer):
    '''ThreadingTCPServer with shutdown capability copied from Python SVN'''
    def __init__(self, server_address, RequestHandlerClass):
        SocketServer.ThreadingTCPServer.__init__(self, server_address, RequestHandlerClass)
        self.__is_shut_down = threading.Event()
        self.__serving = False

    def serve_forever(self, poll_interval=0.5):
        """Handle one request at a time until shutdown.

        Polls for shutdown every poll_interval seconds. Ignores
        self.timeout. If you need to do periodic tasks, do them in
        another thread.
        """
        self.__serving = True
        self.__is_shut_down.clear()
        while self.__serving:
            # XXX: Consider using another file descriptor or
            # connecting to the socket to wake this up instead of
            # polling. Polling reduces our responsiveness to a
            # shutdown request and wastes cpu at all other times.
            r, w, e = select.select([self], [], [], poll_interval)
            if r:
                self._handle_request_noblock()
        self.__is_shut_down.set()

    def shutdown(self):
        """Stops the serve_forever loop.

        Blocks until the loop has finished. This must be called while
        serve_forever() is running in another thread, or it will
        deadlock.
        """
        self.__serving = False
        self.__is_shut_down.wait()

    def _handle_request_noblock(self):
        """Handle one request, without blocking.

        I assume that select.select has returned that the socket is
        readable before this function was called, so there should be
        no risk of blocking in get_request().
        """
        try:
            request, client_address = self.get_request()
        except socket.error:
            return
        if self.verify_request(request, client_address):
            try:
                self.process_request(request, client_address)
            except:
                self.handle_error(request, client_address)
                self.close_request(request)

class NotifyServer(StoppableThreadingTCPServer):
    def __init__(self, server_address, RequestHandlerClass):
        StoppableThreadingTCPServer.__init__(self, server_address, RequestHandlerClass)
        self.channel_states = {}

class Notify(callbacks.Plugin):
    """This plugin relays messages passed to its TCP server to an IRC channel."""
    threaded = True
    def __init__(self, irc):
        self.__parent = super(Notify, self)
        self.__parent.__init__(irc)
        self.host = self.registryValue('server_address')
        self.port = self.registryValue('server_port')
        self.server = NotifyServer((self.host, self.port), NotifyServerHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.setDaemon(True)
        self.server_thread.start()

    def notifications(self, irc, msg, args, channel, state):
        print channel
        if state is None:
            irc.reply("Notifications for %s: %s" % (channel,
                self.server.channel_states.get(channel, "on")))
        else:
            if state:
                self.server.channel_states[channel] = "on"
            else:
                self.server.channel_states[channel] = "off"

    notifications = wrap(notifications, ['inChannel', optional('boolean')])

    def die(self):
        self.server.shutdown()
        self.server.server_close()
        self.__parent.die()

Class = Notify


# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
