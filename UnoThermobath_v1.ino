
//13Mar2018 WWD
//playing around with using Arduino to read from serial communications with water bath
//need RS-232 chip to do that
char incomingByte;
unsigned long milli = millis();

void setup() {
  // send data only when you receive data:
  Serial.begin(19200);
  }

void loop() {
  // put your main code here, to run repeatedly:
  while (milli < 30000); {
    milli = millis();
    //Serial.println(milli);
    if (Serial.available() > 0) {
    Serial.write("RS\r");
    // read the incoming byte:
    incomingByte = Serial.read();
    }
    unsigned long milli = millis();
    Serial.write("SS 32.00\r");
    incomingByte = Serial.read();
    Serial.write("RS\r");
    incomingByte = Serial.read();
  }
}
