# NOTES: Originally based on Luke Miller's code for Cole Parmer bath. 
# TODO: parallelize for 8 baths
# TODO: Read remote temperature probe rather than bath temp
# TODO: Set operation to remote probe
#Needed to remove "float" from read commands, b/c Thermo bath returns letter 'C' via serial after temperature
#WWD 30Mar2018
#


import time
import datetime #datetime module
import serial # from http://pyserial.sourceforge.net/pyserial.html
              # beginner's install instructions for Windows here:
              # http://learn.adafruit.com/arduino-lesson-17-email-sending-movement-detector/installing-python-and-pyserial
import sys # for user input
import csv # module for reading csv files
import os # for jumping around directories if needed, current .csv file save in C/Dowdlabscripts

def readcsv(filename):	#Fxn to read CSV; input filename and will prompt for row to start reading, note first line is 0
    ifile = open(filename, "rU")
    reader = csv.reader(ifile, delimiter=",")
    print "Does file have header row (1) or not (0)?"
    rownum = raw_input("Type 0 or 1 and hit Enter:  ")
    rownum = int(rownum) #convert input to int for loop
    #rownum = 1	#set to 0 if want to read from first line
    a = ['float']

    for row in reader:
        a.append (row)
        rownum += 1
    
    ifile.close()
    return a 
def writecsv(filename,dateout,setout,tempout):	#input filename,note first line is 0
    with open(filename, 'ab') as csvfile:
        tigwriter = csv.writer(csvfile, delimiter=',')
        #rownum = 1	#set to 0 if want to read from first line
        tigwriter.writerow([dateout,setout,tempout])
        csvfile.close()
        
# Establish serial communications with the water bath. Instrument interface menu
# recommend 19200 baud, 8-N-1, no flow control. No linefeeds (\n) should be
# used in the communications with the water bath, only carriage returns (\r). 
# Useful commands for the water bath: 
# RS\r = get current setpoint temperature
# RT\r = get current internal bath temperature
# SS xx.xx\r = change bath setpoint (i.e. SS 25.50, units of degrees Celsius)
# SE1 = turn on command echo. It seems counterintuitive, but this seems to be
#         necessary for this script to run.

# Begin by establishing a serial connection with the bath. The entry COM1 below
# will need to be changed to suit your specific serial port name. On a Mac this
# will be something like dev/tty.usbserial-xxxxxxx, on Windows it will be a
# COM port like COM1. If using Windows cygwin dev/ttyS0 corresponds with COM1, etc.  

# if running cygwin command line use this command to figure out the port:
# python -m serial.tools.list_ports

# if already in python use next 2 lines: 
# import serial.tools.list_ports
# print([comport.device for comport in serial.tools.list_ports.comports()])
# for example on Dowd Mytilus laptop it returns ['/dev/ttyS9']
try: 
    bath = serial.Serial(
                        '/dev/ttyS10',  #'/dev/ttyS9' COM4
						baudrate = 19200,
						bytesize=8,
						#parity="NONE",
                        #stopbits=1,
						timeout = 1)

    print "***********************************"
    print "Serial connection established on "
    print bath.name # print port info
    print "***********************************"
    time.sleep(2)
	#bath.write("SE1\r") # turn on command echo
    #response = bath.readline() # always read the response to clear the buffer
    #print "SE0 response: %s" % response
    bath.write("RT \r")
    response = bath.readline()  #float
    print "Current bath temperature: %s" % response  #reads response as string
    bath.write("RS\r")
    response = bath.readline()
    print "Current bath setpoint: %s" % response
    continue_flag = True
except:
    print "++++++++++++++++++++++++++"
    print "Serial connection failed"
    print "++++++++++++++++++++++++++"
    time.sleep(5)
    continue_flag = False


#Start by asking user which TigBath__.csv file to open"
if continue_flag:
    print "Enter name of TigBathxx CSV file that corresponds to DowdBathxx"
    print "Be sure CSV file cells are Number format with 3 decimals!"
    bathID = raw_input("Hit Enter when done...   \n")
    bathID2 = bathID + ".csv"
    tempset = readcsv(bathID2)

if continue_flag:
        flag = False # set the while-loop flag, runs forever
        bath.write("SO 1\r")# set status of bath to on/run
        response=bath.readline()
        while flag != True:
            if datetime.time(0,0,0): #midnight returns False in Python (=0)
                mintoday = 1
            else:
                curr = datetime.datetime.now() #.strftime('%Y-%m-%d %H:%M:%S')
                mintoday = int(curr.hour)*60+int(curr.minute)curr = datetime.datetime.now() #.strftime('%Y-%m-%d %H:%M:%S')
            mintoday = int(curr.hour)*60+int(curr.minute)
            print mintoday
            set_temp = tempset[mintoday]
            set_temp = float(set_temp[0])
            #print set_temp #troubleshooting conversion
            print "Updating temp setpoint: %2.2f C" % set_temp
            # Assemble the command to send to the water bath
            command = "SS " + "%2.2f\r" % set_temp
            bath.write(command)
            response = bath.readline()
            #read the response to clear buffer
            time.sleep(10)
            # Now check that the set point worked
            bath.write("RS\r")
            response = bath.readline()
            new_point = float(response[0:5])
            if response == set_temp:
                print "Setpoint set: %2.2f C" % response
            time.sleep(5)
            timewrite = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            #filetime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            bath.write("RT \r")
            readtemp = bath.readline()
            readtemp = float(response[0:5])
            outfile = bathID + "_record.csv"
            #outfile = bathID + "_" + filetime + "_record.csv"
            writecsv(outfile,timewrite,set_temp,readtemp)#flag = True  # set True to kill while loop
