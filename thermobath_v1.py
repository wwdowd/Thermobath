# NOTES: based on Luke Miller's code for Cole Parmer bath. 
#ONLY OPTION 0 (constant temperature) HAS BEEN UPDATED
#Need to remove "float" from other options for correct format
#WWD 12Mar2018
#


import time
import serial # from http://pyserial.sourceforge.net/pyserial.html
              # beginner's install instructions for Windows here:
              # http://learn.adafruit.com/arduino-lesson-17-email-sending-movement-detector/installing-python-and-pyserial
import sys # for user input

# Establish serial communications with the water bath. Instrument interface menu
# recommend 19200 baud, 8-N-1, no flow control. No linefeeds (\n) should be
# used in the communications with the water bath, only carriage returns (\r). 
# Useful commands for the water bath: 
# RS = get current setpoint temperature
# RT = get current internal bath temperature
# SSxxx.xx\r = change bath setpoint (i.e. SS025.50, units of degrees Celsius)
# SE1 = turn on command echo. It seems counterintuitive, but this seems to be
#         necessary for this script to run.

# Begin by establishing a serial connection with the bath. The entry COM1 below
# will need to be changed to suit your specific serial port name. On a Mac this
# will be something like dev/tty.usbserial-xxxxxxx, on Windows it will be a
# COM port like COM1. 

#if running python from cygwin use this set of commands to figure out the port:
# import serial.tools.list_ports
# print([comport.device for comport in serial.tools.list_ports.comports()])
# for example on Dowd Mytilus lapt it returns ['/dev/ttyS9']
try: 
    bath = serial.Serial(
                        '/dev/ttyS9',  #COM4
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
	
################################################################################
# Start by asking the user which version of the temperature ramp they want to
# carry out. Option 1 will bring the water bath to a starting temperature and 
# hold it there until the user starts the ramp. Option 2 will immediately 
# start the ramp from the current temperature (useful when the user has 
# manually set the water bath starting temperature already). 
if continue_flag:
        
    print "######################################################"
    print "Choose a routine to run (enter 0, 1, or 2): " 
    print "0. Set to constant temperature"
    print "1. Set to starting temperature, pause, then start ramp"
    print "2. Start ramp immediately from current temperature"
    prog = raw_input("Enter 0, 1, or 2: ")

if prog == "0":
    set_temp = raw_input("Enter the constant setpoint temperature (C): ")
    set_temp = float(set_temp)
    set_temp_str = str(set_temp) #convert to str to send command to change sp 
elif prog == "1":
        # Get the various temperature parameters from the user
        init_temp = raw_input("Enter the starting temperature (C): ")
        init_temp = float(init_temp) # Convert to float

        target_temp = raw_input("Enter the target temperature (C): ")
        target_temp = float(target_temp) # convert to float
        
        rise_rate = raw_input("Enter temperature ramp rate (C per hour): ")
        rise_rate = float(rise_rate)

        hold_time = raw_input("Enter time to hold at target temperature (min): ")
        hold_time = float(hold_time)

        fall_rate = raw_input("Enter temperature fall rate (C per hour): ")
        fall_rate = float(fall_rate)

        end_temp = raw_input("Enter the ending temperature (C): ")
        end_temp = float(end_temp)
elif prog == "2":
        target_temp = raw_input("Enter the target temperature (C): ")
        target_temp = float(target_temp) # convert to float
        
        rise_rate = raw_input("Enter temperature ramp rate (C per hour): ")
        rise_rate = float(rise_rate)


if prog == "0":
        flag = False # set the while-loop flag
        bath.write("SO 1\r")# set status of bath to on/run
        response=bath.readline()
        while flag != True:
            print "Setting constant temperature: %2.2f C" % set_temp
            # Assemble the command to send to the water bath
            command = "SS " + "%2.2f\r" % set_temp
            bath.write(command)
            response = bath.readline()
            #read the response to clear buffer
            time.sleep(10)
            # Now check that the set point worked
            bath.write("RS\r")
            response = bath.readline()
            new_point = float(response[1:5])
            if response == set_temp:
                print "Setpoint set: %2.2f C" % response
                flag = True  # set True to kill while loop
	
    ################################################################################
    # The user chose version 1. Begin by changing the bath setpoint to the 
    # init_temp, and wait for the bath to achieve that temperature.
if prog == "1":
        # The first step will be to set the initial temperature on the water  
        # bath and wait around until it reaches that temperature.
        flag = False # set the while-loop flag
        bath.write("SO 1\r")# set status of bath to on/run
        response=bath.readline()
        while flag != True:
            print "Setting initial temperature: %2.2f C" % init_temp
            # Assemble the command to send to the water bath
            command = "SS0" + "%2.2f\r" % init_temp 
            bath.write(command)
            response = bath.readline() # always read the response to clear 
                                       # the buffer
            time.sleep(0.01)
            # Now check that the set point worked
            bath.write("RS\r")
            response = float(bath.readline())
            if response == init_temp:
                print "Setpoint set: %2.2f C" % response
                flag = True  # set True to kill while loop
            
        # Next we need to wait around for the water bath to get to the initial 
        # temperature.         
        flag = False # reset test flag
        while flag != True:
            time.sleep(5)
            bath.write("RT\r")  # request current bath internal temperature
            response = float(bath.readline())
            print "Current bath temp: %2.2f C" % response
            # When the bath temperature gets within 0.05 of the target, we're 
            # close enough
            if (abs(init_temp - response) < 0.1):
                flag = True  # set True to kill while loop
        # The script will now hold at the initial temperature until the user 
        # tells it to begin ramping the temperature to the target_temp.
        print "****************************************************"
        print "****************************************************"
        print "Initial temperature reached"
        print ""
        junk = raw_input("Press return to start temperature ramp")
        print "Starting temperature ramp"
        print "****************************************************"


    ############################################################################
    # If the user chose program 2, they skipped the initial temperature change 
    # above. Query the water bath to find its current setpoint and use that 
    # value as the init_temp
if prog == "2":
    bath.write("SO 1\r")# set status of bath to on/run
    response=bath.readline()
    bath.write("RS\r") # Query setpoint
    response = float(bath.readline()) # Read setpoint from bath
    init_temp = response # Set init_temp 

    ############################################################################
    # The next step is to change the water bath temperature at the specified 
    # rate until it hits the target_temp

    # Calculate the number of degrees to be covered
    temp_diff = abs(target_temp - init_temp)

    # Calculate the time needed for the ramp (degrees / degrees per hour)
    ramp_duration = temp_diff / rise_rate # units hours
    ramp_duration_m = ramp_duration * 60 # convert to minutes
    print "Ramp will take %2.2f hrs (%1.0f minutes)" % \
        (ramp_duration,ramp_duration_m)

    # Calculate per-minute temperature step (units of degrees C)
    # rise_rate was specified by the user in units of degrees C per hour
    rise_rate_m = rise_rate / 60

    # In cases where the target_temp is lower than the init_temp, the 
    # rise_rate_m value will need to be a negative number for this to work
    # correctly.
    if (target_temp - init_temp) < 0:
        rise_rate_m = rise_rate_m * -1
        decrease_flag = True # This flag will notify the loops below to lower
                             # the temperature instead of raising it.
    else:
        decrease_flag = False # The ramp will be an increasing ramp
            
    prev_time = time.time() # get starting time (in seconds)
    bath.write("RS\r") # get current setpoint
    current_set = float(bath.readline()) # always read response to clear buffer
    current_set = current_set + rise_rate_m # add temp step to current setpoint
    command = "SS0" + "%2.2f\r" % current_set 
    bath.write(command) # change set point
    response = bath.readline()
    
    flag = False # set initial flag
    while flag != True:
        time.sleep(1)
        new_time = time.time() # get time again
        # Compare new_time to prev_time, if more than 60 seconds have elapsed, 
        # update the setpoint to the next temperature
        if new_time > (prev_time + 60):
            prev_time = new_time # update to new time
            current_set = current_set + rise_rate_m # add temp step to setpoint
            if current_set < target_temp and not decrease_flag:
                command = "SS0%2.2f\r" % current_set
                bath.write(command) # update water bath setpoint
                response = bath.readline()
                # Calculate remaining temperature to cover
                temp_left = target_temp - current_set
                # Calculate remaining time in minutes
                time_left = temp_left / rise_rate_m
                if time.localtime().tm_min % 1 == 0:
                    # If the current minute is evenly divisible by 1, print out
                    # an update of the setpoint and remaining minutes
                    time_left_s = time_left * 60 # convert time_left to seconds
                    # calculate finishing time in seconds
                    final_time = new_time + time_left_s + 60
                    # convert final_time to a human-readable string                
                    final_str = time.strftime("%H:%M", 
                                              time.localtime(final_time))
                    print "Current setpoint: %2.2f C, finishing at approx. %s" % \
                        (current_set,final_str)
            elif current_set >= target_temp and not decrease_flag:
                # If the new current_set value is greater than the target_temp, 
                # then the bath has nearly reached the target temp. Make the new 
                # setpoint equal to target_temp and set flag to True to kill 
                # this while loop
                current_set = target_temp # set current_set to the final 
                                          # target_temp
                command = "SS0%2.2f\r" % current_set
                bath.write(command)
                response = bath.readline() # read line to clear buffer
                flag = True # set flag True to kill while loop
                print "Waiting to reach final temperature"
            elif current_set > target_temp and decrease_flag:
                # The temperature should be ramped downward when decrease_flag
                # is True
                command = "SS0%2.2f\r" % current_set
                bath.write(command) # update water bath setpoint
                response = bath.readline()
                # Calculate remaining temperature to cover
                temp_left = target_temp - current_set
                # Calculate remaining time in minutes
                time_left = temp_left / rise_rate_m
                if time.localtime().tm_min % 1 == 0:
                    # If the current minute is evenly divisible by 1, print out
                    # an update of the setpoint and remaining minutes
                    time_left_s = time_left * 60 # convert time_left to seconds
                    # calculate finishing time in seconds
                    final_time = new_time + time_left_s + 60
                    # convert final_time to a human-readable string                
                    final_str = time.strftime("%H:%M", 
                                              time.localtime(final_time))
                    print "Current setpoint: %2.2f C, finishing at approx. %s" % \
                        (current_set,final_str)
                        
            elif current_set <= target_temp and decrease_flag:
                # If the new current_set value is less than the target_temp and
                # the decrease_flag is True (temperature ramp is going down),
                # then the bath has nearly reached the target temperature. 
                # Make the new setpoint equal to target_temp and set flag to 
                # True to kill this while loop 
                current_set = target_temp # set current_set to the final 
                                          # target_temp
                command = "SS0%2.2f\r" % current_set
                bath.write(command)
                response = bath.readline() # read line to clear buffer
                flag = True # set flag True to kill while loop
                print "Waiting to reach final temperature"
                
    # Now hang out and wait for the bath temperature to get close to the final
    # target temperature
    flag = False
    while flag != True:
        time.sleep(1)
        bath.write("RT\r") # Query current bath temperature
        response = float(bath.readline())
        print "Current temperature: %2.2f C" % response
        if (abs(response - target_temp) < 0.05):
            print "**************************************************"
            print "**************************************************"
            print "Starting hold of peak Temperature"    
            print "**************************************************"
            print "**************************************************"
            flag = True
            time.sleep(2)
    
    ####################################################################
    # At this point the water bath should hold at the peak temp for the 
    #specified amount of time
   
    print "Peak hold duration will take %1.0f minutes" % hold_time #check OK
    # hold_time was specified by the user in minutes
    
   
    prev_time = time.time() # get starting time (in seconds)

    flag = False # set initial flag
    while flag != True:
        # time.sleep(1)
        new_time = time.time()# get time again
        # time.sleep(1)
        # Compare new_time to prev_time, if new time equals previous time plus
         #the specified hold time (in seconds), then its time to kill the while 
         #loop
        print "Hold time in seconds: %2.0f" %(hold_time*60)
        if new_time >= (prev_time + (hold_time*60)): 
            print "**************************************************"
            print "**************************************************"
            print "Ramp peak finished"    
            print "**************************************************"
            print "**************************************************"
            flag = True # set flag to True to kill while loop
            # time.sleep(1)
    

    ############################################################################
    # The next step is to change the water bath temperature at the specified 
    # fall rate until it hits the end_temp

    # Calculate the number of degrees to be covered
    temp_diff = abs(end_temp - target_temp)

    # Calculate the time needed for the ramp (degrees / degrees per hour)
    fall_duration = temp_diff / fall_rate # units hours
    fall_duration_m = fall_duration * 60 # convert to minutes
    print "Ramp down will take %2.2f hrs (%1.0f minutes)" % \
        (fall_duration,fall_duration_m)

    # Calculate per-minute temperature step (units of degrees C)
    # fall_rate was specified by the user in units of degrees C per hour
    fall_rate_m = fall_rate / 60

    # In cases where the end_temp is lower than the init_temp, the 
    # fall_rate_m value will need to be a negative number for this to work
    # correctly.
    if (end_temp - target_temp) < 0:
        fall_rate_m = fall_rate_m * -1
        decrease_flag = True # This flag will notify the loops below to lower
                             # the temperature instead of raising it.
    else:
        decrease_flag = False # The ramp will be an increasing ramp
            
    prev_time = time.time() # get starting time (in seconds)
    bath.write("RS\r") # get current setpoint
    current_set = float(bath.readline()) # always read response to clear buffer
    current_set = current_set + fall_rate_m # add temp step to current setpoint
    command = "SS0" + "%2.2f\r" % current_set 
    bath.write(command) # change set point
    response = bath.readline()
    
    flag = False # set initial flag
    while flag != True:
        time.sleep(1)
        new_time = time.time() # get time again
        # Compare new_time to prev_time, if more than 60 seconds have elapsed, 
        # update the setpoint to the next temperature
        if new_time > (prev_time + 60):
            prev_time = new_time # update to new time
            current_set = current_set + fall_rate_m # add temp step to setpoint
            if current_set < end_temp and not decrease_flag:
                command = "SS0%2.2f\r" % current_set
                bath.write(command) # update water bath setpoint
                response = bath.readline()
                # Calculate remaining temperature to cover
                temp_left = end_temp - current_set
                # Calculate remaining time in minutes
                time_left = temp_left / fall_rate_m
                if time.localtime().tm_min % 1 == 0:
                    # If the current minute is evenly divisible by 1, print out
                    # an update of the setpoint and remaining minutes
                    time_left_s = time_left * 60 # convert time_left to seconds
                    # calculate finishing time in seconds
                    final_time = new_time + time_left_s + 60
                    # convert final_time to a human-readable string                
                    final_str = time.strftime("%H:%M", 
                                              time.localtime(final_time))
                    print "Current setpoint: %2.2f C, finishing at approx. %s" % \
                        (current_set,final_str)
            elif current_set >= end_temp and not decrease_flag:
                # If the new current_set value is greater than the end_temp, 
                # then the bath has nearly reached the end temp. Make the new 
                # setpoint equal to end_temp and set flag to True to kill 
                # this while loop
                current_set = end_temp # set current_set to the final 
                                          # target_temp
                command = "SS0%2.2f\r" % current_set
                bath.write(command)
                response = bath.readline() # read line to clear buffer
                flag = True # set flag True to kill while loop
                print "Waiting to reach ending temperature"
            elif current_set > end_temp and decrease_flag:
                # The temperature should be ramped downward when decrease_flag
                # is True
                command = "SS0%2.2f\r" % current_set
                bath.write(command) # update water bath setpoint
                response = bath.readline()
                # Calculate remaining temperature to cover
                temp_left = abs(end_temp - current_set) #FK added in absolute value
                # Calculate remaining time in minutes
                time_left = temp_left / fall_rate_m
                if time.localtime().tm_min % 1 == 0:
                    # If the current minute is evenly divisible by 1, print out
                    # an update of the setpoint and remaining minutes
                    time_left_s = time_left * 60 # convert time_left to seconds
                    # calculate finishing time in seconds
                    final_time = new_time + time_left_s + 60
                    # convert final_time to a human-readable string                
                    final_str = time.strftime("%H:%M", 
                                              time.localtime(final_time))
                    print "Current setpoint: %2.2f C, finishing at approx. %s" % \
                        (current_set,final_str)
                        
            elif current_set <= end_temp and decrease_flag:
                # If the new current_set value is less than the target_temp and
                # the decrease_flag is True (temperature ramp is going down),
                # then the bath has nearly reached the target temperature. 
                # Make the new setpoint equal to target_temp and set flag to 
                # True to kill this while loop 
                current_set = end_temp # set current_set to the final 
                                          # target_temp
                command = "SS0%2.2f\r" % current_set
                bath.write(command)
                response = bath.readline() # read line to clear buffer
                flag = True # set flag True to kill while loop
                print "Waiting to reach ending temperature"
                
    # Now hang out and wait for the bath temperature to get close to the ending
    # temperature
    flag = False
    while flag != True:
        time.sleep(1)
        bath.write("RT\r") # Query current bath temperature
        response = float(bath.readline())
        print "Current temperature: %2.2f C" % response
        if (abs(response - end_temp) < 0.05):
            print "**************************************************"
            print "**************************************************"
            print "Ending temperature reached:]"    
            print "**************************************************"
            print "**************************************************"
            flag = True
            time.sleep(2)
    # At this point the water bath should stay at the end_temp setpoint 
    # indefinitely. 
    try: 
        bath.close() # shut down serial connection
        print "Closed serial connection"
        time.sleep(5)
    except: 
        print "Serial connection failed to close"                  
        time.sleep(5)

