#!/usr/bin/python
import zmq
import simplejson as json
import sys

TIMEOUT = 5

def communicate(msg):
  try:
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.setsockopt(zmq.LINGER,0)
    socket.connect("tcp://127.0.0.1:5678")
    #print "Sending: " + json.dumps(msg)
    socket.send_json(msg)
    #print "Receiving"
    msg = socket.recv()
    #print "Received " + msg
    return msg
  except:
    #print("Unexpected error:", sys.exc_info()[0])
    return('{"result": "Communication Error"}')
  finally:
    socket.close()
    context.term()

def status():
  request = {"action": "getcurrentshow"}
  #print("in lsc.status, sending " + json.dumps(request))
  result = json.loads(communicate(request))
  return(json.dumps(result))

def setshow(showname,showargs):
  request = {"action":"setshow","showname":showname,"showargs":showargs}
  result = json.loads(communicate(request))
  return(json.dumps(result))

def getshows():
  request = {"action":"getshows"}
  #print("in lsc.getshows, sending " + json.dumps(request))
  result = json.loads(communicate(request))
  return(json.dumps(result))

def getshow(showname):
  request = {"action":"getshow","showname":showname}
  result = json.loads(communicate(request))
  return(json.dumps(result))

def getcolornames():
  request = {"action":"getcolornames"}
  result = json.loads(communicate(request))
  return(json.dumps(result))

