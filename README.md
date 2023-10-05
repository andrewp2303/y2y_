# Y2Y Shift Matching

A simple, single-file script to match interested Y2Y volunteers to the shifts they prefer, by reducing the problem to bipartite graph matching and solving it using a well-documented optimization algorithm.

## Getting Started

Make sure you have a csv in the format of *y2y_preferences_template.csv*. Also, feel free to adjust the desired number of people on each shift (e.g. *N_MEAL_VOLS*), or loosen these constraints in any other way. 

**It's important to note that the sum of (Shift * Goal # of people per Shift) for each shift is the *maximum* number of volunteers that will be matched, so you may need to add certain volunteers manually afterwards**

### Dependencies

Python 3, csv, networkx

### Running

```
python y2y_pref_match.py
```

## Help

Feel free to reach out to me with any questions!

Andrew Palacci [@andrewp2303](https://github.com/andrewp2303)