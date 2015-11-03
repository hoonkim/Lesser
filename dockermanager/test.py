import dockermanager.controller as cont
import dockermanager.configure as conf
#print ( conn.containers(all="true",filters={"labels":""}) )

lesser = cont.MinionController()
test = conf.configObj

# test["user"] = "test"
# test['mongo'] = 2702
# test['lesser'] = 801
test['lesserId'] = "testuser"

disk = lesser.diskSpace()
# con = lesser.upLesser(test)
print("1")
# print (con.Id)
# print ( lesser.downLesser(con.Id) )
# print (lesser.conn.port('763da610dcc0a3bd3a25eddacc1c34096219c9cf9ef12157477f174156fd46ca',''))
# print (lesser.conn.start ( container = '95881f351fa3705e902cf1f6304baa23a5db12809178d3e5bd25cc0269e69fd1' ))

# lesser.allClearLesser()
