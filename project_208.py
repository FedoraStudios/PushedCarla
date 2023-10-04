import glob
import os
import sys
import time
import random

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

actor_list = []
start_time= time.time()

def car_control():
    dropped_vehicle.apply_control(carla.VehicleControl(throttle=0.52, gear=0))
    time.sleep(10)
    dropped_vehicle.apply_control(carla.VehicleControl(throttle=0.5, steer=0.17, gear=0))
    time.sleep(3)
    dropped_vehicle.apply_control(carla.VehicleControl(throttle=0.5, steer=-0.10))
    time.sleep(2)
    dropped_vehicle.apply_control(carla.VehicleControl(throttle=0.5, steer=-0.17, gear=0))
    time.sleep(3)
    dropped_vehicle.apply_control(carla.VehicleControl(hand_brake=True))
    time.sleep(5)


try:
    client = carla.Client('127.0.0.1', 2000)
    client.set_timeout(10.0)
    world = client.get_world()

    get_blueprint_of_world = world.get_blueprint_library()
    #define car model
    car_model = get_blueprint_of_world.filter('model3', spawn_point)
    #define random spawn location
    spawn_point = random.choice(world.get_map().get_spawn_points())
    dropped_vehicle = world.spawn_actor(car_model, spawn_point)
    simulator_camera_location_rotation = carla.Transform(spawn_point.location, spawn_point.rotation)
    simulator_camera_location_rotation.location += spawn_point.get_forward_vector() * 30
    simulator_camera_location_rotation.rotation.yaw += 180
    simulator_camera_view = world.get_spectator()
    simulator_camera_view.set_transform(simulator_camera_location_rotation)
    actor_list.append(dropped_vehicle)

    collision_sensor = get_blueprint_of_world.find('sensor.other.collision')
    sensor_collision_spawn_point = carla.Transform(carla.Location(x=2.5, z=0.7))
    sensor = world.spawn_actor(collision_sensor, sensor_collision_spawn_point, attach_to=dropped_vehicle)

    sensor.listen(lambda data: _on_collision(data))

    actor_list.append(sensor)


    def _on_collision(data):
        print('**Caution: Collision**')
        print('--- %s seconds ---' % (time.time() - start_time))
        dropped_vehicle.apply_control(carla.VehicleControl(hand_brake=True))
        time.sleep(5)
        car_control()

    car_control()
    time.sleep(1000)

finally:
    print('destroying actors')
    for actor in actor_list:
        actor.destroy()
    print('done.')
