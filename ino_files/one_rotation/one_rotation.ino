 typedef void (*footype)();
  // variables
int motorPin1 = 2; // IN1
int motorPin2 = 3; // IN2
int motorPin3 = 4; // IN3
int motorPin4 = 5; // IN4

int motorSpeed= 2000;
int count = 0; // count for steps made
int countRot = 512; //number of steps per full rotation
int lookup[8] = {B01000, B01100, B00100, B00110, B00010, B00011, B00001, B01001};
int state = countRot;

void setup() {
  // Motor Pins as outputs
pinMode(motorPin1, OUTPUT);
pinMode(motorPin2, OUTPUT);
pinMode(motorPin3, OUTPUT);
pinMode(motorPin4, OUTPUT);
Serial.begin(9600);
}

void loop() {
//  one_rotation(clockwise);
  clockwise();
}

void one_rotation(footype fcn){
//  One clockwise rotation
//  int state = countRot;
  if(state > count){
    fcn();
    state--;
  }
}

void anticlockwise()
{
  for(int i = 0; i < 8; i++)
  {
    setOutput(i);
    delayMicroseconds(motorSpeed);
  }
}

void clockwise()
{
  for(int i = 7; i >= 0; i--)
  {
    setOutput(i);
    delayMicroseconds(motorSpeed);
  }
}

void setOutput(int out)
{
  digitalWrite(motorPin1, bitRead(lookup[out], 0));
  digitalWrite(motorPin2, bitRead(lookup[out], 1));
  digitalWrite(motorPin3, bitRead(lookup[out], 2));
  digitalWrite(motorPin4, bitRead(lookup[out], 3));
}


