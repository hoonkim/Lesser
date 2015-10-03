import controller as cont

lesser = cont.MinionController()
test = cont.conf.configObj


test['lesserId'] = "testuser"

con = lesser.upLesser( test )

print ( con )

print ( lesser.getContainerInfo(con.Id)['State'])

lesser.allClearLesser()