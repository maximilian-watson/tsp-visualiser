import random

def generate_cities(number_of_cities: int) -> list[tuple[int, int]]:
    """Generate random coordinates representing cities."""
    return [
        (random.randint(0, 100), random.randint(0, 100))
        for _ in range(number_of_cities)
    ]

def main() -> None:
    cities = generate_cities(20)

    for index, city in enumerate(cities, start=1):
        print(f"City {index}: {city}")

if __name__ == "__main__":
    main()