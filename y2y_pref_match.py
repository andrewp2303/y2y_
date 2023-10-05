# usage: python y2y_pref_match.py

import csv
import networkx as nx

# Define the goal number of volunteers per shift type
N_MEAL_VOLS = 6
N_EVENING_VOLS = 4
N_OVERNIGHT_VOLS = 2

# Define the CSV file locations
PREF_CSV = 'y2y_preferences_f23.csv'
MATCHING_CSV = 'y2y_matching_f23.csv'

# Read the CSV file (check example file for format)
with open(PREF_CSV, 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    rows = list(reader)

# Extract relevant columns
volunteers = {}
for row in rows:
    first_name = row[0]
    last_name = row[1]
    preferences = row[4:10]
    true_preferences = []
    for idx, preference in enumerate(preferences):
        if preference != '':
            true_preferences.append(preference)
    if f"{first_name} {last_name}" in volunteers.keys():
        print(f"Duplicate: {first_name} {last_name}")
    if len(true_preferences) > 0 and "Test" not in first_name:
        volunteers[f"{first_name} {last_name}"] = true_preferences
    else:
        print(f"Skipping {first_name} {last_name}")

# Create the graph
G = nx.Graph()

# Add a node to the graph for each volunteer
for volunteer in volunteers.keys():
    G.add_node(volunteer)

print(f"num unique volunteers: {len(volunteers.keys())}")
    

# Define the days and types of shifts, and combine them into shift names
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
shift_types = ['Breakfast', 'Dinner', 'Overnight', 'Evening']
shifts = [day + ' ' + shift_type for day in days for shift_type in shift_types]

# Add nodes to the graph for each shift, and each slot within a shift
for shift in shifts:
    if "Breakfast" in shift or "Dinner" in shift:
        for i in range(N_MEAL_VOLS): 
            G.add_node(f"{shift} {str(i + 1)}")
    elif "Evening" in shift:
        for i in range(N_EVENING_VOLS):
            G.add_node(f"{shift} {str(i + 1)}")
    else:
        for i in range(N_OVERNIGHT_VOLS):
            G.add_node(f"{shift} {str(i + 1)}")

# Add edges to the graph
# (edges connect a volunteer to all shifts they ranked, weighted using their ordering)
for volunteer in volunteers.keys():
    for w, preference in enumerate(volunteers[volunteer]):
        if "Breakfast" in preference or "Dinner" in preference:
            for i in range(N_MEAL_VOLS): 
                G.add_edge(volunteer, preference + ' ' + str(i + 1), weight=w)
        elif "Evening" in preference:
            for i in range(N_EVENING_VOLS):
                G.add_edge(volunteer, preference + ' ' + str(i + 1), weight=w)
        else:
            for i in range(N_OVERNIGHT_VOLS):
                G.add_edge(volunteer, preference + ' ' + str(i + 1), weight=w)

# Define all nodes that refer to a shift, not a volunteer (one side of bipartite graph)
shift_nodes = set([n for n in G.nodes if "Breakfast" in n or "Dinner" in n or "Evening" in n or "Overnight" in n])

# Find the minimum-weight full matching using rectangular linear assignment
# (e.g. the matching of volunteers to shifts that they prefer)
matching = nx.algorithms.bipartite.minimum_weight_full_matching(G, top_nodes=shift_nodes)

# Convert matching into a dictionary from shift: [person1, person2, ...]
matching_dict = {}
for node1, node2 in matching.items():

    # Check if any of days are in node1
    if any(day in node1 for day in days):
        shift = node1
        volunteer = node2
    else:
        shift = node2
        volunteer = node1
    shift = shift[:-2]
    if shift not in matching_dict:
        matching_dict[shift] = []
    if volunteer not in matching_dict[shift]:
        matching_dict[shift] += [volunteer]

# Write the matching dict to a csv 
# First column: shift day/time
# All later columns: volunteer names
with open(MATCHING_CSV, 'w') as file:
    writer = csv.writer(file)
    writer.writerow(['Shift', 'Volunteers'])
    for shift, people in matching_dict.items():
        writer.writerow([shift, *people])