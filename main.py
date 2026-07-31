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

def main() -> None:
    cities = generate_cities(20)

    for index, city in enumerate(cities, start=1):
        print(f"City {index}: {city}")

    first_city = (0, 0)
    second_city = (3, 4)

    distance = calculate_distance(first_city, second_city)
    print(f"Distance: {distance}")

if __name__ == "__main__":
    main()