import sys
import copy
import csv

#  modified gale-shapley:
#  initialize empty matching M
#  while some hospital h is unmatched (has slots available)
#    s <- highest priority student from h's preference list that h has not proposed to
#    if s is unmatched
#      match h to s (add to matching M)
#    else if s is matched and prefers h to current partner h'
#      remove match h' to s (remove from matching M)
#      match h to s (add to matching M)
#      add h' back to unmatched hospitals
#    mark h as having proposed to s (remove from unmatched hospitals)
#  return matching M

def gale_shapley(hospitals, students):
    # deep copy to prevent side effects from mutation
    hospitals = copy.deepcopy(hospitals)
    students = copy.deepcopy(students)
    matching = { "hospitals": {}, "students": {} }
    unmatched_hospitals = list(hospitals.keys())
    # while there are no hospitals with slots available
    while len(unmatched_hospitals) > 0:
        hospital = unmatched_hospitals[0]
        # if there is an unmatched hospital with slots available and unproposed students
        if hospitals[hospital]["slots"] > 0 and len(hospitals[hospital]["list"]) > 0:
            student = hospitals[hospital]["list"].pop(0)
            hospitals[hospital]["slots"] -= 1
            # if there is a student that is matched and prefers the proposed hospital
            if student in matching["students"] and students[student]["list"].index(hospital) < students[student]["list"].index(matching["students"][student]):
                # match the student
                hospitals[matching["students"][student]]["slots"] += 1
                unmatched_hospitals.append(matching["students"][student])
                matching["hospitals"][matching["students"][student]].remove(student)
                matching["students"][student] = hospital
                if hospital in matching["hospitals"]:
                    matching["hospitals"][hospital].append(student)
                else:
                    matching["hospitals"][hospital] = [student]
            elif student not in matching["students"]:
                # match the student
                matching["students"][student] = hospital
                if hospital in matching["hospitals"]:
                    matching["hospitals"][hospital].append(student)
                else:
                    matching["hospitals"][hospital] = [student]
            else:
                # we didn't use the slot so add it back
                hospitals[hospital]["slots"] += 1
        else:
            # there are no slots/unproposed students available, remove the unmatched hospital
            unmatched_hospitals.pop(0)
    return matching

def is_stable_matching(matching, hospitals, students):
    for student, matched_hospital in matching["students"].items():
        matched_student_index = students[student]["list"].index(matched_hospital)
        for proposed_hospital in hospitals.keys():
            if proposed_hospital != matched_hospital:
                proposed_student_index = students[student]["list"].index(proposed_hospital)
                # if the student prefers the proposed hospital to the matched hospital
                if proposed_student_index < matched_student_index:
                    # check all the proposed hospital matches to see if any are less desirable
                    for proposed_student in matching["hospitals"][proposed_hospital]:
                        matched_hospital_index = hospitals[proposed_hospital]["list"].index(student)
                        proposed_hospital_index = hospitals[proposed_hospital]["list"].index(proposed_student)
                        # if the hospital has admitted an undesirable student, we are unstable
                        if proposed_hospital_index > matched_hospital_index:
                            return False
    return True

def read_input_file(input_file):
    def strip(item):
        return item.strip()

    hospitals = {}
    students = {}
    with open(input_file, 'r', newline='') as csv_file:
        reader = csv.reader(csv_file)
        parsing_hospitals = True
        for row in reader:
            if not any(row):
                parsing_hospitals = False
            else:
                if parsing_hospitals:
                    hospitals[row[0].strip()] = { "slots": int(row[1]), "list": list(map(strip, row[2:])) }
                else:
                    students[row[0].strip()] = { "list": list(map(strip, row[1:])) }
    return hospitals, students

def write_output(matching):
    for key, val in matching["hospitals"].items():
        print(key, *val, sep=", ")

if len(sys.argv) < 2:
    print("EXPECTED: python assignment_1.py INPUT_FILE")
    sys.exit(1)

input_file = sys.argv[1]
hospitals, students = read_input_file(input_file)
matching = gale_shapley(hospitals, students)
if is_stable_matching(matching, hospitals, students):
    print("The matching is stable.")
else:
    print("The matching is not stable.")
write_output(matching)
