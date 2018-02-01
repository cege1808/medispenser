
#define LED 12
// Using http://slides.justen.eng.br/python-e-arduino as refference

void setup() {
    pinMode(LED, OUTPUT);
    Serial.begin(9600);
}

void loop() {
    if (Serial.available()) {
        char serialListener = Serial.read();
        Serial.println(serialListener);
        if (serialListener == 'H') {
            digitalWrite(LED, HIGH);
            Serial.write("LED in high\n");
        }
        else if (serialListener == 'L') {
            digitalWrite(LED, LOW);
            Serial.write("LED in low\n");
        }
    }
}
