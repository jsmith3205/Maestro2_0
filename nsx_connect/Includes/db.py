#!/usr/bin/python3
import sys

print(sys.path)

#sys.path.append('/Users/jsmith/Documents/GitHub/Maestro2_0/nsx_connect')

# print(sys.path[-1])

import os
import inspect
print("this file: ",os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
print("this file: ",os.path.abspath(inspect.getfile(inspect.currentframe())))
print("this file: ",os.path.dirname(inspect.getfile(inspect.currentframe())))


import sqlite3
from sqlite3 import Error
import re
import sys
import os



cur=None
conn=None

def db_conn():
    print("sys.path ==>" + str(sys.path))
    db=""
    if os.path.dirname(inspect.getfile(inspect.currentframe())) != '':
        db = os.path.dirname(inspect.getfile(inspect.currentframe())) + "/ipam.db"
    else:
        db = "ipam.db"

    try:
        conn = sqlite3.connect(db)
        return(conn)
    except Error as e:
        print(e)
        return

def db_cursor(conn):
    try:
        cur = conn.cursor
        return(cur)
    except Error as e:
        print(e)
        return

def getSubnets(tc=None,net=None, type1=None):
    conn = db_conn()
    cur = conn.cursor()
    subnets = ''
    if tc != None and net == None and type1 == None:
        query = "select * from subnets where tenant = '"+tc+"'"
    elif tc == None and net == None and type1 == None:
        query = "select * from subnets where tenant = '' limit 1"
    elif tc != None and net != None and type1 == None:
        query = "select * from subnets where tenant = '"+tc+"' and network = '"+net+"'"
    elif tc == None and net != None and type1 == None:
        query = "select * from subnets where net = '"+net+"'"
    elif tc != None and net == None and type1 != None:
        query = "select * from subnets where tenant = '"+tc+"' and type1 = '"+type1+"'"
    elif tc == None and net == None and type1 != None:
        query = "select * from subnets where tenant = '' and type1 = '"+type1+"' limit 1"
    elif tc != None and net != None and type1 != None:
        query = "select * from subnets where tenant = '"+tc+"' and network = '"+net+"' and type1 = '"+type1+"'"
    elif tc == None and net != None and type1 != None:
        query = "select * from subnets where net = '"+net+"' and type1 = '"+type1+"'"
    try:
        subnets = cur.execute(query).fetchall()
        print(subnets)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
        return(subnets[0][0]+"/"+subnets[0][1])

def getAddresses(tc=None,net=None, addr=None):
    conn = db_conn()
    cur = conn.cursor()
    print(os.getcwd())
    subnets = ''
    if tc != None and net == None and addr == None:
        query = "select * from addresses where tenant = '" + tc + "'"
    elif tc == None and net == None and addr == None:
        query = "select * from addresses where tenant = '' limit 1"
    elif tc != None and net != None and addr == None:
        query = "select * from addresses where tenant = '" + tc + "' and network = '" + net + "' and assigned_to=''"
    elif tc == None and net != None and addr == None:
        query = "select * from addresses where network = '" + net + "'"
    elif tc != None and net == None and addr != None:
        query = "select * from addresses where tenant = '" + tc + "' and ip_addr = '" + addr + "'"
    elif tc == None and net == None and addr != None:
        query = "select * from addresses where tenant = '' and ip_addr = '" + addr + "' limit 1"
    elif tc != None and net != None and addr != None:
        query = "select * from addresses where tenant = '" + tc + "' and network = '" + net + "' and ip_addr = '" + addr + "'"
    elif tc == None and net != None and addr != None:
        query = "select * from subnets where network = '" + net + "' and ip_addr = '" + addr + "'"
    try:
        print(query)
        subnets = cur.execute(query).fetchall()
        print(subnets)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
        return (subnets)

def getBGPAS(tc=None, bgp_as=None):
    conn = db_conn()
    cur = conn.cursor()
    auto_sys = ''

    if tc != None and bgp_as == None:
        query = "select * from bgp_as where tc = '"+tc+"'"
    if tc != None and bgp_as != None:
        query = "select * from bgp_as where tc = '"+tc+"' and as = '"+bgp_as+"'"
    if tc == None and bgp_as != None:
        query = "select * from bgp_as where as = '"+bgp_as+"'"
    if tc == None and bgp_as == None:
        # query = "test"
        query = "select * from bgp_as where tc = '' limit 1"
    else:
        print("An illegal operation has been committed; Exiting...")
        return

    auto_sys = cur.execute(query).fetchall()[0][1]

    print(auto_sys)
    return(auto_sys)

def inSubnets(nets):
    conn = db_conn()
    cur = conn.cursor()

    try:
        cur.executemany("insert into subnets values (?,?,?,?,?,?)", nets)
    except Error as e:
        print(e)
    finally:
        print("Insert successful")
        conn.commit()
        if conn:
                conn.close()

def inCustSub(net,gw,net_type,tc,excl):
    conn = db_conn()
    cur = conn.cursor()

    network = net.split('/')
    query = "insert into subnets values ('"+network[0]+"','"+network[1]+"','pr','"+net_type+"','"+gw+"','"+tc+"')"

    hosts = getHostIP(net)
    exclr = excl.split('-')
    print(hosts)

    try:
        cur.execute(query)
    except Error as e:
        print(e)
    finally:
        print("Insert successful")
        conn.commit()
        if conn:
            conn.close()

    try:
        for i in range(len(hosts)):
            if (int(hosts[i].split('/')[0].split('.')[3]) >= int(exclr[0]) and int(hosts[i].split('/')[0].split('.')[3]) <= int(exclr[1])) \
                    or hosts[i].split('/')[0] == gw:
                inAddresses(hosts[i],network[1],network[0],tc,gw,'excluded')
            else:
                inAddresses(hosts[i],network[1],network[0],tc,gw)
    except Error as e:
        print(e)
    finally:
        print("Insert successful")



def inBGPAS(ias, c):
    conn = db_conn()
    cur = conn.cursor()

    try:
        for i in range(c):
            cur.execute("insert into bgp_as values ('',"+str(ias)+")")
            print('BGP AS '+str(ias)+' has been added to \'bgp_as\' table...')
            ias += 1
    except Error as e:
        print(e)
    finally:
        print("Insert successful")
        conn.commit()
        if conn:
                conn.close()

def inAddresses(ip,cidr,net,tc,gw='',assignTo=''):
    conn = db_conn()
    cur = conn.cursor()

    inserts = []
    body = ''

    if type(ip) == list:
        for i in range(len(ip)):
            if i == 0:
                body =  "INSERT into addresses values ('"+ip[i]+"','"+cidr+"','"+net+"','"+gw+"','"+tc+"')"
                inserts.append((ip[i],cidr,net,gw,tc,assignTo))
            else:
                body += "\n"
                body =  "INSERT into addresses values ('"+ip[i]+"','"+cidr+"','"+net+"','"+gw+"','"+tc+"')"
                inserts.append((ip[i],cidr,net,gw,tc,assignTo))

        try:
            cur.executemany("insert into addresses values (?,?,?,?,?,?)", inserts)
            print("Insert successful")
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.commit()
                conn.close()
        print(body)
    elif type(ip) == str:
        query = "INSERT into addresses values ('" + ip + "','" + cidr + "','" + net + "','"+gw+"','" + tc + "','"+assignTo+"')"
        print(query)

        try:
            cur.execute(query)
            print("Insert successful")
        except Error as e:
            print(e)
        finally:
            conn.commit()
            if conn:
                conn.close()


def updSubnets(tc='',net=''):
    conn = db_conn()
    cur = conn.cursor()
    print(tc)
    print(net)

    try:
        cur.execute("update subnets set tenant='"+tc+"' where network = '"+net+"'")
    except Error as e:
        print(e)
    finally:
        print("Update successful")
        conn.commit()
        if conn:
            conn.close()

def updAddresses(tc='',net='',host=None):
    conn = db_conn()
    cur = conn.cursor()
    print(tc)
    print(net)

    try:
        if host==None:
            cur.execute("update addresses set tenant='"+tc+"' where ip_add = '"+net+"'")
            print("Update successful")
        else:
            cur.execute("update addresses set tenant='" + tc + "',assigned_to='"+host+"' where ip_add = '" + net + "'")
            print("Update successful")
    except Error as e:
        print(e)
    finally:
        conn.commit()
        if conn:
            conn.close()

def updBGPAS(tc='',bgp_as=''):
    conn = db_conn()
    cur = conn.cursor()
    query = "update bgp_as set tc = '"+tc+"' where bgp_as = '"+bgp_as+"'"
    print(query)

    try:
        cur.execute(query)
    except Error as e:
        print(e)
    finally:
        print("Update Successful")
        conn.commit()
        if conn:
            conn.close()

def ipam_db():
    conn = None
    try:
        conn = db_conn()

        c = conn.cursor()
        try:
            print("tables:  ")
            d = c.execute("SELECT name FROM sqlite_master WHERE name Like 'addresses' or name LIKE 'subnets' or name like 'bgp_as';").fetchall()
            print(d)
            print(type(d))
            print(d[0])
        except IndexError as e:
            print("no tables present in Database...creating IP Networks, IP Address, and BGP AS tables")
        try:
            c.execute('''
                create table subnets (
                    network text,
                    cidr text,
                    type1 text,
                    type2 text,
                    gateway text,
                    tenant text
                );
                ''')
            conn.commit()
            print("'subnets' table has been created.")
        except Error as e:
            print(e)
        try:
            c.execute('''
                create table addresses (
                    ip_add text,
                    cidr text,
                    network text,
                    gateway,
                    tenant text,
                    assigned_to text
                );
                ''')
            conn.commit()
            print("'addresses' table has been created.")
        except Error as e:
            print(e)
        try:
            c.execute('''
                create table bgp_as (
                    tc text,
                    bgp_as text
                );
                ''')
            conn.commit()
            print("'bgp_as' table has been created.")
        except Error as e:
            print(e)
    except Error as e:
        print(e)
    finally:
        subnets = c.execute("select * from subnets;").fetchall()
        print(subnets)
        if len(subnets) == 0:
            print("No subnets have been configured yet")

            choice = ''
            while [x for x in ['Y','y','N','n'] if x != choice]:
                choice = input('Would you like to activate a new subnet (Y or N)? ')
                if choice == 'Y' or choice == 'y':
                    print("creating new subnets...")
                    createSubnets()
                    conn.commit()
                elif choice == 'N' or choice == 'n':
                    dispMenu()
                elif choice =='Q' or choice == 'q':
                    return
                else:
                    print("Invalid Input:  Please enter 'Y' or 'y'...")

                #cont = input("Would you like to create another subnet (Y or N")
        else:
            uchoice=''
            while [x for x in ['a','A','b','B','c','C'] if x != uchoice]:
                print('''
Options: 
A.  List Subnets
B.  Create Subnet
C.  Create BGP AS
D.  Create Custom Network
                ''')
                uchoice = input("What would you like to do?  ")
                if uchoice == 'A' or uchoice == 'a':
                    getSubnets()
                    # subnets = c.execute("SELECT * FROM subnets;").fetchall()
                    # print(subnets)
                elif uchoice == 'B' or uchoice == 'b':
                    print('Creating Subnets...')
                    createSubnets()
                    #insertSubnets(nets)
                    # c.executemany("insert into subnets values (?,?,?,?,?,?)",nets)
                    # conn.commit()
                elif uchoice == 'c' or uchoice == 'C':
                    print('Creating BGP AS(s)...')
                    bgp_as = input('AS number:  ')
                    count = input('Number of AS(s) to create?  ')
                    inBGPAS(int(bgp_as),int(count))
                elif uchoice == 'd' or uchoice == 'D':
                    print('Creating Custom Addresses...')
                    tc = input('Tenant Code (Press enter to leave unassigned):  ')
                    net_type = input('Network Type (l = lan, t = transit, m = management)?  ')
                    net = input('Enter network address and cidr (xxx.xxx.xxx.xxx/xx:  ')
                    gw = input('Gateway address of this network (xxx.xxx.xxx.xxx):  ')
                    excl = input('Exclusion range (xxx-xxx)?  ')

                    inCustSub(net,gw,net_type,tc,excl)
                elif uchoice == 'Q' or uchoice == 'q':
                    return
                else:
                    print("Please enter A,a,B, or b...")
        if conn:
                conn.close()

def dispMenu():
    uchoice = ''
    while [x for x in ['a', 'A', 'b', 'B', 'c', 'C'] if x != uchoice]:
        print('''
    Options: 
    A.  List Subnets
    B.  Create Subnet
    C.  Create BGP AS
    D.  Create Custom Network
                    ''')
        uchoice = input("What would you like to do?  ")
        if uchoice == 'A' or uchoice == 'a':
            getSubnets()
            # subnets = c.execute("SELECT * FROM subnets;").fetchall()
            # print(subnets)
        elif uchoice == 'B' or uchoice == 'b':
            print('Creating Subnets...')
            createSubnets()
            # insertSubnets(nets)
            # c.executemany("insert into subnets values (?,?,?,?,?,?)",nets)
            # conn.commit()
        elif uchoice == 'c' or uchoice == 'C':
            print('Creating BGP AS(s)...')
            bgp_as = input('AS number:  ')
            count = input('Number of AS(s) to create?  ')
            inBGPAS(int(bgp_as), int(count))
        elif uchoice == 'd' or uchoice == 'D':
            print('Creating Custom Addresses...')
            tc = input('Tenant Code (Press enter to leave unassigned):  ')
            net_type = input('Network Type (l = lan, t = transit, m = management)?  ')
            net = input('Enter network address and cidr (xxx.xxx.xxx.xxx/xx:  ')
            gw = input('Gateway address of this network (xxx.xxx.xxx.xxx):  ')
            excl = input('Exclusion range (xxx-xxx)?  ')

            inCustSub(net, gw, net_type, tc, excl)
        elif uchoice == 'Q' or uchoice == 'q':
            return
        else:
            print("Please enter A,a,B, or b...")

def createSubnets():
    addr_pattern = r'\d'
    sm_pattern = r'\d+'
    body = ''

    print("creating new subnets...")
    tenant = ""
    octets = ['999','999','999','999']
    while (re.match(addr_pattern,octets[0])==None or re.match(addr_pattern,octets[1])==None or \
            re.match(addr_pattern,octets[2])==None or re.match(addr_pattern,octets[3])==None) or \
            ([x for x in octets if int(x) > 256 or int (x) < 0]):
        print(octets)
        print(re.match(addr_pattern,octets[0]))
        print(re.match(addr_pattern, octets[1]))
        print(re.match(addr_pattern, octets[2]))
        print(re.match(addr_pattern, octets[3]))
        network = input('Network Address (xxx.xxx.xxx.xxx):  ')
        octets = network.split('.')
        if re.match(addr_pattern,octets[0])==None or re.match(addr_pattern,octets[1])==None or \
            re.match(addr_pattern,octets[2])==None or re.match(addr_pattern,octets[3])==None or \
            ([x for x in octets if int(x) > 256 or int(x) < 0]):
            print("Incorrect Format:  Example 192.168.0.0")

    cidr = input('Subnet Lenght (nn):  ')
    type1 = input('Public (pu) or Private (pr):  ')
    type2 = input('Transit (t) or Lan (l):  ')

    split = 0
    while re.match(sm_pattern,str(split)) == None or (int(split) < 1 or int(split) > 32):
        split = input('what would you like to split this network into?  ')
        if re.match(sm_pattern,str(split)) == None or (int(split) < 1 or int(split) > 32):
            print("please enter a valid integer between 0 and 32")

    gateway = ''
    if type2 == 'l':
        while (re.match(addr_pattern, octets[0]) == None or re.match(addr_pattern, octets[1]) == None or \
               re.match(addr_pattern, octets[2]) == None or re.match(addr_pattern, octets[3]) == None) or \
                ([x for x in octets if int(x) > 256 or int(x) < 0]):
            gateway = input('Gateway IP:  ')
            if (re.match(addr_pattern, octets[0]) == None or re.match(addr_pattern, octets[1]) == None or \
                   re.match(addr_pattern, octets[2]) == None or re.match(addr_pattern, octets[3]) == None) or \
                    ([x for x in octets if int(x) > 256 or int(x) < 0]):
                print("Incorrect Format:  Example 192.168.0.0")


    net = network.split('.')
    mask = cidr

    net_count = 2**(int(split) - int(mask))
    net_inc = 2**(32 - int(split))

    print("Netowrk:  "+ '.'.join(net))
    print("Network mask:  "+mask)
    print("Split into /"+str(split)+"'s")
    print("Number of networks:  "+str(net_count))
    print("Net Increment:  "+str(net_inc))

    networks = []
    inserts = []
    print("Networks are:")
    for i in range(net_count):
        networks.append(int(net[3]) + (net_inc * i))
        network = net[0]+'.'+net[1]+'.'+net[2]+'.'+str(networks[i])
        print("INSERT into subnets values ('"+network+"','"+split+"','"+type1+"','"+type2+"','"+gateway+"','"+tenant+"')")
        if i == 0:
            body =  "INSERT into subnets values ('"+network+"','"+split+"','"+type1+"','"+type2+"','"+gateway+"','"+tenant+"')"
            inserts.append((network,split,type1,type2,gateway,tenant))
        else:
            body += "\n"
            body += "INSERT into subnets values ('"+network+"','"+split+"','"+type1+"','"+type2+"','"+gateway+"','"+tenant+"')"
            inserts.append((network, split, type1, type2, gateway, tenant))
    print(body)
    inSubnets(inserts)

def getHostIP(net=''):
    this_net = net.split('/')
    net = this_net[0].split('.')
    subnet = this_net[1]
    hostIP = []

    if int(subnet) >= 24 and int(subnet) <= 32:
        host_count = 2**(32 - int(subnet))
        for i in range(host_count-2):
            host = int(net[3])+i+1
            hostIP.append(net[0]+"."+net[1]+"."+net[2]+"."+str(host)+"/"+subnet)

    return hostIP

if __name__ == "__main__":
    ipam_db()
    # inBGPAS(65050,100)
    # tc = input("Tenant Code?  ")
    # bgp_as = getBGPAS()
    # updBGPAS(tc,bgp_as)

    # getSubnets()
else:
    print("Imported by " + __name__)