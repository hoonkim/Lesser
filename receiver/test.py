from worker import *


print("===== Lesser Unit test =====")
 
print("====== bamboo.py ======")

print(" - class :: LesserWorker validation test - ")

work = LesserWork(ipaddress.ip_address('10.88.92.226'), 8000, HostProtocol.POST, "/", "{\"test\":33}")

if str(work) == "<10.88.92.226/8000/POST///{\"test\":33}>":
    print("LesserWork class OK")
else:
    print("LesserWork class FAIL")
    print(work)

print("====== bamboo.py ======")

print(" - class :: LesserWorker validation test - ")

worker = LesserWorker()

worker.AddWork(work)

if worker.GetWorkCount() == 1:
    print("LesserWorkerer class WorkCount method OK")
else:
    print("LesserWorkerer class WorkCount method FAIL")
    print(worker.GetWorkCount())

work2 = LesserWork(ipaddress.ip_address('10.88.92.227'), 8080, HostProtocol.PUT, "/", "{\"test\":444}")

worker.AddWork(work2)

deqwork = worker.GetWork()

if str(deqwork) == "<10.88.92.226/8000/POST///{\"test\":33}>":
    print("LesserWork class addWork / getWork method OK")
else:
    print("LesserWork class addWork / getWork method FAIL")
    print(type(deqwork), deqwork)


worker.start()

time.sleep(1)

worker.exitWorker()