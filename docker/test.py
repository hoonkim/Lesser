import controller as cont
import configure as conf
#print ( conn.containers(all="true",filters={"labels":""}) )

lesser = cont.MinionController()
test = conf.conconfigObj

# test["user"] = "test"
# test['mongo'] = 2702
# test['lesser'] = 801
test['lesserId'] = "testuser"

con = lesser.upLesser(test)

print (con)

lesser.allClearLesser()


# print (lesser.conn.port('763da610dcc0a3bd3a25eddacc1c34096219c9cf9ef12157477f174156fd46ca',''))
# print (lesser.conn.start ( container = '95881f351fa3705e902cf1f6304baa23a5db12809178d3e5bd25cc0269e69fd1' ))

