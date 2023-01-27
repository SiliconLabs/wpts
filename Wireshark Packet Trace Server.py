
import sys
import glob
import serial
import socket
import re
import time
import math

NTP_BASE = 2208988800         #RFC 868 it is 2208988800s to start of epoch
NSEC     = 1000000000
BAUD_RATE = 115200
LOCALHOST_IP = "127.0.0.1"
ZEP_PORT  = 17754


def writeAndCheckRead(command,ser):
	ser.write(command.encode())
	readData = ser.readline()
	#print(readData.decode().replace("> ",""))
	#print(writeData)
	readData = readData.decode().replace("> ","")
	writeData = ''.join(char for char in command if char.isalnum())
	readData = ''.join(char for char in readData if char.isalnum())
	return writeData,readData

	
def findKey(dict,key):
    if key in dict.keys():
        return True,list(dict.keys()).index(key)
    else:
        return False,255


def parse_received_frame(Readdata,packetCount):
	frame = bytearray()
	#magic of python
	tempstring=(((re.sub(r"\([^()]*\)","", (Readdata.replace("{{","").replace("}{"," ")).replace("}}",""))).lstrip(" ")).replace(" 0x","")).split(" ")
	#print(tempstring)
	lengthField=tempstring[0].split(':')
	#have we got the right packet? Check if it has length field       
	if(lengthField[0] == 'len'):
		tempdict={}
		for pair in tempstring:
			k,v = pair.split(':')
			tempdict[k] = v
		#print(tempdict)
		#get payload
		key_present,val=findKey(tempdict, 'payload')				
		if(key_present):
            #ZEP frame version 2
            #ZEP v2 Header will have the following format (if type=1/Data):
            #      |Preamble|Version| Type |Channel ID|Device ID|CRC/LQI Mode|LQI Val|NTP Timestamp|Sequence#|Reserved|Length|
            #      |2 bytes |1 byte |1 byte|  1 byte  | 2 bytes |   1 byte   |1 byte |   8 bytes   | 4 bytes |10 bytes|1 byte|
			payload = tempdict['payload']
			frame = ("EX").encode()                      #preample 2 bytes
			frame += (2).to_bytes(1, byteorder = 'big')  #version 1 byte
			frame += (1).to_bytes(1, byteorder = 'big')  #type 1 byte 
			frame += (int(channel)).to_bytes(1, byteorder = 'big')  #channel 1 byte  
			frame += (1).to_bytes(2, byteorder = 'big')  #device id 2 byte
			frame += (0).to_bytes(1, byteorder = 'big')  #CRC/LQI mode 1 byte 
			key_present,val=findKey(tempdict, 'lqi')
			if(key_present):
				frame += (int(tempdict['lqi'])).to_bytes(1, byteorder = 'big')  #lqi 1 byte
			else:
				raise Exception(lqi[0])	
			ts = time.time()        #seconds since epoch
			frac, whole = math.modf(ts)
			whole = round(whole) + NTP_BASE
			frac = round(frac * 1000000000)
			frame += (whole).to_bytes(4, byteorder = 'big') #timestamp 4 bytes
			frame += (frac).to_bytes(4, byteorder = 'big') #timestamp 4 bytes
			frame += (packetCount).to_bytes(4, byteorder = 'big') #sequence number 4 byte	
			frame += (0).to_bytes(10, byteorder = 'big')          #reserve bytes 10 bytes
			frame += bytes.fromhex(payload)                       #payload

		else:
			raise Exception("didn't get right byte stream")
	return frame




def get_serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


if __name__ == '__main__':
	
	valid_ports = get_serial_ports()
	print('Available ports : ', valid_ports )
	while True:
		wireshark_port = input("Select the port to connect: ")
		if not wireshark_port.upper() in valid_ports:
			print("Not the right port try again.")
			continue
		else:
			try:
				ser = serial.Serial( # set parameters, in fact use your own :-)
    								wireshark_port,
    								baudrate=BAUD_RATE,
    								timeout=1
				)
				ser.isOpen() # try to open port, if possible print message and proceed with 'while True:'
				print ("port is opened!")
				break

			except IOError: # if port is already opened, close it and open it again and print message
				ser.close()
				ser.open()
				print ("port was already open, was closed and opened again!")
				break
	while True:
		channel = input("enter the channel: ")
		if int(channel) < 11 and int(channel) > 26:
			print("invalid channel")
			continue
		else:
			break

    #configure the sniffer or the railtest application
	writeData,readData = writeAndCheckRead("rx 0\r\n",ser)
	if(writeData == readData):
		returnString = ser.readline().decode()
		#print(returnString)
		writeData,readData = writeAndCheckRead("config2p4GHz802154\r\n",ser)	
	else:
		raise Exception(writeData)
	
	if(writeData == readData):
		returnString = ser.readline().decode()
		#print(returnString)
		writeData,readData = writeAndCheckRead("enable802154 rx 100 192 864\r\n",ser)	
	else:
		raise Exception(writeData)

	if(writeData == readData):
		returnString = ser.readline().decode()
		#print(returnString)
		writeData,readData = writeAndCheckRead("setPromiscuousMode 1\r\n",ser)
	else:
		raise Exception(writeData)
	
	if(writeData == readData):
		returnString = ser.readline().decode()
		#print(returnString)
		writeData,readData = writeAndCheckRead("setChannel " + channel + "\r\n",ser)
	else:
		raise Exception(writeData)		
	
	if(writeData == readData):
		returnString = ser.readline().decode()
		#print(returnString)
		writeData,readData = writeAndCheckRead("rx 1",ser)
	else:
		raise Exception(writeData)
	
	if(writeData == readData):
		Readdata = ser.readline().decode()
		#print(Readdata)		
		
	else:
		raise Exception(writeData)
	

	sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
	sock.bind(('', ZEP_PORT))
	packetCount = 0
	while 1:
		Readdata = ser.readline().decode()
		frame = parse_received_frame(Readdata,packetCount)
		
		#print(frame)
		if len(frame) != 0 :
			packetCount+=1
			sys.stdout.write("received: %d   \r" % (packetCount) )
			sys.stdout.flush()
			sock.sendto(frame, (LOCALHOST_IP, ZEP_PORT))

	ser.close()



