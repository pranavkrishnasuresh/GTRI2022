#include <Servo.h>

Servo gripperServo;  // create servo object

// Define the pins for the sensor and servo
const int limitSwitchPin = 2;
const int servoPin = 9;

const int gripperClosed = 0;
const int gripperOpened = 180;

bool gripperShouldClose = false;
bool gripperIsDone = false;

int pos = gripperOpened;

// placeholder code using time, not precise enough
const long robotArmMovementTime = 10 * 1000;
long plateDetectTime = 0;
// end of placeholder code

void setup() {
  // put your setup code here, to run once:
  pinMode(limitSwitchPin, INPUT_PULLUP);

  gripperServo.attach(gripperServoPin);

}

void loop() {
  // put your main code here, to run repeatedly:

  if (gripperIsDone == false) {

    bool switchIsPressed = digitalRead(limitSwitchPin);

    if (switchIsPressed == LOW) {
 
      if (gripperShouldClose == false) {
         plateDetectTime = millis(); // placeholder code to count time 
      }
     
 
      gripperShouldClose = true;
 
      //switch is being pressed
    } else {
 
      //switch is not being pressed
      //Dont do anything
     
    }
 
    if (gripperShouldClose == true) {
 
      //Move the servo to the "closed" position for the gripper
      gripperServo.write(gripperClosed);
     
    } else {
      //Move the servo to the "opened" position for the gripper
      gripperServo.write(gripperOpened);
    }
 
    if (gripperShouldClose == true) { // main if statement, using time
      //time now - minus the time of plate detection >= robotMovementTime
      if (millis() - plateDetectTime >= robotMovementTime) {
        //Time to release the plate
        gripperServo.write(gripperOpened);
        gripperIsDone = true;
       
      }
    }
     
  }
 

}

	
	
	
