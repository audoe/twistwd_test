import socket
import uuid


#source
mac=uuid.getnode()

ip=socket.gethostbyname(socket.gethostname())

#
li=[]
while mac>=16:
    li.append(mac%16)
    mac=mac/16
while len(li)<12:
    li.append(0)
li.reverse()

tmp=[hex(int(i)) for i in li]
t1=[i[len(i)-1:] for i in tmp]
lia=[''.join((t1[i],t1[i+1])) for i in range(0,len(t1)-1,2)]
print 'ip is %s'%ip
print 'mac is %s'%(':'.join(lia))

