# Thermobath
Uses Python to control temperature of a Thermo Scientific Haake AC 200 waterbath
requires pyserial module

thermobath_v1.py gives choice of

0. constant temp
1. go to initial temp, then start ramp to target temp at user-defined heating/cooling rates
2. same as 1. but start ramp to target immediately

thermobath_csv_v1.py reads a .csv file with target temperatures that update every minute, allowing 
any desired temperature profile to be created. Used time of day to determine which row of .csv file
to read setpoint from. 

thermobath_csv_multi_v1.py is same as previous, but allows user to specify unique temperature profiles for 01...0n water baths hooked up via USB serial port to the same computer. 
