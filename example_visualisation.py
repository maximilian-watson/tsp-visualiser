import random
import matplotlib.pyplot as plt

from main import(
    generate_cities,
    nearest_neighbour_route,
    repeated_nearest_neighbour,
    two_opt,
    plot_route
)

random.seed(42)

cities = generate_cities(20)

nearest_route = nearest_neighbour_route(cities)
improved_route = two_opt(repeated_nearest_neighbour(cities))

figure, axes = plt.subplots(1, 2, figsize=(12, 5))

plot_route(nearest_route, "Nearest Neighbour", axes[0])
plot_route(improved_route, "Repeated NN + 2-opt", axes[1])

plt.tight_layout()
plt.savefig("results/example_route.png", dpi=300, bbox_inches="tight")
plt.show()