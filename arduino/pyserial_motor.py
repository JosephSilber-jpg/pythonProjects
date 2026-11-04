import serial
from time import sleep
import pygame
import sys
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

commands = {
    pygame.K_LEFT: "LEFT",
    pygame.K_RIGHT: "RIGHT",
    pygame.K_SPACE: "STOP",
    pygame.K_ESCAPE: "QUIT",
}

# make sure this is correct
ARDUINO_PORT = 'COM3'

def send_command(cmd):
        # print("Sending command:" + cmd)
        Arduino.write((cmd + '\n').encode())

if __name__ == "__main__":
    
    # Initialize the Arduino connection
    Arduino = serial.Serial(ARDUINO_PORT, 9600, timeout=1)
    sleep(1)

    Arduino.reset_input_buffer()

    pygame.init()
    pygame.joystick.init()

    controller = None
    if pygame.joystick.get_count() == 0:
        print("Controller not connected")
    else:
        controller = pygame.joystick.Joystick(0)
        controller.init()

    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Arduino Controller")

    # Set up mathlibplot
    fig, ax = plt.subplots()
    time, wattage = [], []
    line, = ax.plot([], [], 'r-')  # Create an empty line object

    # Set axis limits so the plot doesn't compress automatically
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 10)

    
    def updateGraph(frame, wattage):
      # Simulate receiving new data points (e.g., from a sensor or API)
      time.append(frame)
      wattage.append(wattage)
      
      # Keep the visible window moving once data exceeds limits
      if frame > 100:
          ax.set_xlim(frame - 100, frame)
          
      # Update the data of the existing line object (highly efficient)
      line.set_data(time, wattage)
      plt.show()
      return line,

    running = True
    print("Running starting now")
    while running:
        
        # check for serial values
        if Arduino.in_waiting > 0:
            message = Arduino.readline().decode().strip()
            print(f"Received value from Arduino: {message}")
            if message.startswith("WATTAGE"):
                wattage = float(message.split(":")[1])
                # updateGraph(len(time), wattage)
                

        # handle pygame inputs
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                # if the key pressed is in the commands dictionary, send the corresponding command
                print(f"Button pressed: {event.key}")

                if event.key in commands:
                    cmd = commands[event.key]
                    if cmd == "QUIT":
                        print("Shutting down")
                        running = False
                    else:
                        send_command(cmd)

            elif event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:
                    # send horizontal joystick input, rounded to 2 decimal places
                    print(math.floor(event.value * 100) / 100)
                    send_command("JOYSTICK" + str(math.floor(event.value * 100) / 100))

    print("Exiting main loop")
    Arduino.close()
    sys.exit(0)

# The following code is copied to the arduino IDE and uploaded to the arduino
"""

#include <Servo.h>
#include <Wire.h>
#include <Adafruit_INA219.h>

Adafruit_INA219 ina219;

int PORT = 9600;
int MOTOR_DIO = 7;
double currentSpeed = 0;

Servo motor;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(PORT);
  motor.attach(MOTOR_DIO);
  //motor.write(0);

  if (!ina219.begin()) {
    Serial.println("Failed to find INA219 chip");
    while (1) { delay(10); }
  }
}

void setMotorSpeed(double speed) {
  motor.write(speed);
  currentSpeed = speed;
  // Serial.print("SETTING SPEED TO " + String(speed));
}

void loop() {
  float busvoltage = ina219.getBusVoltage_V();
  float current_mA = ina219.getCurrent_mA();
  double wattage = abs(busvoltage) * abs(current_mA);
  Serial.println("WATTAGE:" + String(wattage));

  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');

    if (command.equals("LEFT")) {
      setMotorSpeed(50);
    }
    if (command.equals("RIGHT")) {
      setMotorSpeed(140);
    }
    if (command.equals("STOP") || command.equals("QUIT")) {
      setMotorSpeed(90);
    } 

    if (command.substring(0, 8).equals("JOYSTICK")) {
      double speed = command.substring(8).toDouble();
      setMotorSpeed(90 + (6 * speed));
    }
  }

  delay(100);
}

"""