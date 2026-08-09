from main import calculate_distance, calculate_route_length, find_nearest_city, nearest_neighbour_route, repeated_nearest_neighbour, two_opt

def test_calculate_distance():
    result = calculate_distance((0, 0), (3, 4))

    assert result == 5.0


def test_calculate_route_length():
    route = [(0, 0), (3, 0), (3, 4)]
    result = calculate_route_length(route)

    assert result == 12.0


def test_find_nearest_city():
    current_city = (0, 0)
    unvisited_cities = [(10, 0), (3, 4), (2, 0)]
    result = find_nearest_city(current_city, unvisited_cities)

    assert result == (2, 0)


def test_nearest_neighbour_route():
    cities = [(0, 0), (2, 0), (5, 0), (10, 0)]
    result = nearest_neighbour_route(cities)

    assert result == [(0, 0), (2, 0), (5, 0), (10, 0)]


def test_nearest_neighbour_route_with_no_cities():
    result = nearest_neighbour_route([])

    assert result == []


def test_repeated_nearest_neighbour():
    cities = [(0, 0), (0, 1), (0, 3), (1, 2)]
    result = repeated_nearest_neighbour(cities)

    assert result == [(0, 1), (0, 0), (1, 2), (0, 3)]


def test_two_opt_improves_crossing_route():
    route = [
        (0, 0),
        (6, 6),
        (7, 5),
        (7, 1),
        (6, 0),
        (0, 6),
    ]

    result = two_opt(route)

    assert calculate_route_length(result) < calculate_route_length(route)