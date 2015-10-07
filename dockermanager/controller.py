__author__ = 'dejawa'
from docker import Client
import dockermanager.configure as conf
import json

class MinionController:

    conn = Client(base_url=conf.host+':'+conf.port)


#docker mongo db image create/start/stop/replset/sharding

    def getAllContainers(self):
        return self.conn.containers(all=True)

    def getUserContainers(self):
        #return self.conn.containers(all="true",filters=[{"label":"${userid}"}])
        return self.conn.containers(all="true")

    def isContainerRunning(self , Id):
        status = self.conn.inspect_container(Id)['State']
        if status['Running'] :
            return True
        return False
        # if status['']


    def createLesser(self, info):
        obj = conf.configObj
        mongo={}
        lesser={}

        if info['lesserId'] :
            obj['labels']['lesserId'] = info['lesserId']

        if info['command'] :
            obj['command'] = info['command']

        if info['env'] :
            obj['env'] = info['env']

        if info['name'] :
            obj['name'] = info['name']

        if info['entrypoint'] :
            obj['entrypoint'] = info['entrypoint']

        if info['working_dir'] :
            obj['working_dir'] = info['working_dir']


        # if info['mongo'] :
        #     mongo = {info['mongo']:('0.0.0.0',conf.mongoPort)}
        # if info['lesser'] :
        #     lesser = {info['lesser']:('0.0.0.0',conf.lesserPort)}

        container = self.conn.create_container(
            image=obj['image'],
            command=obj['command'],
            ports=[conf.mongoPort, conf.clientPort],
            environment=obj['env'],
            volumes=obj['volumes'],
            volumes_from=obj['volumes_from'],
            name=obj['name'],
            entrypoint=obj['entrypoint'],
            working_dir=obj['working_dir'],
            labels=obj['labels']
        )
        return container['Id']

    def startLesser(self, Id):

        self.conn.start ( Id ,publish_all_ports=True)
        portInfo = self.conn.inspect_container(Id)['NetworkSettings']['Ports']

        ports = portInfo.keys()
        info = conf.Info()
        for k,v in portInfo.items():
            if '/' in k:
                k = k.split('/')[0]

            if k == conf.mongoPort:
                info.mongoPort = v[0]['HostPort']
            if k == conf.clientPort:
                info.clientPort = v[0]['HostPort']

            info.Id = Id
            # print ("K is "+ k + " V is " + v[0]['HostPort'] )
        return info


    #user lesser minion create
    # image, command=None, hostname=None, user=None,
        #                  detach=False, stdin_open=False, tty=False,
        #                  mem_limit=None, ports=None, environment=None,
        #                  dns=None, volumes=None, volumes_from=None,
        #                  network_disabled=False, name=None, entrypoint=None,
        #                  cpu_shares=None, working_dir=None, domainname=None,
        #                  memswap_limit=None, cpuset=None, host_config=None,
        #                  mac_address=None, labels=None, volume_driver=None
    def upLesser(self, info):

        containerId = self.createLesser(info)
        return self.startLesser(containerId)


    def stopLesser(self, Id):
        return self.conn.stop( Id )

    #user lesser minion delete
    def delLesser(self, Id):
        return self.conn.remove_container( Id )

    def downLesser(self, Id):
        self.stopLesser(Id)
        return self.delLesser(Id)

    def statusLesser(self, containerid):
        ret = self.conn.stats(containerid)
        return ret

    def allClearLesser(self):
        for i in  (self.conn.containers(all=True)) :
            print ('Delete Container')
            print ( i['Names'],i['Id'] )
            #for stat in lesser.statusLesser(i['Id']):
                # print (stat)
            self.downLesser(i['Id'])

    def cliConfigure(self, obj):
        return


