import carla
import random
import time

client = carla.Client('localhost', 2000)
client.set_timeout(5.0)  # Set the time limit for connecting with the server.

world = client.get_world()

spawn_points = world.get_map().get_spawn_points()

models = ['dodge', 'audi', 'model3', 'mini', 'mustang', 'lincoln', 'prius', 'nissan', 'crown', 'impala']
blueprints = []
for vehicle in world.get_blueprint_library().filter('vehicle'):
    if any(model in vehicle.id for model in models):
        blueprints.append(vehicle)

# Set a max number of vehicles and prepare a list for those we spawn
max_vehicles = 100
max_vehicles = min([max_vehicles, len(spawn_points)])
vehicles = []

# Draw the spawn point locations as numbers in the map
for i, spawn_point in enumerate(spawn_points):
    world.debug.draw_string(spawn_point.location, str(i), life_time=10)

spawn_point_1 = spawn_points[32]
# Create route 1 from the chosen spawn points
route_1_indices = [129, 28, 137, 101, 57, 58, 154, 147]
route_1 = []
for ind in route_1_indices:
    route_1.append(spawn_points[ind].location)

# Route 2
spawn_point_2 = spawn_points[149]
# Create route 2 from the chosen spawn points
route_2_indices = [21, 105, 134, 52, 86, 120, 4, 121]
route_2 = []
for ind in route_2_indices:
    route_2.append(spawn_points[ind].location)

# Route 3
spawn_point_3 = spawn_points[147]
# Create route 3 from the chosen spawn points
route_3_indices = [72, 146, 126, 99, 108, 68, 24]
route_3 = []
for ind in route_3_indices:
    route_3.append(spawn_points[ind].location)

# Route 4
spawn_point_4 = spawn_points[106]
# Create route 4 from the chosen spawn points
route_4_indices = [85, 1, 104, 67, 140, 10, 143]
route_4 = []
for ind in route_4_indices:
    route_4.append(spawn_points[ind].location)

# Set autopilot mode for vehicles
for vehicle in vehicles:
    vehicle.set_autopilot(True)

# Finding Traffic lights
actors = world.get_actors()

traffic_lights = actors.filter('traffic_light')

# Iterate over each traffic light and set the state
for traffic_light in traffic_lights:
    traffic_light.set_state(carla.TrafficLightState.Red)
    if traffic_light.get_state() == carla.TrafficLightState.Red:
        traffic_light.set_state(carla.TrafficLightState.Green)
        traffic_light.set_green_time(10.0)

tm = client.get_trafficmanager(8000)
tm_port = tm.get_port()
for v in my_vehicles:
  v.set_autopilot(True,tm_port)
danger_car = my_vehicles[0]
tm.global_distance_to_leading_vehicle(5)
tm.global_percentage_speed_difference(80)
for v in my_vehicles:
  tm.auto_lane_change(v,False)

while True:
    world.tick()
