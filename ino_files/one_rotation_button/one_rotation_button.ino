 typedef void (*footype)();
  // variables
int motorPin1 = 2; // IN1
int motorPin2 = 3; // IN2
int motorPin3 = 4; // IN3
int motorPin4 = 5; // IN4
int motorPin5 = 8; // IN1
int motorPin6 = 9; // IN2
int motorPin7 = 10; // IN3
int motorPin8 = 11; // IN4
int buttonPin = A5;

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
pinMode(motorPin5, OUTPUT);
pinMode(motorPin6, OUTPUT);
pinMode(motorPin7, OUTPUT);
pinMode(motorPin8, OUTPUT);
pinMode(buttonPin, INPUT);
Serial.begin(9600);
}

void loop() {
//  clockwise();
//  one_rotation(clockwise);
  int button_status = digitalRead(buttonPin);
  Serial.println(button_status);
  if(button_status == 1){
    Serial.println("spin");
    clockwise();
  }
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
  digitalWrite(motorPin5, bitRead(lookup[out], 0));
  digitalWrite(motorPin6, bitRead(lookup[out], 1));
  digitalWrite(motorPin7, bitRead(lookup[out], 2));
  digitalWrite(motorPin8, bitRead(lookup[out], 3));
}


