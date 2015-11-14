import sys
from http.server import BaseHTTPRequestHandler, HTTPServer, urllib
from bson import json_util
import pymongo

sys.path.append("../")

from users.usermanager import *
import dockermanager.controller as cont
import dockermanager.configure as conf

from urllib.parse import *
from receiver.lesserjob import *
import time


hostName = "175.126.105.125"
#hostName = "localhost"
hostPort = 8080

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
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        parse_result = urlparse(self.path)

        print("client addr", self.client_address)
        print("command", self.command)
        print("request line",self.requestline)

        print("path",parse_result.path)
        print("query",parse_result.query)

        print("query parse", parse_qs(parse_result.query))

        urlPath = parse_url(parse_result.path)

        if len(urlPath) is 0 :
            ret = {
                "status" : "ok", "request" : "GET"
            }
            self.wfile.write(json.dumps(ret).encode('utf-8'))
            return

        appName = urlPath[0]

        scheme = ".".join(urlPath[1:])
        print("scheme :", scheme )

        user = userManager.searchUser(appName)
        if user is None:
            print("Unavailable User")
            #TODO: Guide move to useradd procedure
            return 0

        print(parse_result.query)

        abcd = parse_qs(parse_result.query, True)

        qsDict = dict()
        seDict = dict()

        for key in abcd:
            for value in abcd[key]:
                if value is '':
                    if "<=" in key :
                        qsDict[key.split('<-')[0]] = {"$lte" : int(key.split('<-')[1])}
                    elif "<" in key :
                        qsDict[ key.split('<')[0]] = {"$lt" : int(key.split('<')[1])}
                    elif ">" in key :
                        qsDict[key.split('>')[0]] = {"$gt" : int(key.split('>')[1])}
                    elif ">=" in key :
                        qsDict[key.split('>-')[0]] = {"$gte" : int(key.split('>-')[1])}
                    else :
                        seDict[key] = 1

                else :
                    if value.isdigit():
                        qsDict[key] = int(value)
                    elif value.replace('.', '', 1).isdigit():
                        qsDict[key] = float(value)
                    else :
                        qsDict[key] = value

        print(qsDict)
        print(seDict)

        machine = user.getFirstMachine()
        if machine is None:
            print("No Machine for User:",appName, ". Docker creation starts.")
            lesser = cont.MinionController()
            test = conf.configObj

            test['lesserId'] = user.GetUsername()

            mem = lesser.memInfo()
            disk = lesser.diskInfo()

            print("Space Total : ", disk['total'], ", Used : ", disk['used'])
            if disk['threshhold'] :
                print("Need more space. Docker creation failed.")
                return

            else :
                print("Space is enough")

            print("Mem Total : ", mem['total'], ", Used : ", mem['used'])
            if mem['threshhold'] :
                print("Need more Memory. Docker creation failed.")
                return

            else :
                print("Memory is enough")


            con = lesser.upLesser(test)

            print ("New Server:",con.Id,"\nport:", con.mongoPort)

            machine = Machine("127.0.0.1", con.Id, int(con.mongoPort))
            #machine = Machine("127.0.0.1", user.GetUsername() , 27017)

            user.AddMachine(machine)
            user.setBridge(Bridge(machine))

        print(parse_result.path)


        #TODO: Add Machine argument
        #lesserJob.add_work(self.client_address[0], self.client_address[1], ProtocolToInt(self.command), parse_result.path, qsDict, "{}" ,machine)

        ret = {}
        try:
            #db = MongoClient(machine.addr, machine.port)
            bridge = user.getBridge()
            if len(seDict) is 0:
                data = json_util.dumps(bridge.application(appName).schema(scheme).find(qsDict))
            else :
                data = json_util.dumps(bridge.application(appName).schema(scheme).find(qsDict, seDict))

        except ConnectionError:
            ret['error'] = "Connection Error"
        except pymongo.errors.CollectionInvalid :
            ret['error'] = "Wrong type of collection"

        self.wfile.write(data.encode("utf-8"))



    def do_POST (self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        parse_result = urlparse(self.path)
        urlPath = parse_url(parse_result.path)

        if len(urlPath) is 0 :
            ret = {
                "status" : "ok", "request" : "POST"
            }
            self.wfile.write(json.dumps(ret).encode('utf-8'))
            return

        appName = urlPath[0]
        scheme = ".".join(urlPath[1:])

        user = userManager.searchUser(appName)
        print(appName)
        print(urlPath)
        if user is None:
            print("Unavailable User")
            #TODO: Guide move to useradd procedure
            return 0

        machine = user.getFirstMachine()

        if machine is None:
            print("No Machine for User:",appName)
            lesser = cont.MinionController()
            test = conf.configObj

            test['lesserId'] = user.GetUsername()

            mem = lesser.memInfo()
            disk = lesser.diskInfo()

            print("Space Total : ", disk['total'], ", Used : ", disk['used'])
            if disk['threshhold'] :
                print("Need more space. Docker creation failed.")
                return

            else :
                print("Space is enough")

            print("Mem Total : ", mem['total'], ", Used : ", mem['used'])
            if mem['threshhold'] :
                print("Need more Memory. Docker creation failed.")
                return

            else :
                print("Memory is enough")

            con = lesser.upLesser(test)



            print ("New Server:",con.Id,"\nport:", con.mongoPort)

            machine = Machine("127.0.0.1", con.Id, int(con.mongoPort))
            #machine = Machine("127.0.0.1", user.GetUsername() , 27017)
            user.AddMachine(machine)
            user.setBridge(Bridge(machine))


        content_length = int(self.headers.get('content-length', 0))  #read header
        #print("content-length:",content_length) #length

        body =  self.rfile.read(content_length)
        encoded_body = body.decode('utf-8')
        print(type(encoded_body)) #type

        ret = {'result' : 'Error'}

        try:
            data = parse_body(encoded_body)

            print(type(data))
            print(data)
            print("scheme : ", scheme)

            #Create Bridge here.
            bridge = user.getBridge()
            bridge.application(appName).schema(scheme).insert(data)


        except ConnectionError:
            ret['error'] = "Connection Error"
        except pymongo.errors.CollectionInvalid :
            ret['error'] = "Wrong type of collection"
        except ValueError :
            ret['error'] = "Wrong formatted Json!"
        else :
            ret['result'] = "Success"

        response = json.dumps(ret)

        self.wfile.write(response.encode("utf-8"))

        #lesserJob.add_work(self.client_address[0], self.client_address[1], ProtocolToInt(self.command), parse_result.path, qsDict, encoded_body.decode('utf-8'),machine)



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
