// String constants
const char inbound_start_str = '<';
const char inbound_end_str = '>';
const char outbound_start_str = '{';
const char outbound_end_str = '}';

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

// States
char incoming_byte;
String read_str = "";

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
          read_str += incoming_byte;
        }
      } while(!is_end_str(incoming_byte));

      // TODO after getting instruction
      read_str.trim();
      check_led_instruction();
      check_drop_instruction();
      check_verification_instruction();
      Serial.println(construct_outbound_msg(read_str));
      read_str = "";
    }
  }
}

String construct_outbound_msg(String msg) {
  return outbound_start_str + msg + outbound_end_str;
}

bool is_start_str(char c){
  return c == inbound_start_str;
}

bool is_end_str(char c){
  return c == inbound_end_str;
}

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

void check_led_instruction(){
  // Turn on/off an led
  if(read_str[0] == 'L'){
    if(read_str[1] == 'H'){
      // Led on
      digitalWrite(led_pin, HIGH);
    }
    else if(read_str[1] == 'L'){
      // Led off
      digitalWrite(led_pin, LOW);
    }
  }
}

void check_verification_instruction(){
  // Verify if pill has been dropped
  if(read_str[0] == 'V'){
    int module_num = read_str[1];
    int ir_value = analogRead(ir_detection_pins[module_num]);
    // TODO send back info about pin
  }
}

int convert_char_to_int(char c){
  // Only for integers 0-9
  return int(c) - 48;
}


void check_drop_instruction(){
  // Drop a pill with one rotation
  if(read_str[0] == 'D'){
    char module_char = read_str[1];
    int module_num = convert_char_to_int(module_char);
    one_cw_rotation(module_num);
  }
}

void one_cw_rotation(int module_num){
  for(int i=0; i<steps_in_one_rotation; i++){
    clockwise(module_num);
  }
}

void one_ccw_rotation(int module_num){
  for(int i=0; i<steps_in_one_rotation; i++){
    counterclockwise(module_num);
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


