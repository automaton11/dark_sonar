'''
Dark Sonar v.1                                                                                                                                                                                                                                                                                                                                      
                                                               
opens each .txt file in folder_path and extracts relevant fields to dictionary

FIELDS EXTRACTED:

HOST NAME
OS NAME
SERIAL NUMBER
DATE
USERNAME
SESSION NAME
ID NUMBER
STATE
IDLE TIME
LOGON TIME
'''

emblem = '''

 ____             _      ____                         
|  _ \  __ _ _ __| | __ / ___|  ___  _ __   __ _ _ __ 
| | | |/ _` | '__| |/ / \___ \ / _ \| '_ \ / _` | '__|
| |_| | (_| | |  |   <   ___) | (_) | | | | (_| | |   
|____/ \__,_|_|  |_|\_\ |____/ \___/|_| |_|\__,_|_|   


'''
                                                                                                                                                           
# get them modules
import os
import re
import time

# import data from Workstations folder into a dictionary object
def load_user_data():
    start_time = time.time()

    folder_path = "S:\Group_Policy\Hardware\Workstations"
    workstations = []

    # Get list of all files in the folder
    files = os.listdir(folder_path)

    # Process each file to get extended file path
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        work_dict = {}
        
        with open(file_path, 'r') as file:
            # pre-regex, grab the serial number
            # variables have _ser suffix to distinguish from code later on
            # once working, clean this up with clear variable names
            serial_line = 0
            serial_pattern = re.compile(r'S.*?e.*?r.*?i.*?a.*?l.*?N.*?u.*?m.*?b.*?e.*?r')
            for line_number_ser, line_ser in enumerate(file, start=1):
                if serial_pattern.search(line_ser):
                    #print(f'Match found on line {line_number_ser}: {line_ser.strip()}')
                    serial_line = line_number_ser + 2
                if line_number_ser == serial_line:
                    # this line prints each serial for testing, but is commented out for function
                    #print(line_ser.strip())
                    # Add the serial number to the dictionary as 'serialnum'
                    work_dict['serialnum'] = line_ser.strip()
            
        with open(file_path, 'r') as file:
            document = file.read()

            # Do regex stuff here
            # Save each entry to a dictionary, which will appended to a list of dictionaries

            # Easy to grab patterns
            patterns = {
                "hostname": r"Host Name:\s+(.*)",
                "osname": r"OS Name:\s+(.*)",
                "date": r"Date:\s+(\d{4}-\d{2}-\d{2})\s+Time:\s+(\d{1,2}:\d{2}:\d{2})",
            }

            data = {}
            for field, pattern in patterns.items():
                match = re.search(pattern, document)
                if match:
                    data[field] = match.group(1).strip() if match.lastindex == 1 else match.groups()

            # Add extracted data to dictionary
            for field, value in data.items():
                work_dict[field] = value

            '''
            # Print the extracted data (leave print block for testing)
            for field, value in data.items():
                print(f"{field}: {value}")
            '''

            # Get second to last line by iterating through lines in document
            lines_of_interest = []

            for line in document.split('\n'):
                if line.startswith(">"):
                    lines_of_interest.append(line)

            # Set line of interest to single value, in a sloppy way
            for line in lines_of_interest:
                line_of_interest = line

            # Split the line into individual components
            components = line_of_interest.split()

            # Extract specific pieces of information
            username = components[0][1:]  # Remove the leading ">"
            session_name = components[1]
            id_number = components[2]
            state = components[3]
            idle_time = components[4]
            logon_time = " ".join(components[5:])  # Join the remaining components for logon time

            # Add extracted info to dictionary
            work_dict['username'] = username
            work_dict['sessionname'] = session_name
            work_dict['ID'] = id_number
            work_dict['state'] = state
            work_dict['idletime'] = idle_time
            work_dict['logontime'] = logon_time

            '''
            # Print the extracted information
            print("Username:", username)
            print("Session Name:", session_name)
            print("ID:", id_number)
            print("State:", state)
            print("Idle Time:", idle_time)
            print("Logon Time:", logon_time)
            '''

            workstations.append(work_dict)
            '''
            # test block, prints dictionary
            for key, value in work_dict.items():
                print(f"{key}: {value}")
            print(f"\n\n")
            '''

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Data loaded. Execution time: {execution_time} seconds\n")

    return workstations

def serial_search(workstations):
    """
    Search dictionary by serial number
    """
    serialnum = input("Enter serial number: ").strip()
    #print_ascii_values(serialnum)
    for entry in workstations:
        if 'serialnum' in entry and entry['serialnum'] is not None:
            if entry['serialnum'] == serialnum:
                print(f"found: {entry['serialnum']} for username: {entry['username']} on host: {entry['hostname']}")
                #print_ascii_values(entry['serialnum'])
        
def user_search(workstations):
    """
    Search dictionary by username
    """
    username = input("Enter username: ").strip()
    for entry in workstations:
        if 'username' in entry and entry['username'] is not None:
            if entry['username'] == username:
                    print(f"found: {entry['username']} for serialnum: {entry['serialnum']} on host: {entry['hostname']}")

def host_search(workstation):
    """
    Search dictionary by hostname
    """
    hostname = input("Enter host name: ")
    for entry in workstation:
        if 'hostname' in entry and entry['hostname'] is not None:
            if entry['hostname'] == hostname:
                print(f"found: {entry['hostname']} with serialnum: {entry['serialnum']} for user: {entry['username']}")
    
def print_ascii_values(s):
    """
    Test function, prints each character as an ASCII value to diagnose errors
    """
    for char in s:
        print(f"Character: {char}, ASCII Value: {ord(char)}")

def remove_null_spaces_and_extra_spaces(s):
    """ 
    Removes null characters and spacing issues with serial number field 
    """
    if s is not None:
        cleaned_string = re.sub(r'\s+', ' ', s.replace('\0', '').strip())
        return cleaned_string
    
def clean_serialnum_values(workstations):
    """
    Serialnum field is created with null characters and spaces.
    Calls function to remove problem characters and replaces entry with cleaned version.
    """
    for entry in workstations:
        if 'serialnum' in entry and entry['serialnum'] is not None:
            cleaned_serialnum = remove_null_spaces_and_extra_spaces(entry['serialnum'])
            entry['serialnum'] = cleaned_serialnum

def print_key_value_pairs(workstations):
    """
    Test function. Prints Key - Value pairs in Workstations.
    """
    for entry in workstations:
        value = entry.get('serialnum')
        value2 = entry.get('hostname')
        value_type = type(value).__name__
        print(f"Key: 'serialnum', Value: {value}, Type: {value_type}")
        print(f"Key: 'hostname: {value2}")

def main():
    """
    main
    """
    print(emblem)
    print("Dark Sonar v.1")
    print(f"SEARCH CRITERIA:\nusername\nserialnum\nhostname\n")
    print("To end the program, type 'exit'\n")
    print("***Please wait, loading data***\n")

    workstations = load_user_data()
    clean_serialnum_values(workstations)
    #print_key_value_pairs(workstations)

    search_options = {
        'username' : user_search, 
        'serialnum': serial_search,
        'hostname': host_search
        }
    
    while True:
        selection = input("Please enter a search criteria: ")
        if selection == 'exit':
            break

        if selection in search_options.keys():
            selected_func = search_options.get(selection)
            selected_func(workstations)           
        else:
            print("Please select a viable search criteria\n")

main()