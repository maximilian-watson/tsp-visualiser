from main import calculate_distance, calculate_route_length, find_nearest_city, nearest_neighbour_route

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