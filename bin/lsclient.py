#!/usr/bin/python
import zmq
import signal
import simplejson as json

TIMEOUT = 5

def alarm_handler(signal, frame):
  raise TimeoutError()

def communicate(msg):
  previous_alarm_handler = signal.signal(signal.SIGALRM, alarm_handler)
  try:
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.setsockopt(zmq.LINGER,0)
    signal.alarm(2)
    socket.connect("tcp://127.0.0.1:5678")
    signal.alarm(0)
    #print "Setting timeout to " + str(TIMEOUT)
    signal.alarm(TIMEOUT)
    #print "Sending: " + json.dumps(msg)
    socket.send_json(msg)
    #print "Receiving"
    msg = socket.recv_json()
    signal.alarm(0)
    return msg
  except:
    #print "Returning a com error"
    return('{"result": "Communication Error"}')
  finally:
    #Clean up
    signal.signal(signal.SIGALRM, previous_alarm_handler)
    socket.close()
    context.term()

def status():
  request = {"action": "getcurrentshow"}
  result = communicate(request)
  return(json.dumps(result))

def setshow(showname,showargs):
  request = {"action":"setshow","showname":showname,"showargs":showargs}
  result = communicate(request)
  return(json.dumps(result))

def getshows():
  request = {"action":"getshows"}
  result = communicate(request)
  return(json.dumps(result))

def getshow(showname):
  request = {"action":"getshow","showname":showname}
  #print("Sending " + json.dumps(request))
  result = communicate(request)
  return(json.dumps(result))

