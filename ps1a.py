###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """

    cows = {}
    with open(filename) as f:
        for line in f:
            cows_dict = line.strip().split(",")
            cows[cows_dict[0]] = int(cows_dict[1])
    return cows

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """

    cowsCopy = sorted(cows.items(), key=lambda x:x[1], reverse=True)
    trips = []

    while cowsCopy and cowsCopy[-1][1] < limit:
        current_weight = 0
        current_transport = []
        for cow in cowsCopy:
            if current_weight +cow[1] <= limit:
                current_transport.append(cow[0])
                current_weight += cow[1]
                cowsCopy.remove(cow)
        trips.append(current_transport)
    print(trips)
    return trips


# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """

    best_yet = None

    for partition in get_partitions(cows):
        if within_weight_limit(cows, partition, limit):
            if best_yet == None or len(partition) < len(best_yet):
                best_yet = partition

    return best_yet

def within_weight_limit(cows, partition, limit):
    for cow_set in partition:
        cow_set_weight = 0
        for cow in cow_set:
            cow_weight = cows[cow]
            cow_set_weight += cow_weight

        if cow_set_weight > limit:
            return False
    return True

        
# Problem 4
def compare_cow_transport_algorithms(filename):
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    cows = load_cows(filename)

    start = time.perf_counter()
    greedy_result = greedy_cow_transport(cows)
    end = time.perf_counter()
    print("Rusult greedy: ", greedy_result)
    print("Time: ", "{:.4f} ms ".format(end - start)*1000)

    start2 = time.perf_counter()
    brute_result = brute_force_cow_transport(cows)
    end2 = time.perf_counter()
    print("Result brute force: ", brute_result)
    print("Time: ", "{:.4f} ms ".format(end2 - start2)*1000)


if __name__ == '__main__':
    print(load_cows('ps1_cow_data.txt'))
    print(load_cows('ps1_cow_data_2.txt'))
    print(greedy_cow_transport(load_cows('ps1_cow_data.txt')))
    print(brute_force_cow_transport(load_cows('ps1_cow_data.txt')))
    print(brute_force_cow_transport(load_cows('ps1_cow_data_2.txt')))
    print(compare_cow_transport_algorithms('ps1_cow_data.txt'))
