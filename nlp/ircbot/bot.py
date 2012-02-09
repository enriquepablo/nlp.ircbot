# -*- coding: utf-8 -*-

import re
import sys
from collections import defaultdict
from twisted.words.protocols import irc
from twisted.internet import protocol
from twisted.internet import reactor
import nl

partial_msg = ''
partial = False


class MacarronicBot(irc.IRCClient):

    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)

    def signedOn(self):
        self.nl_buff = defaultdict(str)
        self.join(self.factory.channel)
        print "Signed on as %s." % (self.nickname,)

    def joined(self, channel):
        print "Joined %s." % (channel,)

    def privmsg(self, user, channel, msg):
        if user and self.nickname in msg:
            msg = re.compile(self.nickname + "[:, ]*", re.I).sub('', msg)
            other = user.split('!', 1)[0]
            prefix = other + ': '
            msg = msg.strip()
            self.nl_buff[other] += ' ' + msg
            if self.nl_buff[other][-1] in ('.', '?'):
                resp = nl.yacc.parse(self.nl_buff[other])
                self.nl_buff[other] = ''
            else:
                resp = '...'
            if resp is None:
                resp = 'Do not understand'
            self.msg(self.factory.channel, prefix + str(resp))


class MacarronicBotFactory(protocol.ClientFactory):
    protocol = MacarronicBot

    def __init__(self, name, channel, nickname):
        self.name = name
        self.channel = channel
        self.nickname = nickname

    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting." % (reason,)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)


def main():
    try:
        name = sys.argv[1]
    except IndexError:
        name = 'test'
    nick = name + '_bot'
    chan = 'nlpbot_' + name
    reactor.connectTCP('irc.freenode.net', 6667,
                       MacarronicBotFactory(name, '#' + chan, nick))
    nl.kb.open_kb(name)
    reactor.run()


if __name__ == "__main__":
    main()
