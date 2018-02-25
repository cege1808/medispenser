typedef void (*fcntype)(int module_num);

// String constants
const char inbound_start_str = '<';
const char inbound_end_str = '>';
const char outbound_start_str = '[';
const char outbound_end_str = ']';

// Serial constants;
const int baudrate = 9600;

// Pin contants
const int num_of_modules = 3;
const int motor_driver_pins[3][4] = { {2,3,4,5}, {6,7,8,9}, {10,11,12,13} };
const int ir_detection_pins[3] = {A0,A1,A2};
const int led_pin = A5;

// Motor constants
const int motor_speed = 2000;
const int motor_lookup[8] = {B01000, B01100, B00100, B00110, B00010, B00011, B00001, B01001};
const int steps_in_one_rotation = 512;

// IR sensor
const int ir_sensor_limit = 400;

// States
char incoming_byte;
String inbound_str;
String outbound_str;

void setup() {
  // put your setup code here, to run once:
  initialize_pins();
  Serial.begin(baudrate);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available() > 0){
    incoming_byte = Serial.read();

    // get the complete instruction between '<' and '>'
    if(is_start_str(incoming_byte)){
      do {
        incoming_byte = Serial.read();
        if(incoming_byte != -1 and incoming_byte != '>'){
          inbound_str += incoming_byte;
        }
      } while(!is_end_str(incoming_byte));

      // After getting instruction
      inbound_str.trim();
      outbound_str = process_instruction(inbound_str);
      writeStringtoSerial(construct_outbound_msg(outbound_str));
      inbound_str = "";
    }
  }
}


// Initialize Functions

void initialize_pins(){
  for(int i=0; i < num_of_modules; i++){
    // Stepper motor has 4 control pins connected to the driver
    for(int j=0; j < 4; j++){
      pinMode(motor_driver_pins[i][j], OUTPUT);
    }
    // IR sensor
     pinMode(ir_detection_pins[i], INPUT);
    // Led
     pinMode(led_pin, OUTPUT);
  }
}


// Read Functions

bool is_start_str(char c){
  return c == inbound_start_str;
}

bool is_end_str(char c){
  return c == inbound_end_str;
}


// Write Functions

String construct_outbound_msg(String msg) {
  return outbound_start_str + msg + outbound_end_str;
}

void writeStringtoSerial(String stringData) {
  for (int i = 0; i < stringData.length(); i++) {
    Serial.write(stringData[i]);   // Push each char 1 by 1 on each loop pass
  }
}


//Instruction Functions

String process_instruction(String instruction){
  if(inbound_str[0] == 'L'){
    return run_led_instruction(inbound_str);
  }
  else if(inbound_str[0] == 'P'){
    return run_prepare_drop_instruction(inbound_str);
  }
  else if(inbound_str[0] == 'R'){
    return run_repeat_prepare_drop_instruction(inbound_str);
  }
  else if(inbound_str[0] == 'D'){
    return run_drop_instruction(inbound_str);
  }
  else if(inbound_str[0] == 'V'){
    return run_verification_instruction(inbound_str);
  }
  else if(inbound_str[0] == 'C'){
    return run_calibration_instruction(inbound_str);
  }
}

String run_calibration_instruction(String instruction){
  // Move motor to calibrate to position 0
  char module_char = instruction[1];
  int module_num = convert_char_to_int(module_char);
  int step_num_1 = convert_char_to_int(int(instruction[2]));
  int step_num_2 = convert_char_to_int(int(instruction[3]));
  int step_num_3 = convert_char_to_int(int(instruction[4]));
  int step_num_combine = (step_num_1*100) + (step_num_2*10) + step_num_3;
  int step_num = int(float(step_num_combine /360.0) * steps_in_one_rotation);
  rotation(counterclockwise, module_num, step_num);
  return instruction + 'Y';
}

String run_led_instruction(String instruction){
  // Turn on/off an led
  if(instruction[1] == 'H'){
    // Led on
    digitalWrite(led_pin, HIGH);
  }
  else if(instruction[1] == 'L'){
    // Led off
    digitalWrite(led_pin, LOW);
  }
  return instruction + 'Y';
}

String run_verification_instruction(String instruction){
  // Verify if pill has been dropped
  char module_char = instruction[1];
  int module_num = convert_char_to_int(module_char);
  int ir_value = analogRead(ir_detection_pins[module_num]);
  Serial.println(ir_value);
  if(ir_value < ir_sensor_limit){
    return instruction + 'Y';
  }
  else{
    return instruction + 'N';
  }
}

String run_prepare_drop_instruction(String instruction){
  // Prepare to drop a pill with 7/8 rotation
  char module_char = instruction[1];
  int module_num = convert_char_to_int(module_char);
  int step_num = (steps_in_one_rotation * 7) / 8;
  rotation(counterclockwise, module_num, step_num);
  return instruction + 'Y';
}

String run_repeat_prepare_drop_instruction(String instruction){
  // Repeat prepare to drop a pill with one rotation
  char module_char = instruction[1];
  int module_num = convert_char_to_int(module_char);
  int step_num = steps_in_one_rotation - 2;
  rotation(counterclockwise, module_num, step_num);
  return instruction + 'Y';
}

String run_drop_instruction(String instruction){
  // Drop a pill with 1/8 rotation
  char module_char = instruction[1];
  int module_num = convert_char_to_int(module_char);
  int step_num = steps_in_one_rotation / 8;
  rotation(counterclockwise, module_num, step_num);
  return instruction + 'Y';
}


//Motor Functions

void rotation(fcntype fcn, int module_num, int steps){
  for(int i=0; i<steps; i++){
    fcn(module_num);
  }
}

void clockwise(int module_num){
  for(int i = 7; i >= 0; i--){
    set_motor_output(module_num, i);
    delayMicroseconds(motor_speed);
  }
}

void counterclockwise(int module_num){
  for(int i = 0; i < 8; i++){
    set_motor_output(module_num, i);
    delayMicroseconds(motor_speed);
  }
}

void set_motor_output(int module_num,int out){
  for(int i=0; i<4; i++){
    int driver_pin = motor_driver_pins[module_num][i];
    int driver_on_off = bitRead(motor_lookup[out], i);
    digitalWrite(driver_pin, driver_on_off);
  }
}


// Utility Functions

int convert_char_to_int(char c){
  // Only for integers 0-9
  return int(c) - 48;
}








