import glob
import random
import os
import sys
import cv2
import numpy as np
import time

try:
	sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' '%'(
		sys.version_info.major,
		sys.version_info.minor,
		'win-amd64' 
		if os.name == 'nt' else 'linux-x86-64'))[0])

except IndexError:
	pass

import carla

IM_WIDTH = 640
IM_HEIGHT = 480

def image(image):
	matrix_representational_data = np.array(image.raw_data)
	reshape_of_image = matrix_representational_data.reshape((IM_HEIGHT, IM_WIDTH, 4))
	live_feed_from_camera = reshape_of_image[:, :, :3]
	cv2.imshow(',', live_feed_from_camera)
	cv2.waitKey(1)
	return

def camera(get_blueprint_of_world):
    camera_sensor = get_blueprint_of_world.find('sensor.camera.rgb')
    camera_sensor.set_attribute('image_size_x', f'{IM_WIDTH}')
    camera_sensor.set_attribute('image_size_y', f'{IM_HEIGHT}')
    camera_sensor.set_attribute('fov', '70')
    return camera_sensor

def car_control():
	#throttle, steer, gear
    #left = negative, right = posative

    dropped_vehicle.apply_control(carla.VehicleControl(throttle = 0.52, steer = -1, gear = 0))
    time.sleep(5)

    dropped_vehicle.apply_control(carla.VehicleControl(throttle = 0.5, gear = 0))
    time.sleep(6)

    dropped_vehicle.apply_control(carla.VehicleControl(throttle = 0.5, steer = -0.17, gear = 0))
    time.sleep(2)

    dropped_vehicle.apply_control(carla.VehicleControl(throttle = 0.5, steer = 0.14, gear = 0))
    time.sleep(9)

    dropped_vehicle.apply_control(carla.VehicleControl(throttle = 0.4, steer = -0.25, gear = 0))
    time.sleep(1)

    dropped_vehicle.apply_control(carla.VehicleControl(throttle = 0.8, gear = 0))
    time.sleep(4)

    dropped_vehicle.apply_control(carla.VehicleControl(hand_brake = True))
    time.sleep(5)

    location = dropped_vehicle.get_location()
    return location

data = []
actor_list = []

try:
	client = carla.Client('127.0.0.1', 2000)
	client.set_timer(20.0)
	world = client.get_world()
	get_blueprint_of_world = world.get_blueprint_library
	car_model = get_blueprint_of_world.filter('model_3' [0])
	spawn_point = world.get_map(.get_spawn([1]))
	dropped_vehicle = world.spawn_actor(car_model, spawn_point)

	simulator_camera_location_rotation = carla.Transform(spawn_point.location, spawn_point.rotation)
	simulator_camera_location_rotation.location += spawn_point.get_forward_vector()*30
	simulator_camera_location_rotation.rotation.yaw += 180
    simulator_camera_view = world.get_spectator()
    simulator_camera_view.set_transform(simulator_camera_location_rotation)

    camera_sensor = camera(get_blueprint_of_world)
    sensor_camera_spawn_point = carla.Transform(carla.Location(x=2.5, z=0.7))
    sensor = world.spawn_actor(camera_sensor, sensor_camera_spawn_point, attach_to = dropped_vehicle)
    actor_list.append(sensor)
    sensor.listen(Lambda camera_data: image(camera_data))
    speed = Lambda speed: carla.VehicleControl(throttle = speed)
    dropped_vehicle.apply_control(speed(1.0))
    time.sleep(11)
    steer = Lambda steer: carla.VehicleControl(steer = steer)
    dropped_vehicle.apply_control(steer(0.5))
    time.sleep(5)
    car_new_location = car_control
    print(car_new_location)
    actor_list.append(dropped_vehicle)

finally:
	print('destroy actors')
	for actors in actor_list:
		actor.destroy()
    print('done')