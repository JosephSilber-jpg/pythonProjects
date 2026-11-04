import serial
from time import sleep
from Reduino.Actuators import Led
from Reduino.Utils import sleep
import pygame
import sys

# make sure this is correct
ARDUINO_PORT = 'COM3'

# mapping for standard Xbox controller
button_map = {
    "A": 0,
    "B": 1,
    "X": 2,
    "Y": 3,
    "LB": 4,
    "RB": 5,
    "BACK": 6,
    "START": 7,
    "LS": 8,
    "RS": 9,
    "XBOX": 10
}

def send_command(cmd):
        print("Sending command:" + cmd)
        arduino.write((cmd + '\n').encode())

if __name__ == "__main__":
    
    # Initialize the Arduino connection
    arduino = serial.Serial(ARDUINO_PORT, 9600, timeout=1)

    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        print("Controller not found")
        sys.exit(1)

    controller = pygame.joystick.Joystick(0)
    controller.init()


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.JOYBUTTONDOWN:
                print(f"Button pressed: {event.button}")
                if (event.button == button_map.get("A")):
                    send_command("LED_ON")
                if (event.button == button_map.get("B")):
                    send_command("LED_OFF")
                if (event.button == button_map.get("X")):
                    send_command("LED_TOGGLE")
                if (event.button == button_map.get("BACK")):
                    print("Shutting down")
                    running = False

    arduino.close()
    sys.exit(0)

# The following code is copied to the arduino IDE and uploaded to the arduino uno
"""

int LED_DIO = 7;
bool ledStatus = false;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LED_DIO, OUTPUT);
}

void setLed(bool status) {
  if (status) {
    digitalWrite(LED_DIO, HIGH)
  } else {
    digitalWrite(LED_DIO, LOW);
  }
  ledStatus = status;
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');

    if (command.equals("LED_ON")) {
      setLed(true);
    } 

    else if (command.equals("LED_OFF")) {
      setLed(false);
    }
    
    else if (command.equals("LED_TOGGLE")) {
      setLed(!ledStatus);
    }
  }
}


"""