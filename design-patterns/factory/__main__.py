from autofactory import AutoFactory

factory = AutoFactory()

for car_name in 'ChevyVolt', 'FordFusion', 'JeepSahara', 'Tesla', 'LandRover':
    car = factory.create_instance(car_name)
    car.start()
    car.stop()