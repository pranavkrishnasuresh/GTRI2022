// currently looking at errors, extraneous functions, logic of loop
#include <Servo.h>

Servo gripperServo;
char cmdStr[128];
int byte_mk = 0;

// pin nums
const int limitSwitchPin1 = 2;
const int limitSwitchPin2 = 3;
const int servoPin = 9;

// closed or opened
const int gripperClosePos = 0;
const int gripperOpenPos = 180;

// bools
bool gripperIsDone = 0;


// input info
void serial_setup() {
  // Open Serial communication
  Serial.begin(9600);
  // Serial.println("INIT");
}

// setup pins
void setup() {
  
  serial_setup();

  // Servo setup
  gripperServo.attach(servoPin);

  // Switch setup
  pinMode(limitSwitchPin1, INPUT_PULLUP);
  pinMode(limitSwitchPin2, INPUT_PULLUP);
}

int switch1state = digitalRead(limitSwitchPin1);

void gripperCommand(char* command) {

  if(strcmp(command, "open") == 0){
    gripperServo.write(gripperOpenPos);
    gripperIsDone = 1;
  } else if(strcmp(command, "close") == 0){
    gripperServo.write(gripperClosePos);
    gripperIsDone = 1;
  }

}

void output_str(){

  delay(4000);

  if (!gripperIsDone) {
    Serial.write("0");
  } else {
    Serial.write("1");
  }
  
  if (digitalRead(limitSwitchPin1) == HIGH) {
    Serial.write("0");
  } else {
    Serial.write("1");
  }

  if (digitalRead(limitSwitchPin2) == HIGH) {
    Serial.write("0");
  } else {
    Serial.write("1");
  }
  Serial.write("\n");
  
  
}  // first one: open/close, second and third limitswitch

// Process the current serial command and call respective functions.
int process_cmd() {

  // // Save a copy of command string (strtok will destroy it)
  char tmpStr[sizeof(cmdStr)];
  strcpy(tmpStr, cmdStr);

  // Split out first word at space
  char *actionStr = strtok(tmpStr, " ");

  // Serial.print("Received command: ");
  // Serial.println(actionStr);

  // Switch over available actions:
  int action_res = 1;

  if (strcmp(actionStr, "open") == 0) {
    
    // Serial.println("open detected.");
    gripperCommand("open");
    output_str();    
    action_res = 0;

  } else if (strcmp(actionStr, "close") == 0) {

    // Serial.println("close detected.");
    gripperCommand("close");
    output_str();
    action_res = 0;
    
  } else {
    // Return error code
    action_res = -1;
  }
  // // Convert failed action response to correct error enum
  // if (action_res != 0) {
  //   action_res = -1;  // Error Action Failed
  // }
  return action_res;
}

void serial_loop() {

  // Read new serial characters from buffer
  while (Serial.available()) {

    char ch = Serial.read();
    cmdStr[byte_mk] = ch;  // Add character(s) to command string
    byte_mk += 1;          // Increment byte marker

    // Overflow error
    // if (byte_mk > 127) {
    //   byte_mk = 0;
    //   Serial.println("OVERFLOW");
    // }

    // Process command line
    if (ch == '\n') {

      //Replace newline character with space so it will be caught by strtok
      cmdStr[byte_mk - 1] = ' ';
      int res = process_cmd();
      byte_mk = 0;



      // Send response message
      // if (res == 0) {
      //   Serial.println("ACTION");
      // } else if (res == 1) {
      //   Serial.println("COMMAND_INVALID");
      // } else {
      //   Serial.println("ACTION_FAIL");
      // }
    } 
  }
}

void loop()
{
  
  serial_loop();

}


  //sending 3 characters list to next part
  
