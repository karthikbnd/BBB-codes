#!/usr/bin/python

# Test whether a client sends a correct UNSUBSCRIBE packet.

import inspect
import os
import subprocess
import socket
import sys
import time

# From http://stackoverflow.com/questions/279237/python-import-a-module-from-a-folder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"..")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

import mosq_test

rc = 1
keepalive = 60
connect_packet = mosq_test.gen_connect("unsubscribe-test", keepalive=keepalive)
connack_packet = mosq_test.gen_connack(rc=0)

disconnect_packet = mosq_test.gen_disconnect()

mid = 1
unsubscribe_packet = mosq_test.gen_unsubscribe(mid, "unsubscribe/test")
unsuback_packet = mosq_test.gen_unsuback(mid)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.settimeout(10)
sock.bind(('', 1888))
sock.listen(5)

client_args = sys.argv[1:]
env = dict(os.environ)
env['LD_LIBRARY_PATH'] = '../../lib:../../lib/cpp'
try:
    pp = env['PYTHONPATH']
except KeyError:
    pp = ''
env['PYTHONPATH'] = '../../lib/python:'+pp
client = subprocess.Popen(client_args, env=env)

try:
    (conn, address) = sock.accept()
    conn.settimeout(10)
    connect_recvd = conn.recv(len(connect_packet))

    if mosq_test.packet_matches("connect", connect_recvd, connect_packet):
        conn.send(connack_packet)
        unsubscribe_recvd = conn.recv(len(unsubscribe_packet))

        if mosq_test.packet_matches("unsubscribe", unsubscribe_recvd, unsubscribe_packet):
            conn.send(unsuback_packet)
            disconnect_recvd = conn.recv(len(disconnect_packet))
        
            if mosq_test.packet_matches("disconnect", disconnect_recvd, disconnect_packet):
                rc = 0
        
    conn.close()
finally:
    client.terminate()
    client.wait()
    sock.close()

exit(rc)