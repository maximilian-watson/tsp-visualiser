import random, math, itertools
import matplotlib.pyplot as plt

def generate_cities(number_of_cities: int) -> list[tuple[int, int]]:
    """Generate random coordinates representing cities."""
    return [
        (random.randint(0, 100), random.randint(0, 100))
        for _ in range(number_of_cities)
    ]

def calculate_distance(
    first_city: tuple[int, int],
    second_city: tuple[int, int],
) -> float:
    x_difference = second_city[0] - first_city[0]
    y_difference = second_city[1] - first_city[1]
    return math.hypot(x_difference, y_difference)

def calculate_route_length(route: list[tuple[int, int]]) -> float:
    total_distance = 0.0
    for index in range(len(route) - 1):
        current_city = route[index]
        next_city = route[index + 1]
        total_distance += calculate_distance(current_city, next_city)

    total_distance += calculate_distance(route[-1], route[0])
    return total_distance

def find_nearest_city(
    current_city: tuple[int, int],
    unvisited_cities: list[tuple[int, int]],
) -> tuple[int, int]:
    nearest_city = unvisited_cities[0]
    shortest_distance = calculate_distance(current_city, nearest_city)

    for city in unvisited_cities[1:]:
        distance = calculate_distance(current_city, city)

        if distance < shortest_distance:
            nearest_city = city
            shortest_distance = distance

    return nearest_city


def nearest_neighbour_route(
    cities: list[tuple[int, int]]
) -> list[tuple[int, int]]:
    if len(cities) < 1:
        return []
    current_city = cities[0]
    route = [current_city]
    unvisited_cities = cities[1:]
    while unvisited_cities:
        nearest_city = find_nearest_city(current_city, unvisited_cities)
        route.append(nearest_city)
        unvisited_cities.remove(nearest_city)
        current_city = nearest_city

    return route


def repeated_nearest_neighbour(
    cities: list[tuple[int, int]]
) -> list[tuple[int, int]]:
    best_distance = float("inf")
    for i in range(len(cities)):
        rotated_cities = cities[i:] + cities[:i]
        candidate_route = nearest_neighbour_route(rotated_cities)
        candidate_distance = calculate_route_length(candidate_route)

        if candidate_distance < best_distance:
            best_route = candidate_route
            best_distance = candidate_distance

    return best_route


def two_opt(
    route: list[tuple[int, int]]
) -> list[tuple[int, int]]: 
    distance = calculate_route_length(route)
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route) - 1):
            for j in range(i + 1, len(route)):
                before = route[:i]
                middle = route[i:j+1]
                after = route[j + 1:]
                candidate_route = before + middle[::-1] + after
                candidate_distance = calculate_route_length(candidate_route)
                if candidate_distance < distance:
                    route = candidate_route
                    distance = candidate_distance
                    improved = True
    return route


def plot_cities(
    cities: list[tuple[int, int]]
) -> None:
    x_coordinates = []
    y_coordinates = []
    for i in range(len(cities)):
        x_coordinates.append(cities[i][0])
        y_coordinates.append(cities[i][1])
    plt.scatter(x_coordinates, y_coordinates)
    plt.show()


def plot_route(
    route: list[tuple[int, int]],
    title: str,
    axis
) -> None:
    axis.set_title(title)
    closed_route = route + [route[0]]
    x_coordinates = []
    y_coordinates = []
    for i in range(len(closed_route)):
        x_coordinates.append(closed_route[i][0])
        y_coordinates.append(closed_route[i][1])

    axis.plot(x_coordinates, y_coordinates)
    axis.scatter(x_coordinates, y_coordinates)
    for i, city in enumerate(route):
        axis.annotate(
            str(i+1),
            city,
            xytext=(5, 5),
            textcoords="offset points"
        )
    axis.scatter(
        route[0][0], 
        route[0][1], 
        marker="*",
        s=150
    )


def brute_force_route(
    cities: list[tuple[int, int]]
) -> list[tuple[int, int]]:
    best_distance = float("inf")
    best_route = []
    
    for route in itertools.permutations(cities):
        current_distance = calculate_route_length(route)
        if current_distance < best_distance:
            best_route = list(route)
            best_distance = current_distance

    return best_route


def run_experiments(
    number_of_trials: int,
    number_of_cities: int
) -> None:
    nearest_total = 0.0
    repeated_total = 0.0
    improved_total = 0.0
    for trial in range(number_of_trials):
        cities = generate_cities(number_of_cities)
        nearest_route = nearest_neighbour_route(cities)
        repeated_route = repeated_nearest_neighbour(cities)
        improved_route = two_opt(repeated_route)
        nearest_distance = calculate_route_length(nearest_route)
        repeated_distance = calculate_route_length(repeated_route)
        improved_distance = calculate_route_length(improved_route)
        nearest_total += nearest_distance
        repeated_total += repeated_distance
        improved_total += improved_distance
        
    nearest_average = nearest_total / number_of_trials
    print(f"Nearest Neighbour Average: {nearest_average:.2f}")
    repeated_average = repeated_total / number_of_trials
    print(f"Repeated Nearest Neighbour Average: {repeated_average:.2f}")
    improved_average = improved_total / number_of_trials
    print(f"Repeated + 2-opt Average: {improved_average:.2f}")

    repeated_improvement = (nearest_average - repeated_average) / nearest_average * 100
    two_opt_improvement = (repeated_average - improved_average) / repeated_average * 100
    overall_improvement = (nearest_average - improved_average) / nearest_average * 100

    print(f"Repeated Nearest Neighbour Improvement: {repeated_improvement:.2f}%")
    print(f"2-opt Improvement: {two_opt_improvement:.2f}%")
    print(f"Overall Improvement: {overall_improvement:.2f}%")


def run_optimal_experiments(
    number_of_trials: int,
    number_of_cities: int
) -> None:
    optimal_total = 0.0
    nearest_total = 0.0
    repeated_total = 0.0
    improved_total = 0.0
    for trial in range(number_of_trials):
        cities = generate_cities(number_of_cities)

        optimal_route = brute_force_route(cities)
        nearest_route = nearest_neighbour_route(cities)
        repeated_route = repeated_nearest_neighbour(cities)
        improved_route = two_opt(repeated_route)

        optimal_distance = calculate_route_length(optimal_route)
        nearest_distance = calculate_route_length(nearest_route)
        repeated_distance = calculate_route_length(repeated_route)
        improved_distance = calculate_route_length(improved_route)

        optimal_total += optimal_distance
        nearest_total += nearest_distance
        repeated_total += repeated_distance
        improved_total += improved_distance

    optimal_average = optimal_total / number_of_trials
    nearest_average = nearest_total / number_of_trials
    repeated_average = repeated_total / number_of_trials
    improved_average = improved_total / number_of_trials

    nearest_to_optimal = (nearest_average - optimal_average) / optimal_average * 100
    repeated_to_optimal = (repeated_average - optimal_average) / optimal_average * 100
    improved_to_optimal = (improved_average - optimal_average) / optimal_average * 100

    print(f"Optimal Average: {optimal_average:.2f}")
    print(f"Nearest Neighbour Average: {nearest_average:.2f}")
    print(f"Repeated Nearest Neighbour Average: {repeated_average:.2f}")
    print(f"Repeated + 2-opt Average: {improved_average:.2f}")

    print(f"Nearest Neighbour above optimal: {nearest_to_optimal:.2f}%")
    print(f"Repeated Nearest Neighbour above optimal: {repeated_to_optimal:.2f}%")
    print(f"Repeated + 2-opt above optimal: {improved_to_optimal:.2f}%")

def main() -> None:
    random.seed(32)
    #run_experiments(100, 20)
    run_optimal_experiments(10, 7)

if __name__ == "__main__":
    main()