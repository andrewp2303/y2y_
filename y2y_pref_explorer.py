# Mostly written with Codeium

import csv

PREF_CSV = 'y2y_preferences_f23.csv'
MATCHING_CSV = 'y2y_matching_f23.csv'

# Step 1: Read the initial volunteer preferences CSV file
with open(PREF_CSV, 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    initial_prefs = list(reader)

# Step 2: Read the final shift matchings CSV file
with open(MATCHING_CSV, 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    final_matchings = list(reader)

# Step 3: Create a dictionary to track the number of people who got their 1st, 2nd, etc. preferences
preference_counts = {}

# Step 4: Iterate over each final shift matching
for row in final_matchings:
    shift = row[0]
    volunteers = row[1:]

    # Step 5: Iterate over each volunteer in the final shift matching
    for volunteer in volunteers:
        # Step 6: Find the corresponding initial preference for each volunteer
        person_prefs = [p[4:10] for p in initial_prefs if p[0] + ' ' + p[1] == volunteer]
        if person_prefs:
            person_prefs = person_prefs[0]

            # Step 7: Check if the volunteer's preference matches the shift they were assigned to
            if shift in person_prefs:
                preference = person_prefs.index(shift) + 1
            else:
                preference = 0

            # Step 8: Update the preference counts dictionary
            if preference not in preference_counts:
                preference_counts[preference] = 0
            preference_counts[preference] += 1

# Step 9: Print the results
for preference, count in sorted(preference_counts.items()):
    if preference == 0:
        print(f"Number of people who did not get matched: {count}")
    else:
    	print(f"Number of people who got Preference #{preference}: {count}")