import time
import sys
import ibmiotf.application
import ibmiotf.device
import random


#Provide your IBM Watson Device Credentials
organization = "2melo1"
deviceType = "waste1"
deviceId = "2345"
authMethod = "token"
authToken = "12345678"

        


try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

# Initialize GPIO


def myCommandCallback(cmd):
    print("Command received: %s" % cmd.data['command'])
    status=cmd.data['command']
    if status=="waste level":
        print ("waste level monitored")
    else :
        print ("weight is monitored")
   
    #print(cmd)
    
while True:
        #Get Sensor Data from HX711
        
        Garbage_level1=random.randint(0,100)
        Trash_Weight1=random.randint(0,100)
        
        data = { 'Garbage_level' : Garbage_level1, 'Trash_Weight': Trash_Weight1 }
        #print data
        def myOnPublishCallback():
            print ("Published Level = %s %%" % Garbage_level1, "Weight = %s gallon" % Trash_Weight1, "to IBM Watson")

        success = deviceCli.publishEvent("IoTSensor", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(20)
        
        deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()
