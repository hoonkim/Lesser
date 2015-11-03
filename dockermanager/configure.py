__author__ = 'dejawa'

host = '175.126.105.125' #server ip
port = '22375'           #server docker port


clientPort = '80'     #example of lesser client port in docker image
mongoPort = '27017'   #example of mongo port in docker image

path = '/'  #disk, mem info location path

diskLimit = 3 * 1000 * 1024 * 1024 # 3GB m
memLimit = 1 * 1000 *1024 * 1024 # 1GB

configObj = {
    "image":"dejawa/lesser",
    "command":None,
    "hostname":None,
    "user":None,        #user id
    "detach":False,
    "stdin_open":False,
    "tty":False,
    "mongoport":None,        #port : [80, 27017]
    "lesserport":None,
    "env":None,
    "volumes":None,
    "volumes_from":None,
    "name":None,
    "entrypoint":None,
    "working_dir":None,
    "labels":{'lesserId':None},
    "host_config":None
    }

class Info :
    mongoPort = ''
    clientPort =''
    Id = ''


