import glob
import os
import sys
import threading
import cv2
import numpy as np
import math

try:
	sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg'%(
		sys.version_info.major,
		sys.version_info.minor,
		'win-amd64' if os.name == 'nt' else 'linux_x86_64'))[0])

except IndexError:
	pass

import carla

def get_actor_display_name(actor): #Obtaining the name of the actor
	name = ' '.join(actor.type_id.replace('_', '.').title().split('.')[1:])
	return name

actor_list = []
IM_WIDTH = 640 
IM_HEIGHT = 480

def number_of_vehicle():
	all_vehicles = world.get_actors().filter('vehicles.*')
	threading.Timer(0.1, number_of_vehicle).start()
	transform_location = dropped_vehicle.get_transform()
	
    if len(all_vehicles) > 1:
    	distance = lambda data: math.sqrt((data.x - transform_location.location.x)**2 + (data.y - transform_location.location.y)**2 + (data.z - transform_location.location.z)**2)
    	get_distance_of_bot_vehicles = []
    	for car in all_vehicles:
    		if car.id != world.id:
    			get_distance_of_bot_vehicles.append((distance(car.get_location()), each_car))

    	vehicle_data = {}
    	final_vehicle_result = []
    	sorted_vehicles = sorted(get_distance_of_bot_vehicles)

        for distance_of_car, vehicle in sorted_vehicles:
        	if distance_of_car > 200.0:
        		break
        	vehcile_type = get_actor_display_name(vehicle)
        	vehicle_data['vehicle_name'] = vehicle_type
        	vehicle_data['distance'] = distance_of_car
        	final_vehicle_result.append(vehicle_data)

        	for distance_in_meter in final_vehicle_result:
        		if distance_in_meter['distance'] > 6 and distance_in_meter['distance'] < 10:
        			dropped_vehicle.apply_control(carla.VehicleControl(throttle = 0.2))
        			time.sleep(3)

        			dropped_vehicle.apply_control(carla.VehicleControl(throttle = 0.2, steer = -0.2))
        			time.sleep(2)

        			dropped_vehicle.apply_control(carla.VehicleControl(throttle = 0.2, steer = 0.1))
        			time.sleep(2)

        			dropped_vehicle.apply_control(carla.VehicleControl(throttle = 0.2))
        			time.sleep(3)

        			car_control()

        		if distance_in_meter['distance'] > 1 and distance_in_meter['distance'] < 5:
        			print('Incomming collison.')
        			dropped_vehicle.apply_control(carla.VehicleControl(hand_brake = True))
        			time.sleep(2)

        			car_control()  

def image(image):
    matrix_representational_data = np.array(image.raw_data)
    reshape_of_image = matrix_representational_data.reshape((IM_HEIGHT, IM_WIDTH, 4))
    live_feed_from_camera = reshape_of_image[:, :, :3]
    cv2.imshow("", live_feed_from_camera)
    cv2.waitKey
    return

def camera(get_blueprint_of_world):
	camera_sensor = get_blueprint_of_world.find('sensor.camera.rgb')
	camera_sensor.set_attribute('image_size_x', f'{IM_WIDTH}')
	camera_sensor.set_attribute('image_size_y', f'{IM_HEIGHT}')
	camera_sensor.set_attribute('fov', '70')
	return camera

def car_control():
	dropped_vehicle.apply_control(carla.VehicleControl(throttle = 0.34, reverse = True))
	dropped_vehicle.set_light_state(carla.VehicleLightState(carla.VehicleLightState.reverse | carla.VehicleLightState.Interior | carla.VehicleLightState.LowBeam))
	time.sleep(4)

	dropped_vehicle.apply_control(carla.VehicleControl(throttle = 0.45, steer = -0.1))
	dropped_vehicle.set_light_state(carla.VehicleLightState(carla.VehicleLightState.reverse | carla.VehicleLightState.Interior | carla.VehicleLightState.LowBeam))
	time.sleep(6)

	dropped_vehicle.apply_control(carla.VehicleControl(throttle = 0.1, steer = 0.1))
	dropped_vehicle.set_light_state(carla.VehicleLightState())
	time.sleep(1)


	dropped_vehicle.apply_control(carla.VehicleControl(throttle = 0.4))
	dropped_vehicle.set_light_state(carla.VehicleLightState())
	time.sleep(3)


	dropped_vehicle.apply_control(carla.VehicleControl(hand_brake = True))
	dropped_vehicle.set_light_state(carla.VehicleLightState())
	time.sleep(5)

try:
	carla.Client('127.0.0.1', 2000)
	client.set_timeout(10.0)
	world = client.get_world()
	
	get_blueprint_of_world = world.get_blueprint_library()
	car_model = get_blueprint_of_world.filter('model3')[0]
	spawn_point = world.get_map().get_spawn_points()[1]
	dropped_vehicle = world.spawn_actor(car_model, spawn_point)

	#Defining carla simulation camera, location, rotation, yaw
	simulator_camera_location_rotation = carla.Transform(spawn_point.location, spawn_point.rotation)
	simulator_camera_location_rotation.location += spawn_point.get_forward_vector()* 30
	simulator_camera_location_rotation.rotation.yaw += 180
	simulator_camera_view = world.get_spectator()
	simulator_camera_view.set_transform(simulator_camera_location_rotation)
	actor_list.append(dropped_vehicle)

	#Defining camera sensor
	camera_sensor = camera(get_blueprint_of_world)
	sensor_camera_spawn_point = carla.Transform(carla.Location(x = -11.5, z = 4.7, y = 1.2))
	sensor = world.spawn_actor(camera_sensor, sensor_camera_spawn_point, attach_to = dropped_vehicle)
	sensor.listen(lambda camera_data: image(camera_data))
	actor_list.append(sensor)

	number_of_vehicle()
	car_control()
	time.sleep(1000)

finally:
	print('Destorying actors.')
	for actor in actor_list:
		actor.destroy()
	print('Finished.')