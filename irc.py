import socket, threading, importlib
import handler



class IRC_Bot(threading.Thread):
    def __init__(self, server,port,name,channel,admin,exitcode="bye"):
        threading.Thread.__init__(self)
        self.server = server
        self.port = port
        self.name = name
        self.channel = channel
        self.admin = admin
        self.exitcode = exitcode
        self.ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        



        conntuple = (self.server,self.port)
        botnick = self.name

        self.ircsock.connect(conntuple)
        self.ircsock.send(bytes("USER " + botnick + " " + botnick + " " + botnick + " " + botnick + "\n","UTF-8"))
        self.ircsock.send(bytes("NICK " + botnick + "\n","UTF-8"))
        self.ircsock.send(bytes("JOIN " + self.channel + "\n","UTF-8"))
        

        print("[*] Searching for 'End of /NAMES list'...")
        ircmsg = ""
        while ircmsg.find("End of /NAMES list") == -1:
            ircmsg = self.ircsock.recv(2048).decode("UTF-8").strip('\n\r')
        print("[*] Successfully started bot: " + botnick)


        while 1 and not self.ircsock._closed:
            ircmsg = self.ircsock.recv(2048).decode("UTF-8").strip('\n\r')
            chunk = ircmsg.split(' ')


            if chunk[0] == "PING":
                self.ircsock.send(bytes('PONG :%s\r\n' % (chunk[1]), 'UTF-8'))
                print("PONGED: " + chunk[1])
            elif chunk[1] == "NICK":
                raw = chunk[0]
                name = raw[raw.find(":")+1:raw.find("!")]
                print("[!] [" + name + "] changed name to: " + " ".join(chunk[2:])[1:])
            elif chunk[1] == "JOIN":
                raw = chunk[0]
                name = raw[raw.find(":")+1:raw.find("!")]
                print("[!] [" + name + "] joined channel: " + " ".join(chunk[2:])[1:])
            elif chunk[1] == "PART":
                raw = chunk[0]
                name = raw[raw.find(":")+1:raw.find("!")]
                print("[!] [" + name + "] left the channel: " + " ".join(chunk[2:])[1:])
            elif chunk[1] == "QUIT":
                raw = chunk[0]
                name = raw[raw.find(":")+1:raw.find("!")]
                print("[!] [" + name + "] disconnected: " + " ".join(chunk[2:])[1:])

            elif chunk[1] == "PRIVMSG":
                try:
                    importlib.reload(handler)
                    handler.handle(chunk, chunk[2], self.name, self.ircsock, self.exitcode, self.admin)
                except Exception as e:
                    pass
            else:
                print(str(chunk)) #print unknown commands

bot1 = IRC_Bot("chat.freenode.net",6667,"pybot010101","##bot-testing","botadmin")
bot1.start()








while 1:
    a = input("")
    bot1.ircsock.send(bytes("PRIVMSG " + bot1.channel + " :" + a + "\n","UTF-8"))
