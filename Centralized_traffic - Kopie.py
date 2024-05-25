import carla
import random

# Connect to the client and retrieve the world object
client = carla.Client('localhost', 2000)
world = client.get_world()

# Set up the simulator in synchronous mode
settings = world.get_settings()
settings.synchronous_mode = True # Enables synchronous mode
settings.fixed_delta_seconds = 0.02
world.apply_settings(settings)

# Set up the TM in synchronous mode
traffic_manager = client.get_trafficmanager()
traffic_manager.set_synchronous_mode(True)

# Set a seed so behaviour can be repeated if necessary
traffic_manager.set_random_device_seed(0)
random.seed(0)

actors = world.get_actors()

traffic_lights = actors.filter('traffic_light')

for traffic_light in traffic_lights:
    traffic_light.set_state(carla.TrafficLightState.Red)

# We will also set up the spectator
spectator = world.get_spectator()

spawn_points = world.get_map().get_spawn_points()

# Select some models from the blueprint library
models = ['dodge', 'audi', 'model3', 'mini', 'mustang', 'lincoln', 'prius', 'nissan', 'crown', 'impala']
blueprints = []
for vehicle in world.get_blueprint_library().filter('*vehicle*'):
    if any(model in vehicle.id for model in models):
        blueprints.append(vehicle)

# Set a max number of vehicles and prepare a list for those we spawn
max_vehicles = 50
max_vehicles = min([max_vehicles, len(spawn_points)])
vehicles = []

# Take a random sample of the spawn points and spawn some vehicles
for i, spawn_point in enumerate(random.sample(spawn_points, max_vehicles)):
    temp = world.try_spawn_actor(random.choice(blueprints), spawn_point)
    if temp is not None:
        vehicles.append(temp)

# Route 1
spawn_point_1 =  spawn_points[32]
# Create route 1 from the chosen spawn points
route_1_indices = [129, 28, 137, 101, 57, 58, 154, 147]
route_1 = []
for ind in route_1_indices:
    route_1.append(spawn_points[ind].location)

# Route 2
spawn_point_2 =  spawn_points[149]
# Create route 2 from the chosen spawn points
route_2_indices = [21, 105, 134, 52, 86, 120, 4, 121]
route_2 = []
for ind in route_2_indices:
    route_2.append(spawn_points[ind].location)

# Route 3
spawn_point_3 =  spawn_points[147]
# Create route 3 from the chosen spawn points
route_3_indices = [72, 146, 126, 99, 108, 68, 24]
route_3 = []
for ind in route_3_indices:
    route_3.append(spawn_points[ind].location)

# Route 4
spawn_point_4 =  spawn_points[106]
# Create route 4 from the chosen spawn points
route_4_indices = [85, 1, 104, 67, 140, 10, 143]
route_4 = []
for ind in route_4_indices:
    route_4.append(spawn_points[ind].location)

for vehicle in vehicles:
    vehicle.set_autopilot(True)
    # Randomly set the probability that a vehicle will ignore traffic lights
    traffic_manager.ignore_lights_percentage(vehicle, random.randint(0,50))

# Set delay to create gap between spawn times
spawn_delay = 20
counter = spawn_delay


while True:
    world.tick()











