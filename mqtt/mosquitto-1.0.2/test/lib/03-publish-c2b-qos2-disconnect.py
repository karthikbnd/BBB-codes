#!/usr/bin/python

# Test whether a client sends a correct PUBLISH to a topic with QoS 1 and responds to a disconnect.

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
connect_packet = mosq_test.gen_connect("publish-qos2-test", keepalive=keepalive)
connack_packet = mosq_test.gen_connack(rc=0)

disconnect_packet = mosq_test.gen_disconnect()

mid = 1
publish_packet = mosq_test.gen_publish("pub/qos2/test", qos=2, mid=mid, payload="message")
publish_dup_packet = mosq_test.gen_publish("pub/qos2/test", qos=2, mid=mid, payload="message", dup=True)
pubrec_packet = mosq_test.gen_pubrec(mid)
pubrel_packet = mosq_test.gen_pubrel(mid)
pubrel_dup_packet = mosq_test.gen_pubrel(mid, dup=True)
pubcomp_packet = mosq_test.gen_pubcomp(mid)

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
    conn.settimeout(5)
    connect_recvd = conn.recv(len(connect_packet))

    if mosq_test.packet_matches("connect", connect_recvd, connect_packet):
        conn.send(connack_packet)
        publish_recvd = conn.recv(len(publish_packet))

        if mosq_test.packet_matches("publish", publish_recvd, publish_packet):
            # Disconnect client. It should reconnect.
            conn.close()

            (conn, address) = sock.accept()
            conn.settimeout(15)
            connect_recvd = conn.recv(len(connect_packet))

            if mosq_test.packet_matches("connect", connect_recvd, connect_packet):
                conn.send(connack_packet)
                publish_recvd = conn.recv(len(publish_dup_packet))

                if mosq_test.packet_matches("retried publish", publish_recvd, publish_dup_packet):
                    conn.send(pubrec_packet)
                    pubrel_recvd = conn.recv(len(pubrel_packet))

                    if mosq_test.packet_matches("pubrel", pubrel_recvd, pubrel_packet):
                        # Disconnect client. It should reconnect.
                        conn.close()

                        (conn, address) = sock.accept()
                        conn.settimeout(15)
                        connect_recvd = conn.recv(len(connect_packet))

                        # Complete connection and message flow.
                        if mosq_test.packet_matches("connect", connect_recvd, connect_packet):
                            conn.send(connack_packet)

                            publish_recvd = conn.recv(len(publish_dup_packet))
                            if mosq_test.packet_matches("2nd retried publish", publish_recvd, publish_dup_packet):
                                conn.send(pubrec_packet)
                                pubrel_recvd = conn.recv(len(pubrel_packet))

                                if mosq_test.packet_matches("pubrel", pubrel_recvd, pubrel_packet):
                                    conn.send(pubcomp_packet)
                                    disconnect_recvd = conn.recv(len(disconnect_packet))

                                    if mosq_test.packet_matches("disconnect", disconnect_recvd, disconnect_packet):
                                        rc = 0

    conn.close()
finally:
    client.terminate()
    client.wait()
    sock.close()

exit(rc)
