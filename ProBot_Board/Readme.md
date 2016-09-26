# Probot Board

Greetings, this version of the board is an evolution from what we already have, if you find any problem, please report.
The board have an input for 5V in the top (Ethernet port side) to power the board and a 24V input to monitor the battery voltage (Don't put higher than this voltage or youll burn the microcontroller or the ADC).

To control, we have two PWM ouputs one for each controller if used the same as us and an output for the Sabertooth 2X25A.

There are also two inputs for the encoders with the usual order A, Vcc, B, empty, Gnd. You need to have atention on wich you connect to that the robot doesn't go in the wrong way.

This shield is ready to put the MPU6050 acelerometer.

For future work, we are thinking to incorporate a LiPo battery monitor with the TI BQ76930 and BQ78350 devices, and change it all to SMD circuit, integrating the MPU6050.
