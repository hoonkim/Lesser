import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

sys.path.append("../")

from users.usermanager import *
import dockermanager.controller as cont
import dockermanager.configure as conf

from urllib.parse import *
from receiver.lesserjob import *
import time


hostName = "localhost"
hostPort = 9000

lesserJob = LesserJob()

userManager = UserManager()
minionController = cont.MinionController()

def ProtocolToInt(str):
    if str=="GET":
        return 0
    elif str=="POST":
        return 1
    elif str=="PUT":
        return 2
    elif str=="DELETE":
        return 3
    elif str=="OPTION":
        return 4
    elif str=="HEADER":
        return 5
userManager.AppendUser("torisdream","abcdefg","")

class Lesserver(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        parse_result = urlparse(self.path)

        print("client addr", self.client_address)
        print("command", self.command)
        print("request line",self.requestline)

        print("path",parse_result.path)
        print("query",parse_result.query)

        print("query parse", parse_qs(parse_result.query))

        urlPath = parse_result.path
        if urlPath.endswith('/') == False:
            urlPath += '/'

        appName = urlPath.partition('/')[2].rpartition('/')[0]
        user = userManager.searchUser(appName)
        if user is None:
            print("Unavailable User")
            #TODO: Guide move to useradd procedure
            return 0

        abcd = parse_qs(parse_result.query)

        qsDict = dict()
        for key in abcd:
            qsDict[key] = abcd[key][0]
        print(qsDict)

        urlPath = parse_result.path
        if urlPath.endswith('/') == False:
            urlPath += '/'

        appName = urlPath.split('/')[1]
        user = userManager.searchUser(appName)
        if user is None:
            print("Unavailable User", appName)
            #TODO: Guide move to useradd procedure
            return 0

        machine = user.getFirstMachine()
        if machine is None:
            print("No Machine for User:",appName)
            lesser = cont.MinionController()
            test = conf.configObj

            test['lesserId'] = user.GetUsername()

            con = lesser.upLesser(test)

            print ("New Server:",con.Id," port:", con.mongoPort)



            machine = Machine("127.0.0.1", con.Id, int(con.mongoPort))
            user.AddMachine(machine)

        #TODO: Add Machine argument
        lesserJob.add_work(self.client_address[0], self.client_address[1], ProtocolToInt(self.command), parse_result.path, qsDict, "{}" ,machine)


    def do_ (self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        parse_result = urlparse(self.path)
        urlPath = parse_result.path
        
        if urlPath.endswith('/') == False:
            urlPath += '/'

        appName = urlPath.partition('/')[2].rpartition('/')[0]
        user = userManager.searchUser(appName)
        if user == None:
            print("Unavailable User")
            #TODO: Guide move to useradd procedure
            return 0

        machine = user.getFirstMachine()

        if machine is None:
            print("No Machine for User:",appName)
            lesser = cont.MinionController()
            test = conf.configObj

            test['lesserId'] = user.GetUsername()

            con = lesser.upLesser(test)

            print ("New Server:",con.Id)

            machine = Machine("127.0.0.1", con.Id, con.mongoPort)
            user.AddMachine(machine)

        #print("client addr", self.client_address) #{'127.0.0.1', 50286}
        #print("command", self.command) #POST
        #print("request line",self.requestline) #POST /abcd/efgb/aa?bb=cc&dd=ee&ff=gg HTTP/1.1

        #print("path",parse_result.path) #/abcd/efgb/aa
        #print("query",parse_result.query) #bb=cc&dd=ee&ff=gg

        #print("query parse", parse_qs(parse_result.query)) #query jsonbody

        content_length = int(self.headers.get('content-length', 0))  #read header
        #print("content-length:",content_length) #length
        encoded_body = self.rfile.read(content_length)
        #print(type(encoded_body)) #type
        #print(encoded_body.decode('utf-8')) #encode output

        abcd = parse_qs(parse_result.query)

        qsDict = dict()
        for key in abcd:
            qsDict[key] = abcd[key][0]
        print(qsDict)


        lesserJob.add_work(self.client_address[0], self.client_address[1], ProtocolToInt(self.command), parse_result.path, qsDict, encoded_body.decode('utf-8'),machine)



myServer = HTTPServer((hostName, hostPort), Lesserver)
lesserJob.start_work()
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

userManager.loadUser()


try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))