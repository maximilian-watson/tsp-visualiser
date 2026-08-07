import random, math

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

def main() -> None:
    cities = generate_cities(20)

    for index, city in enumerate(cities, start=1):
        print(f"City {index}: {city}")

    first_city = (0, 0)
    second_city = (3, 4)

    distance = calculate_distance(first_city, second_city)
    print(f"Distance: {distance}")

    test_route = [(0, 0), (3, 0), (3, 4)]
    route_length = calculate_route_length(test_route)
    print(f"Route Length: {route_length}")

    current_city = (0, 0)
    unvisited_cities = [(10, 0), (3, 4), (2, 0)]

    nearest = find_nearest_city(current_city, unvisited_cities)
    print(nearest)

if __name__ == "__main__":
    main()