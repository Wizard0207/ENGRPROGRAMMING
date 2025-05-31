#!/usr/bin/env python
# coding: utf-8

# In[149]:


##This is the first version of the basic downforce equation.
##Written by Lachlan Knighton
##No integration with other tools. 

##Float function: Determines if inputs are strings, or can be converted into floats
##Used to insure only valid inputs are used 
def is_it_a_float(value_of_input):
    replaced_float = value_of_input.replace('.','',1).isdigit() 
    ##Replace function can be used, as values of inputs are always strings
    ## First '.' searches for '.' in input, and converts to ''
    ## The step of 1 ensures that only one decimal is replaced
    ## isdigit checks if the remaining components are all digits
    if replaced_float == True: ##Checking if all characters are digits after replacement
        converted_float = float(value_of_input) ##As all characters are digits, result is converted to float
        return True ##Main program is returned confirmation of valid status
    else: ##If input does not provide replaced_float == True
        return False ##Main function is notified of incorrect input
## space
def first_downforce_function():
    print('*************')
    print('Downforce Function V1')
    print('This function will calculate the downforce at a given speed, based off given variables.')
    print('')
    print('Firstly, what air temperature will you be racing at?') 
    print('Enter B1 for The Bend Motorsport Park temperature. Enter C1 for Collingrove Hillclimb Circuit. Enter M1 for Mallala Motorsports Park.')
    print('Or, enter a custom air temperature.')
    air_temp_count = 0 ##Count variable used to ensure loop repeats until valid input given
    while air_temp_count < 1:
        air_temp_input = input('Enter Air temperature in degrees celsius.') #"Input" variable to be used in if-elif statements to 
        if air_temp_input == "B1":
            air_temp = 25 ##TO BE REPLACED with Tailem Bend temperature plugin.
            air_temp_count = air_temp_count+1 ##Upon valid input, count is increased, breaking the loop
            print("Your chosen air temperature is %.2f degrees (The Bend current temperature)." %(air_temp))
        elif air_temp_input == "C1":
            air_temp = 24 ##TO BE REPLACED with Collingrove temperature plugin.
            air_temp_count = air_temp_count+1
            print("Your chosen air temperature is %.2f degrees (Collingrove current temperature)." %(air_temp))
        elif air_temp_input == "M1":
            air_temp = 23 ##TO BE REPLACED with Mallala temperature plugin.
            air_temp_count = air_temp_count+1
            print("Your chosen air temperature is %.2f degrees (Mallala current temperature)." %(air_temp))
        elif is_it_a_float(air_temp_input) == True: ##Checking if input is able to be used
            air_temp = float(air_temp_input)
            air_temp_count = air_temp_count+1
            print("Your chosen air temperature is %.2f degrees (Custom Input)." %(air_temp))
        else: ##Input is not valid, and count is not increased, causing loop to restart until valid option given
            print("Invalid value. Please input new value.")
    print('')
    print('')
    print('Please enter your coefficient of lift. If unsure, leave this field blank.') ##Blank field is to use default value of 1
    clift_count = 0 ##As with air temp function
    while clift_count <1:
        clift_input = input('Coefficient of lift:')
        if is_it_a_float(clift_input) == True: ##Checking for valid result
            clift = float(clift_input)
            clift_count = clift_count+1
            print('Your coefficient of lift is equal to %.2f (custom input).' %(clift))
        elif clift_input == '':
            clift = 1
            clift_count = clift_count+1
            print('Your coefficient of lift is equal to %.2f (standard).' %(clift))
        else:
            print("Invalid value. Please input new value.")
    print('')
    print('')
    print('Next, the surface area of your spoiler is required.')
    print('Please input the surface area of your spoiler in centimetres squared.')
    area_count = 0
    while area_count < 1:
        area_input = input("Area of spoiler:")
        if is_it_a_float(area_input) == True: ##Checking for valid result
            spoilerareacm2 = float(area_input) ##Converting area in cm^2 to float
            spoilerarea = (spoilerareacm2)/(929) ##Conversion from cm^2 to feet squared. This is required for the equation.
            area_count = area_count+1
            print('The area of your spoiler is equal to %.2f centimetres squared.' %(spoilerareacm2))
        else:
            print("Invalid value. Please input new value.")
    print('')
    print('')
    print('Finally, the speeds you will be travelling at are required.')
    print('Please input the speed you want to test, in kilometres per hour.')
    velocity_count = 0
    while velocity_count < 1:
        velocity_input = input("Speed:")
        if is_it_a_float(velocity_input) == True: ##Checking for valid result
            velocitykmh = float(velocity_input) ##Converting velocity in km/h to float
            velocity = (velocitykmh)/(1.097) ##Conversion from km/h to feet per second. This is required for the equation.
            velocity_count = velocity_count+1
            print('Your chosen speed is %.2f km/h.' %(velocitykmh))
        else:
            print("Invalid value. Please input new value.")
    print('')
    print('')
    print('Calculating equation...')
    print('Equation used:')
    print('1/2 air density multiplied by area, multiplied by coefficient of lift, multiplied by velocity squared.') ##Clarifying equation
    Air_density = (1013.25/100)/((287)*(air_temp)) #Air density equation, as air density was not an input
    print('Your air density factor is %.5f.' %(Air_density)) ##Additional decimal places as factor is quite small
    print('')
    print('Calculation of downforce:')
    downforce_lbs = (0.5*(Air_density))*(spoilerarea)*(clift)*(velocity)**2 ##Usage of equation, using imperial measurements, providing imperial result
    downforce_kg = (downforce_lbs)*(2.205) ##Conversion of imperial to metric units (pounds to kilograms)
    print('Your spoiler will generate %.2f kilograms of downforce at %.2f kilometres per hour.' %(downforce_kg,velocitykmh))
    print('Please restart program to test further values.')
    print('Finished.')

