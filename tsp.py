import json
import math
import argparse
from visualise_tsp import visualise_tsp

def calculate_distance(city1, city2):
    x1, y1 = city1['x'], city1['y']
    x2, y2 = city2['x'], city2['y']
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def tsp_solver(cities):
    num_cities = len(cities)
    optimal_path = []
    total_distance = 0

    # Start with the first city
    current_city_index = 0
    current_city = cities[current_city_index]
    visited_cities = [current_city_index]

    while len(visited_cities) < num_cities:
        min_distance = float('inf')
        closest_city_index = None

        for idx, city in enumerate(cities):
            if idx not in visited_cities:
                distance = calculate_distance(current_city, city)
                if distance < min_distance:
                    min_distance = distance
                    closest_city_index = idx

        optimal_path.append(closest_city_index)
        total_distance += min_distance
        visited_cities.append(closest_city_index)
        current_city_index = closest_city_index
        current_city = cities[current_city_index]

    return optimal_path, total_distance


def solve_tsp(cities):
    print("Solving TSP...")
    optimal_path_indices, min_distance = tsp_solver(cities)
    print("TSP solved.")

    # Convert indices back to city data
    optimal_path = [cities[i] for i in optimal_path_indices]

    # Add the start city to the beginning and end of the optimal path
    start_city = cities[0]
    optimal_path.insert(0, start_city)
    optimal_path.append(start_city)

    return optimal_path, min_distance


def save_result(result):
    print("Saving result...")
    with open('output_files/result.json', 'w') as f:
        # Append total_distance to the best_route list
        result['best_route'].append({'total_distance': result['min_distance']})
        json.dump(result['best_route'], f, indent=2)  # pretty-print JSON data
    print("Result saved.")


def load_input():
    print("Loading input...")
    with open('input_files/cities.json', 'r') as f:
        cities = json.load(f)
    print("Input loaded.")
    return cities


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='TSP Solver')
    parser.add_argument('--visualise', action='store_true', help='Visualise the TSP route')
    args = parser.parse_args()

    cities = load_input()
    optimal_path, min_distance = solve_tsp(cities)

    # Prepare result
    result = {
        'best_route': optimal_path,
        'min_distance': min_distance
    }

    # Save result
    save_result(result)

    # Visualize the result if the "--visualise" flag is provided
    if args.visualise:
        visualise_tsp(optimal_path, cities)
    else:
        print("To visualise the routing process, run tsp.py with the --visualise argument.")

if __name__ == '__main__':
    main()
