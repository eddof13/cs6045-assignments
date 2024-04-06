#Skyline Problem Solution
import csv

def read_buildings(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        # Adjusting to match the input order: height, left x-coordinate, right x-coordinate
        buildings = [(int(row[1]), int(row[2]), int(row[0])) for row in reader]  # (Lxi, Rxi, Hi)
    return buildings

def write_buildings(skyline, output_file_path):
    with open(output_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        for point in skyline:
            writer.writerow([point[1], point[0]])  # Swapping order: height before x-coordinate

def skylines(buildings):
    if not buildings:
        return []
    if len(buildings) == 1:
        l, r, h = buildings[0]
        return [(l, h), (r, 0)]  # Correctly represent a single building's silhouette
    mid = len(buildings) // 2
    leftSkyline = skylines(buildings[:mid])
    rightSkyline = skylines(buildings[mid:])
    return merge(leftSkyline, rightSkyline)

def merge(left, right):
    heightLeft = heightRight = 0
    indexLeft = indexRight = 0
    merged = []
    currentHeight = 0
    while indexLeft < len(left) and indexRight < len(right):
        if left[indexLeft][0] < right[indexRight][0]:
            x, heightLeft = left[indexLeft]
            indexLeft += 1
        elif left[indexLeft][0] > right[indexRight][0]:
            x, heightRight = right[indexRight]
            indexRight += 1
        else:
            x, heightLeft = left[indexLeft]
            _, heightRight = right[indexRight]
            indexLeft += 1
            indexRight += 1
        maxHeight = max(heightLeft, heightRight)
        if maxHeight != currentHeight:
            merged.append((x, maxHeight))
            currentHeight = maxHeight
    # Append any remaining points
    merged.extend(left[indexLeft:])
    merged.extend(right[indexRight:])
    # Filter out consecutive points with the same height to finalize the skyline
    finalSkyline = [merged[0]]
    for point in merged[1:]:
        if point[1] != finalSkyline[-1][1]:
            finalSkyline.append(point)
    return finalSkyline

filename1In = 'input.csv'
filename2In= 'input2.csv'
filename3In='input3.csv'
filename1Out = 'output.csv'
filename2Out = 'output2.csv'
filename1Out = 'output3.csv'

buildings = read_buildings(filename1In)
sky = skylines(buildings)
write_buildings(sky, filename1Out)
print("Skyline has been successfully written to", filename1Out)
