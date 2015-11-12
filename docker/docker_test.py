import docker_controller as cont

lesser = cont.MinionController()
test = cont.conf.configObj


test['lesserId'] = "testuser"

con = lesser.upLesser( test )

print ( con )

# print ( lesser.getContainerStatus(con.Id) )

print (lesser.getAllContainers())

lesser.allClearLesser()