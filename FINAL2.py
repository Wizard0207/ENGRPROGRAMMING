import requests
from bs4 import BeautifulSoup
import inquirer
import matplotlib.pyplot as plt
import numpy as np

def is_it_a_float(value_of_input):
    '''
    This function checks if the input is a valid float.
    '''
    replaced_float = value_of_input.replace('.', '', 1).isdigit()
    return replaced_float

def get_temperatures(location_label):
    '''
    This function fetches the current air temperature for a given location from the BOM website.
    It uses BeautifulSoup to scrape the temperature data from the BOM page for the specified location.
    It returns the temperature in Celsius and a display name for the location.
    '''
    if location_label == "Collingrove":
        location_url = "barossa"
        display_name = "Collingrove (Barossa weather station)"
    else:
        location_url = location_label.replace(" ", "-").lower()
        display_name = location_label

    url = 'https://www.bom.gov.au/places/sa/%s/' % location_url
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception("Failed to fetch data for %s: HTTP %d" % (location_label, response.status_code))

    soup = BeautifulSoup(response.text, 'html.parser')
    temp_element = soup.find('li', class_='airT')
    if not temp_element:
        raise Exception("Temperature element not found for %s." % location_label)

    temperature = temp_element.get_text(strip=True)
    numeric_temp = ''.join(c for c in temperature if (c.isdigit() or c == '.'))
    return float(numeric_temp), display_name

def calculate_downforce(air_temp, clift, spoilerarea_ft2, velocity_kmh):
    '''
    This function calculates the downforce based on air temperature, coefficient of lift,
    spoiler area in square feet, and velocity in km/h.
    It uses the formula:
    Downforce = 0.5 × Air Density × Area × Lift Coefficient × Velocity²
    The air density is calculated using the ideal gas law, assuming standard atmospheric pressure.
    The function returns the downforce in kilograms.'''
    velocity_fps = velocity_kmh / 1.097
    Air_density = (1013.25 / 100) / (287 * air_temp)
    downforce_lbs = 0.5 * Air_density * spoilerarea_ft2 * clift * velocity_fps ** 2
    downforce_kg = downforce_lbs / 2.205
    return downforce_kg

def first_downforce_function():
    '''
    This function calculates downforce based on user inputs or live weather data.
    It allows the user to choose between live track data or custom input for air temperature,
    and provides options for graphing downforce across a range of speeds or calculating it for a single speed.

    It uses the BeautifulSoup library to scrape live weather data from the BOM website,
    and matplotlib for graphing the results.
    It also includes input validation to ensure correct data types are entered by the user.

    The function prompts the user for:
    - Temperature input method (live data or custom input)
    - Track selection if using live data
    - Air temperature (either live or custom)
    - Coefficient of lift
    - Spoiler area in cm²
    - Speed for downforce calculation (if not graphing)
    It then calculates the downforce using the formula:
    Downforce = 0.5 x Air Density x Area x Lift Coefficient x Velocity²
    It can graph the downforce across speeds from 20 to 300 km/h if the user chooses that option.
    It prints the calculated downforce and optionally displays a graph of downforce vs speed.
    '''
    print('*************')
    print('Downforce Function V1 with Live Weather Integration and Graphing\n')

    questions = [
        inquirer.List('temp_mode',
                      message="Choose temperature input method:",
                      choices=['Live Track Data', 'Custom Input'])
    ]
    answer = inquirer.prompt(questions)
    use_graph = False

    if answer['temp_mode'] == 'Live Track Data':
        questions = [
            inquirer.List('track',
                          message="Select your track:",
                          choices=['Mallala', 'Collingrove', 'Tailem Bend'])
        ]
        track_answer = inquirer.prompt(questions)
        selected_track = track_answer['track']

        try:
            air_temp, display_name = get_temperatures(selected_track)
            print("Live temperature for %s: %.2f°C" % (display_name, air_temp))
        except Exception as e:
            print("Error fetching live temperature: %s" % str(e))
            return

        questions = [
            inquirer.List('mode',
                          message="Would you like a graph or a single downforce result?",
                          choices=['Graph (20–300 km/h)', 'Single speed'])
        ]
        mode_answer = inquirer.prompt(questions)
        use_graph = mode_answer['mode'] == 'Graph (20–300 km/h)'
    else:
        air_temp_count = 0
        while air_temp_count < 1:
            air_temp_input = input("Enter custom air temperature in °C: ")
            if is_it_a_float(air_temp_input):
                air_temp = float(air_temp_input)
                air_temp_count += 1
                print("Using custom air temperature: %.2f°C" % air_temp)
            else:
                print("Invalid input. Try again.")

        use_graph = False  # Default to single speed with custom

    # Coefficient of lift input
    clift_count = 0
    while clift_count < 1:
        clift_input = input("Coefficient of lift (leave blank for default = 1): ")
        if is_it_a_float(clift_input):
            clift = float(clift_input)
            clift_count += 1
            print("Using coefficient of lift: %.2f" % clift)
        elif clift_input == '':
            clift = 1
            clift_count += 1
            print("Using coefficient of lift: %.2f (default)" % clift)
        else:
            print("Invalid input. Try again.")

    # Spoiler area input
    area_count = 0
    while area_count < 1:
        area_input = input("Spoiler area in cm²: ")
        if is_it_a_float(area_input):
            spoilerareacm2 = float(area_input)
            spoilerarea = spoilerareacm2 / 929  # convert to ft²
            area_count += 1
            print("Using spoiler area: %.2f cm²" % spoilerareacm2)
        else:
            print("Invalid input. Try again.")

    if use_graph:
        print("\nGenerating downforce graph across speeds 20–300 km/h...")
        velocities = np.linspace(20, 300, 100)
        downforces = [calculate_downforce(air_temp, clift, spoilerarea, v) for v in velocities]

        plt.figure(figsize=(10, 6))
        plt.plot(velocities, downforces, label="Downforce", color='blue')
        plt.xlabel("Speed (km/h)")
        plt.ylabel("Downforce (kg)")
        plt.title("Downforce vs Speed")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()
    else:
        # Single-speed input
        velocity_count = 0
        while velocity_count < 1:
            velocity_input = input("Enter test speed in km/h: ")
            if is_it_a_float(velocity_input):
                velocitykmh = float(velocity_input)
                velocity_count += 1
                print("Using speed: %.2f km/h" % velocitykmh)
            else:
                print("Invalid input. Try again.")

        print("\nCalculating...")
        print("Equation: 0.5 × air density × area × lift coefficient × velocity²")

        Air_density = (1013.25 / 100) / (287 * air_temp)
        print("Air density: %.5f" % Air_density)

        downforce = calculate_downforce(air_temp, clift, spoilerarea, velocitykmh)
        print("Estimated downforce: %.2f kg at %.2f km/h" % (downforce, velocitykmh))

    print("Finished.")


first_downforce_function()
