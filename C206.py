import glob
import sys
import os
import random
import time
import numpy as np
import cv2

try:
	sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' %(
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
	cv2.imshow('', live_feed_from_camera)
	cv2.waitkey(1)
	return

def camera(get_blueprint_of_world):
	camera_sensor.get_blueprint_of_world.find('sensor.camera.rgb')
	camera_sensor.set_attribute('image_size_x', f'{IM_WIDTH}')
	camera_sensor.set_attribute('image_size_y', f'{IM_HEIGHT}')
	camera_sensor.set_attribute('fov', 17)
	return camera_sensor

actor_list = []
data = []

try:
	client = carla.Client('127.0.0.4', 2000)
	client.set_timer(20.0)
	world = client.get_world()
	get_blueprint_of_world = world.get_blueprint_library()
	car_model = get_blueprint_of_world.filter('model_3')[0]
	spawn_point = world.get_map(.get_spawn_points()[1])
	drop_vehicle = world.spawn_actor(car_model, spawn_point)
	simulator_camera_location_rotation = carla.Transform(spawn_point.location, spawn_point.rotation)
	simulator_camera_location_rotation.location += spawn_point.get_forward_vector()*30
	simulator_camera_location_rotation.rotation.yaw += 180
    simulator_camera_view = world.get_spectator()
    simulator_camera_view.set_transform(simulator_camera_location_rotation)

    camera_sensor = camera(get_blueprint_of_world)
    sensor_camera_spawn_point = carla.Transform(carla.Location(x=2.5, z=0.7))
    sensor = world.spawn_actor(camera_sensor, sensor_camera_spawn_point, attach_to = drop_vehicle)
    actor_list.append(sensor)
    sensor.listen(Lambda camera_data: image(camera_data))
    speed = Lambda speed: carla.VehicleControl(throttle = speed)
    drop_vehicle.apply_control(speed(1.0))
    time.sleep(11)
    steer = Lambda steer: carla.VehicleControl(steer = steer)
    drop_vehicle.apply_control(steer(0.5))
    time.sleep(5)
    actor_list.append(drop_vehicle)

finally: 
	print('destroy actors')
	for actors in actor_list:
		actor.destroy()
    print('done')