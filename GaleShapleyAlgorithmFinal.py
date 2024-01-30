"""
    Modified Gale-Shapley Algorithm:
    1. Initialize all residents as free.
    2. While there exists a free resident:
        a. Pick a free resident (let's say 'R').
        b. 'R' proposes to the most preferred hospital that they haven't proposed to yet.
        c. If the hospital has an available slot, 'R' is tentatively assigned to it.
        d. If the hospital is full but prefers 'R' over some assigned resident(s):
           - The least preferred resident(s) is unassigned, and 'R' takes their place.
        e. If the hospital is full and does not prefer 'R', 'R' remains free.
    3. Repeat until all residents are either assigned or have proposed to every hospital.
    """

def parse_input_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()

    hospitals = {}
    residents = {}

    # Parsing hospitals and residents
    i = 0
    while lines[i].strip():
        parts = [part.strip() for part in lines[i].split(',')]
        hospital_name = parts[0]
        slots = int(parts[1])
        preferences = parts[2:]
        hospitals[hospital_name] = {'slots': slots, 'preferences': preferences}
        i += 1

    # Skip the blank line and parse residents
    i += 1
    while i < len(lines):
        parts = [part.strip() for part in lines[i].split(',')]
        resident_name = parts[0]
        preferences = parts[1:]
        residents[resident_name] = {'preferences': preferences}
        i += 1

    return hospitals, residents

# Modified Gale-Shapley algorithm implementation
def gale_shapley(hospitals, residents):

    free_residents = list(residents.keys())   
    proposals = {resident: [] for resident in residents}  

    while free_residents:
        for resident in free_residents.copy():
            resident_prefs = residents[resident]['preferences']
            for hospital in resident_prefs:
                if hospital not in proposals[resident]:
                    proposals[resident].append(hospital)

                    if hospital in hospitals:
                        hospital_prefs = hospitals[hospital]['preferences']
                        assigned_residents = hospitals[hospital].get('assigned', [])
                        if len(assigned_residents) < hospitals[hospital]['slots']:
                            assigned_residents.append(resident)
                            hospitals[hospital]['assigned'] = assigned_residents
                            free_residents.remove(resident)
                            break
                        else:
                          # If hospital prefers this resident over currently assigned ones
                            for current_resident in assigned_residents:
                                if hospital_prefs.index(resident) < hospital_prefs.index(current_resident):
                                    assigned_residents.remove(current_resident)
                                    assigned_residents.append(resident)
                                    hospitals[hospital]['assigned'] = assigned_residents
                                    free_residents.remove(resident)
                                    if current_resident not in free_residents:
                                        free_residents.append(current_resident)
                                    break
                            break
                    else:
                        # Return None if invalid hospital name is encountered
                        return None   
    # Compile the final matching results
    matching = {hospital: hospitals[hospital].get('assigned', []) for hospital in hospitals}
    return matching

# Function to check the stability of the matching
def check_stability(hospitals, residents, matching):
     # Check for each hospital and its assigned residents
    for hospital, assigned_residents in matching.items():
        hospital_prefs = hospitals[hospital]['preferences']
        unassigned_residents = [r for r in residents if r not in assigned_residents]

        # Check for first type of instability
        for unassigned in unassigned_residents:
            for assigned in assigned_residents:
                if hospital_prefs.index(unassigned) < hospital_prefs.index(assigned):
                    return False
    # Check for second type of instability
    for resident in residents:
        if resident not in [r for sublist in matching.values() for r in sublist]:
            continue

        resident_prefs = residents[resident]['preferences']
        resident_hospital = next((hospital for hospital, residents in matching.items() if resident in residents), None)

        for other_hospital in resident_prefs:
            if resident_prefs.index(other_hospital) < resident_prefs.index(resident_hospital):
                other_hospital_residents = matching[other_hospital]
                other_hospital_prefs = hospitals[other_hospital]['preferences']

                for other_resident in other_hospital_residents:
                    if other_hospital_prefs.index(resident) < other_hospital_prefs.index(other_resident):
                        return False

    return True

# Function to format the output of the matching
def format_output(matching):
    formatted_output = []
    for hospital, residents in matching.items():
        line = f"{hospital}, " + ", ".join(residents)
        formatted_output.append(line)

    return "\n".join(formatted_output)


csv_file_path = "test4.csv"
hospitals, residents = parse_input_from_file(csv_file_path)

# Running the Gale-Shapley algorithm
matching = gale_shapley(hospitals, residents)

# Outputting the matching results
output = format_output(matching)
print("\nMatching Result:\n")
print(output)

# Checking if the matching is stable
if matching:
    is_stable = check_stability(hospitals, residents, matching)
    if is_stable:
        print("The matching is stable.")
    else:
        print("The matching is not stable.")
else:
    print("Failed to complete matching due to data issues.")




    