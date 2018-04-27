# Thermobath
Uses Python to control temperature of a Thermo Scientific Haake AC 200 waterbath
requires pyserial module. 

4 different versions of code: 

A. thermobath_v1.py gives choice of

0. constant temp
1. go to initial temp, then start ramp to target temp at user-defined heating/cooling rates
2. same as 1. but start ramp to target immediately

B. thermobath_csv_v1.py reads a .csv file with target temperatures that update every minute, allowing 
any desired temperature profile to be created. Used time of day to determine which row of .csv file
to read setpoint from. 

C. thermobath_csv_multi_v1.py is same as previous, but allows user to specify unique temperature profiles for 01...0n water baths hooked up via USB serial port to the same computer. 

D. thermobath_csv_multi_extRTD_v1.py is same as previous, but uses external RTD temperature sensors rather than the internal sensor on the waterbath. This is useful for controlling process temperature remote from the bath itself, but requires calibration of the external probes to a known temperature standard. 
