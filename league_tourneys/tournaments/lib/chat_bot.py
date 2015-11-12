import logging
import sleekxmpp
import dns


username    = "chabons"
password    = "asdl;kas;dlk"

class ChatBot():    

    def __init__(self):
        """Attempts to connect to the XMPP server"""

        #XMPP
        self.xmpp                       = sleekxmpp.ClientXMPP(username+"@pvp.net/xiff", "AIR_"+password)

        #Server
        self.server                     = 'chat.%REGION%.lol.riotgames.com'
        self.regions                    = {"BR":"br", "EUN": "eun1",
                                           "EUW": "euw1", "NA": "na1",
                                           "KR": "kr", "OCE": "oc1",
                                           "RU": "ru", "TR": "tr",
                                           "LAN": "la1"}
        self.port                       = 5223
        self.region                     = "NA"


        serverIp = dns.resolver.query(self.server.replace("%REGION%", self.regions[self.region.upper()]))
        print(serverIp[0])
        if serverIp:
            if self.xmpp.connect((str(serverIp[0]), self.port), use_ssl=True):
                self.xmpp.process(block=False)
                self.xmpp.register_plugin("xep_0199") #Ping plugin
                self.xmpp.register_plugin("xep_0045") #MUC
                print("Connection with the server established.")
                return True
            else:
                print("Couldn't resolve the server's A record.\nAn update may be required to continue using this.")
                sys.exit(-1)
        else:
            print("Couldn't resolve the server's A record.\nAn update may be required to continue using this.")
            sys.exit(-1)

    def message(self, to, message, newline=True):
        """Sends a message to the specified person"""

        if newline:
            message = "~\n"+message
        mtype = "chat"
        if str(to)[2:3] == "~":
            mtype = "groupchat"
            to    = to[0:to.find("/")]
        self.xmpp.send_message(mto=str(to), mbody=str(message), mtype=mtype)

if __name__ == '__main__':
    bot = ChatBot()
    bot.message("tweaks","Chat bot!!")
