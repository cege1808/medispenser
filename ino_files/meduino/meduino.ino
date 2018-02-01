const char inbound_start_str = '<';
const char inbound_end_str = '>';
const char outbound_start_str = '{';
const char outbound_end_str = '}';

const int baudrate = 9600;

const int num_of_modules = 3;
const int motor_driver_pins[3][4] = { {2,3,4,5}, {6,7,8,9}, {10,11,12,13} };
const int ir_detection_pins[3] = {A0,A1,A2};
const int led_pin = A5;

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

