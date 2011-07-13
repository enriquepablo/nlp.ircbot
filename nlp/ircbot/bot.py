# -*- coding: utf-8 -*-

import re
import sys
import nl
from twisted.words.protocols import irc
from twisted.internet import protocol
from twisted.internet import reactor
from nlp.ircbot.compiler import yacc
from nlp.ircbot import cmnds

partial_msg = ''
partial = False


class MacarronicBot(irc.IRCClient):


    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)

    def signedOn(self):
        self.join(self.factory.channel)
        print "Signed on as %s." % (self.nickname,)

    def joined(self, channel):
        print "Joined %s." % (channel,)

    def privmsg(self, user, channel, msg):
        if user and self.nickname in msg:
            msg = re.compile(self.nickname + "[:, ]*", re.I).sub('', msg)
            prefix = user.split('!', 1)[0] + ': '
            cmnd = msg.split(':')
            if len(cmnd) == 1:
                resp = yacc.parse(msg)
                if resp is None:
                    resp = 'Do not understand'
            elif len(cmnd) == 2:
                try:
                    fun = getattr(cmnds, cmnd[0])
                except AttributeError:
                    resp = 'Unknown command'
                else:
                    resp = fun(cmnd[1])
            else:
                resp = 'Too many ":"'
            self.msg(self.factory.channel, prefix + resp)

class MacarronicBotFactory(protocol.ClientFactory):
    protocol = MacarronicBot

    def __init__(self, channel, nickname='luis_ricardo'):
        self.channel = channel
        self.nickname = nickname

    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting." % (reason,)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)


def main():
    nick = sys.argv[1]
    chan = sys.argv[2]
    reactor.connectTCP('irc.freenode.net', 6667,
                       MacarronicBotFactory('#' + chan, nickname=nick))
    nl.kb.open(nick)
    reactor.run()


if __name__ == "__main__":
    main()
