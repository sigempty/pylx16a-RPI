from pylx16a.lx16a import *
import time

LX16A.initialize("/dev/ttyUSB0")

print ("Input the old id of the servo")
oid = int(input())
servo = LX16A(oid)

print ("Input the id you want to set for this servo [{}]".format(oid))
id = int(input())
print ("New ID is {}".format(id))

servo.set_id(id)
time.sleep(1)
nid = servo.get_id()

print ("Old ID is {} and new ID is {}".format(oid, nid))
