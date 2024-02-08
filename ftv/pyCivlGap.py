import numpy as np

# Data definitions

# Task definitions
nominal_distance = 60.0 # km
minimum_distance = 3.0 # km
nominal_goal = 0.3 # percent
nominal_time = 90 # min

# Pilot results

# Pilot distances
distances_pilots_in_goal = [83.38]*21
distances_med_pilots = [59, 59, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 53, 56, 53, 53, 53, 53, 53, 52, 52, 52, 52, 52] + [52]*33 + [51]*26
distances_other_pilots = [50]*14 + [44, 43, 39, 38, 37, 34, 29, 28, 28, 24, 9, 7, 3, 3]
distances = distances_pilots_in_goal + distances_med_pilots + distances_other_pilots

# Validities

# Distance Validity
sum_of_flown_distances_over_min_distances = np.sum([d - minimum_distance for d in distances])
avg_of_flown_distances_over_min_distances = np.mean([d - minimum_distance for d in distances])
print(avg_of_flown_distances_over_min_distances)

a = (nominal_goal+1.0)*(nominal_distance-minimum_distance)
b = max(0, nominal_goal*(max(distances)-nominal_distance))
print('a', a, 'b', b)
nominal_distances_area = (a + b)/2.0
print('nominal_distances_area', nominal_distances_area)

dvr = avg_of_flown_distances_over_min_distances / nominal_distances_area
distance_validity = min(1.0, dvr)
print('Distance Validity:', distance_validity)

#print('statistics:')
#print((nominal_distance*(1-nominal_goal)))
#pilots_with_nominal_distances = np.array(distances) >= (nominal_distance*(1-nominal_goal))
#print('pilots with nominal distance area:', pilots_with_nominal_distances.sum()/len(distances))

# computation task 2
task2_distance = 59.7
a = (nominal_goal+1.0)*(nominal_distance-minimum_distance)
b = max(0, nominal_goal*(task2_distance-nominal_distance))
print('a', a, 'b', b)
nominal_distances_area = (a + b)/2.0
print('nominal_distances_area task2', nominal_distances_area)

# Estimate time, leading and distance points
