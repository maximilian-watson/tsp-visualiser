import random, math
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
    best_route = []

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
    route: list[tuple[int, int]]
) -> None:
    closed_route = route + [route[0]]
    x_coordinates = []
    y_coordinates = []
    for i in range(len(closed_route)):
        x_coordinates.append(closed_route[i][0])
        y_coordinates.append(closed_route[i][1])

    plt.plot(x_coordinates, y_coordinates)
    plt.scatter(x_coordinates, y_coordinates)
    for i, city in enumerate(route):
        plt.annotate(
            str(i+1),
            city,
            xytext=(5, 5),
            textcoords="offset points"
        )
    plt.scatter(
        route[0][0], 
        route[0][1], 
        marker="*",
        s=150
    )

    plt.show()

def main() -> None:
    cities = generate_cities(20)
    nearest_route = nearest_neighbour_route(cities)
    repeated_route = repeated_nearest_neighbour(cities)
    improved_route = two_opt(repeated_route)
    nearest_distance = calculate_route_length(nearest_route)
    repeated_distance = calculate_route_length(repeated_route)
    improved_distance = calculate_route_length(improved_route)
    print("Nearest Neighbour:", nearest_distance)
    print("Repeated Nearest Neighbour:", repeated_distance)
    print("Repeated + 2-opt", improved_distance)

if __name__ == "__main__":
    main()