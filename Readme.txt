Self Balancing Robot

This robot has almost 1,50m high, uses sabertooth controller with packetized serial protocol to control two EMG49 motors.
To find it's angle it uses the MPU6050 IC that uses an I2C connection with all the data from an accelerometer and a gyroscope.

To control all that data, we use a Beaglebone Black rev C with Linux environment. 

It is used several PID's to control the speed and angle of the robot.

The end
