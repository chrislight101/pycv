int inbyte = 0;
char outbyte = 'x';

void setup() {
  Serial.begin(9600);
}

void loop() {
  //Serial.println(outbyte);
  if(Serial.available() > 0) {
  inbyte = Serial.read();
    Serial.println(inbyte);
  }
}



