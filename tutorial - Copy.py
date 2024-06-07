import carla
import random
import time

# Connect to the client and retrieve the world object
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)  # Set a timeout for client commands
world = client.get_world()

# Set up the simulator in synchronous mode
settings = world.get_settings()
settings.synchronous_mode = True  # Enables synchronous mode
settings.fixed_delta_seconds = 0.02
world.apply_settings(settings)

# Set up the TM in synchronous mode
traffic_manager = client.get_trafficmanager()
traffic_manager.set_synchronous_mode(True)

# Set a seed so behaviour can be repeated if necessary
traffic_manager.set_random_device_seed(0)
random.seed(0)

actors = world.get_actors()


def get_traffic_density(traffic_light, radius=50):
    vehicles = world.get_actors().filter('vehicle.*')
    density = 0
    for vehicle in vehicles:
        if vehicle.get_location().distance(traffic_light.get_location()) < radius:
            density += 1
    return density


def set_traffic_light_state(traffic_light, state, duration):
    traffic_light.set_state(state)
    traffic_light.set_green_time(duration if state == carla.TrafficLightState.Green else 0)
    traffic_light.set_yellow_time(3.0)
    traffic_light.set_red_time(duration if state == carla.TrafficLightState.Red else 0)


def control_traffic_lights(traffic_lights, check_interval=1, density_threshold=5, green_duration=10):
    while True:
        world.tick()  # Advance the simulation by one tick
        for traffic_light in traffic_lights:
            density = get_traffic_density(traffic_light, radius=50)
            if density > density_threshold:
                set_traffic_light_state(traffic_light, carla.TrafficLightState.Green, green_duration)
                print(
                    f"Traffic light at {traffic_light.get_location()} turned green for {green_duration} seconds due "
                    f"to high traffic density.")
                time.sleep(green_duration + 3.0)  # Include the yellow light duration
                set_traffic_light_state(traffic_light, carla.TrafficLightState.Red, green_duration)
            else:
                set_traffic_light_state(traffic_light, carla.TrafficLightState.Red, green_duration)
        time.sleep(check_interval)


traffic_lights = world.get_actors().filter('traffic.traffic_light')

# We will also set up the spectator
spectator = world.get_spectator()

spawn_points = world.get_map().get_spawn_points()

# Select some models from the blueprint library
models = ['dodge', 'audi', 'model3', 'mini', 'mustang', 'lincoln', 'prius', 'nissan', 'crown', 'impala']
blueprints = []
for vehicle in world.get_blueprint_library().filter('*vehicle*'):
    if any(model in vehicle.id for model in models):
        blueprints.append(vehicle)

# Assign vehicle counts to each route
route_vehicle_counts = [10, 10, 20, 10]
total_vehicles = sum(route_vehicle_counts)

# Set a max number of vehicles and prepare a list for those we spawn
max_vehicles = total_vehicles
max_vehicles = min([max_vehicles, len(spawn_points)])
vehicles = []

# Take a random sample of the spawn points and spawn some vehicles
for i, spawn_point in enumerate(random.sample(spawn_points, max_vehicles)):
    temp = world.try_spawn_actor(random.choice(blueprints), spawn_point)
    if temp is not None:
        vehicles.append(temp)

# Routes with their respective spawn points and indices
routes = [
    ([32], [129, 28, 137, 101, 57, 58, 154, 147]),
    ([149], [21, 105, 134, 52, 86, 120, 4, 121]),
    ([147], [72, 146, 126, 99, 108, 68, 24]),
    ([106], [85, 1, 104, 67, 140, 10, 143])
]

# Prepare route locations
route_locations = []
for spawn_point, indices in routes:
    route = [spawn_points[spawn_point[0]].location]
    for ind in indices:
        route.append(spawn_points[ind].location)
    route_locations.append(route)

# Assign vehicles to routes
assigned_vehicles = {
    0: [],  # Vehicles for route 1
    1: [],  # Vehicles for route 2
    2: [],  # Vehicles for route 3
    3: []  # Vehicles for route 4
}

vehicle_idx = 0
for route_idx, count in enumerate(route_vehicle_counts):
    for _ in range(count):
        if vehicle_idx < len(vehicles):
            assigned_vehicles[route_idx].append(vehicles[vehicle_idx])
            vehicle_idx += 1

# Assign routes to vehicles
for route_idx, vehicle_list in assigned_vehicles.items():
    for vehicle in vehicle_list:
        traffic_manager.set_path(vehicle, route_locations[route_idx])
        vehicle.set_autopilot(True)
        # Randomly set the probability that a vehicle will ignore traffic lights
        traffic_manager.ignore_lights_percentage(vehicle, random.randint(0, 50))

# Set delay to create gap between spawn times
spawn_delay = 20
counter = spawn_delay

try:
    control_traffic_lights(traffic_lights, check_interval=10, density_threshold=5, green_duration=20)
except KeyboardInterrupt:
    print("Traffic control interrupted")

