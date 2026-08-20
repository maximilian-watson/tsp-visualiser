import random, math, itertools, time
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
) -> tuple[float, float, float , float]:
    optimal_total = 0.0
    nearest_total = 0.0
    repeated_total = 0.0
    improved_total = 0.0

    optimal_time_total = 0.0
    nearest_time_total = 0.0
    repeated_time_total = 0.0
    two_opt_time_total = 0.0
    for _ in range(number_of_trials):
        cities = generate_cities(number_of_cities)

        start_time = time.perf_counter()
        optimal_route = brute_force_route(cities)
        end_time = time.perf_counter()
        optimal_time_total += end_time - start_time

        start_time = time.perf_counter()
        nearest_route = nearest_neighbour_route(cities)
        end_time = time.perf_counter()
        nearest_time_total += end_time - start_time

        start_time = time.perf_counter()
        repeated_route = repeated_nearest_neighbour(cities)
        end_time = time.perf_counter()
        repeated_time_total += end_time - start_time

        start_time = time.perf_counter()
        improved_route = two_opt(repeated_route)
        end_time = time.perf_counter()
        two_opt_time_total += end_time - start_time

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

    optimal_time = optimal_time_total / number_of_trials
    nearest_time = nearest_time_total / number_of_trials
    repeated_time = repeated_time_total / number_of_trials
    two_opt_time = two_opt_time_total / number_of_trials

    improved_time = repeated_time + two_opt_time

    print(f"Optimal Average: {optimal_average:.2f}")
    print(f"Nearest Neighbour Average: {nearest_average:.2f}")
    print(f"Repeated Nearest Neighbour Average: {repeated_average:.2f}")
    print(f"Repeated + 2-opt Average: {improved_average:.2f}")

    print(f"Nearest Neighbour above optimal: {nearest_to_optimal:.2f}%")
    print(f"Repeated Nearest Neighbour above optimal: {repeated_to_optimal:.2f}%")
    print(f"Repeated + 2-opt above optimal: {improved_to_optimal:.2f}%")

    print(f"Optimal time: {optimal_time:.5f}s")
    print(f"Nearest time: {nearest_time:.5f}s")
    print(f"Repeated time: {repeated_time:.5f}s")
    print(f"2-opt time: {two_opt_time:.5f}s")
    print(f"Repeated + 2-opt time: {improved_time:.5f}s")

    return optimal_time, nearest_time, repeated_time, improved_time


def plot_runtime_scaling(
    city_counts: list[int],
    optimal_times: list[float],
    nearest_times: list[float],
    repeated_times: list[float],
    improved_times: list[float]
) -> None:
    plt.plot(city_counts, optimal_times, marker="o", label="Brute Force")
    plt.plot(city_counts, nearest_times, marker="o", label="Nearest Neighbour")
    plt.plot(city_counts, repeated_times, marker="o", label="Repeated NN")
    plt.plot(city_counts, improved_times, marker="o", label="Repeated NN + 2-opt")

    plt.xlabel("Number of Cities")
    plt.ylabel("Average Runtime (seconds)")
    plt.title("TSP Algorithm Runtime Scaling")

    plt.yscale("log")
    plt.xticks(city_counts)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def run_heuristic_timing_experiment(
    number_of_trials: int, 
    number_of_cities: int
) -> tuple[float, float, float]:
    nearest_time_total = 0.0
    repeated_time_total = 0.0
    two_opt_time_total = 0.0

    for _ in range(number_of_trials):
        cities = generate_cities(number_of_cities)

        start_time = time.perf_counter()
        nearest_neighbour_route(cities)
        end_time = time.perf_counter()
        nearest_time_total += end_time - start_time

        start_time = time.perf_counter()
        repeated_route = repeated_nearest_neighbour(cities)
        end_time = time.perf_counter()
        repeated_time_total += end_time - start_time

        start_time = time.perf_counter()
        two_opt(repeated_route)
        end_time = time.perf_counter()
        two_opt_time_total += end_time - start_time

    nearest_time = nearest_time_total / number_of_trials
    repeated_time = repeated_time_total / number_of_trials
    two_opt_time = two_opt_time_total / number_of_trials

    improved_time = repeated_time + two_opt_time

    return nearest_time, repeated_time, improved_time


def plot_heuristic_runtime_scaling(
    city_counts: list[int],
    nearest_times: list[float],
    repeated_times: list[float],
    improved_times: list[float]
) -> None:
    plt.figure()

    plt.plot(
        city_counts,
        nearest_times,
        marker="o",
        label="Nearest Neighbour"
    )

    plt.plot(
        city_counts,
        repeated_times,
        marker="o",
        label="Repeated Nearest Neighbour"
    )

    plt.plot(
        city_counts,
        improved_times,
        marker="o",
        label="Repeated NN + 2-opt"
    )

    plt.xlabel("Number of Cities")
    plt.ylabel("Average Runtime (seconds)")
    plt.title("Heuristic Runtime Scaling")

    plt.yscale("log")
    plt.xticks(city_counts)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def main() -> None:
    random.seed(42)
    city_counts = [7, 8 ,9]

    optimal_times = []
    nearest_times = []
    repeated_times = []
    improved_times = []

    for number_of_cities in city_counts:
        print(f"\n--- {number_of_cities} cities ---")
        optimal_time, nearest_time, repeated_time, improved_time = (
            run_optimal_experiments(10, number_of_cities)
        )

        optimal_times.append(optimal_time)
        nearest_times.append(nearest_time)
        repeated_times.append(repeated_time)
        improved_times.append(improved_time)

    plot_runtime_scaling(
        city_counts,
        optimal_times,
        nearest_times,
        repeated_times,
        improved_times
    )

    large_city_counts = [10, 20, 50, 100]

    large_nearest_times = []
    large_repeated_times = []
    large_improved_times = []

    for number_of_cities in large_city_counts:
        print(f"\n--- {number_of_cities} cities ---")

        nearest_time, repeated_time, improved_time = (
            run_heuristic_timing_experiment(5, number_of_cities)
        )

        large_nearest_times.append(nearest_time)
        large_repeated_times.append(repeated_time)
        large_improved_times.append(improved_time)

        print(f"Nearest time: {nearest_time:.8f}s")
        print(f"Repeated time: {repeated_time:.8f}s")
        print(f"Repeated + 2-opt time: {improved_time:.8f}s")

    plot_heuristic_runtime_scaling(
        large_city_counts,
        large_nearest_times,
        large_repeated_times,
        large_improved_times
    )

    
if __name__ == "__main__":
    main()