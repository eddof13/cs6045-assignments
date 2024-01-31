""" The stable matching algorithm peformed by this interpretation works as follows: A list of hospitals and residents is read from a CSV file 
this list is then parsed to generate two seperate arrays, one with the data for hospitals, and one with the data for residents.

The gale shapely algorithm starts with a list of hosiptials, for each hospital it proposes a spot to their top choice for resident. If the resident is currently unmatched,
the resident accepts unconidtionally. If the resident is already matched with another hospital this function checks if the resident the proposed hospital to their currently
matched hospital. If the resident does prefer the proposed hospital to its current match, it breaks its existing match, leaving the old hospital unmatched. 
Since hospitals always nominate their top picks first, the hospitals will always prefer their current matches over other students. This code runs until all hospitals have
all their slots filled.  
 """

import csv

def read_csv_split_arrays(filename):
    '''This function takes a file name in the current directory as an input and outputs two arrays, one for the hospital matching requirements, and one of the residents'''
    array1 = []
    array2 = []
    with open(filename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        current_array = array1
        for row in reader:
            if not any(row):
                current_array = array2
            else:
                current_array.append(row)
    return array1, array2

def ResParse (ResidentArrayLineItem):
    '''Takes a single row of resident information and formats it such that it can be input into a dictionary'''
    residentId=ResidentArrayLineItem[0]
    requests=[]
    for element in ResidentArrayLineItem[1:]:#removes spaces from being in names, important when sorting
        element=element.strip()
        requests.append(element)
    formattedarray=[residentId,requests]
    return formattedarray

def ResidentsDict(ResidentArray):
    '''Creates a dictionary of resident item, takes an array of resident data as input and outputs the dictionary, as well as an array of resident names so searching can be easier
    The residents for the output are sorted alphabetically for quicker searching'''
    students=[]
    studentNames=[]
    for resident in ResidentArray:
        SingleRes=ResParse(resident)
        studentlineitem={'name':SingleRes[0], 'prefs':SingleRes[1], 'matched':False}
        students.append(studentlineitem)
        studentNames.append(SingleRes[0])
    students=sorted(students, key=lambda d: d['name']) #sorts students by name to find them easier. 
    studentNames=sorted(studentNames)
    return students,studentNames

def hosParse (singularHospital):
    '''Parses and formats a single line of hospital data so that it can be input into the hospital dictionary'''
    hospitalID=singularHospital[0]
    hospitalSlots=singularHospital[1]
    hospitalPrefs=[]
    for element in singularHospital[2:]:#removes spaces from being in names
        element=element.strip()
        hospitalPrefs.append(element)
    formattedoutput=[hospitalID,hospitalSlots,hospitalPrefs]
    return formattedoutput

def HospitalDict(HospitalArray):
    '''Creates a dictionary from hospital data, the input is a an array of hospital information, '''
    hospices=[]
    for hospital in HospitalArray:
        SingleHospital=hosParse(hospital)
        hospitalLineItem={'name':SingleHospital[0], "slots":int(SingleHospital[1]),"prefs":SingleHospital[2],'slotsfilled':int("0"),"atCapacity":False}
        hospices.append(hospitalLineItem)
    return hospices

# Define the Gale-Shapley algorithm function
def gale_shapley(hospitals, students,studentIDs):
    # Initialize a dictionary to store the current matches
    matches = {}

    # While there are unmatched hospitals
    while any(not hospital['atCapacity'] for hospital in hospitals):
        # Iterate over each hospital
        for hospital in hospitals:
            if not hospital['atCapacity']:
                # Find the most preferred student who has not yet been matched to this hospital
                for student_name in hospital['prefs']:
                    residentNumber=studentIDs.index(student_name)
                    studentSingular=students[residentNumber]
                    if student_name not in matches:
                        # Mark the student as matched
                        matches[student_name] = hospital['name']
                        hospital['slotsfilled'] += 1
                        hospital['prefs'].pop(0)
                        studentSingular['matched']=True
                        
                        # Check if the hospital has reached its capacity
                        if hospital['slotsfilled'] == hospital['slots']:
                            hospital['atCapacity'] = True
                        break
                    else:
                        current_match_hospital = matches.get(student_name)
                        # Check if the current hospital is more preferred by the student than the already matched hospital
                        if studentSingular['prefs'].index(hospital.get('name')) < studentSingular['prefs'].index(current_match_hospital):
                            # Mark the previous hospital as not at capacity if needed
                            for h in hospitals:
                                if h['name'] == current_match_hospital:
                                    h['atCapacity'] = False
                                    h['slotsfilled'] -= 1
                                    break
                            
                            # Update the match
                            matches[student_name] = hospital['name']
                            hospital['slotsfilled'] += 1
                            
                            # Check if the hospital has reached its capacity
                            if hospital['slotsfilled'] == hospital['slots']:
                                hospital['atCapacity'] = True
                            break
                        else:#stops attemping to match with student who isnt interested. 
                            hospital['prefs'].pop(0)
                            break

    return matches

def StableMatching(matches, hospitals, students):
    for hire in matches:
        currentHospital=matches.get(hire) #store the currently matched hospital
        for hospital in hospitals.keys(): #iterates through list of key values for hospitals 
            if currentHospital==hospital: 
                pass



filename="inputs.csv"
output="output.csv"
HospitalsArrary,ResidentsArray=read_csv_split_arrays(filename)

Students,StudentNames=ResidentsDict(ResidentsArray)
hospitals=HospitalDict(HospitalsArrary)

# Call the Gale-Shapley algorithm function
match = gale_shapley(hospitals, Students,StudentNames)
print(StableMatching(match,hospitals, Students))
# Write the stable matching to a CSV file
with open(output, mode='w', newline='') as csvfile:
    writer = csv.writer(csvfile)
       # Write the stable matching by hospital
    for hospital in hospitals:
        matched_students = [student for student, matched_hospital in match.items() if matched_hospital == hospital['name']]
        writer.writerow([hospital['name']] + matched_students)