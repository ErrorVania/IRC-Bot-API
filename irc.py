import socket, threading

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
        self.run()


    def send():
        self.ircsock.send(bytes("PRIVMSG " + self.channel + " :" + self.message + "\n","UTF-8"))


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
                print("[!] [" + name + "] changed name to: " + chunk[2][1:])
            elif chunk[1] == "JOIN":
                raw = chunk[0]
                name = raw[raw.find(":")+1:raw.find("!")]
                print("[!] [" + name + "] joined channel: " + chunk[2][1:])
            elif chunk[1] == "PART":
                raw = chunk[0]
                name = raw[raw.find(":")+1:raw.find("!")]
                print("[!] [" + name + "] left the channel: " + chunk[2][1:])
            elif chunk[1] == "QUIT":
                raw = chunk[0]
                name = raw[raw.find(":")+1:raw.find("!")]
                print("[!] [" + name + "] disconnected: " + chunk[2][1:])

            elif chunk[1] == 'PRIVMSG':

                if chunk[2] == self.channel:
            
                    first = chunk[0]
                    chunk.remove(chunk[0])
                    chunk.remove(chunk[1])
                    chunk.remove("PRIVMSG")

                    name = first[first.find(":")+1:first.find("!")]
                    print("<" +  name + "> " + " ".join(chunk)[1:])





                    #commands start here, chunk[0] will be the first word
                    if chunk[0] == ":!" + self.exitcode and name == self.admin:
                        self.ircsock.close()

            else:
                print(str(chunk)) #print unknown commands
    


    



bot1 = IRC_Bot("chat.freenode.net",6667,"pybotAAA","##bot-testing","botadmin")
