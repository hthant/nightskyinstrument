float targetangle = 0; 


void setup() {
  Serial.begin(9600);              //Starting serial communication
}
void loop() {
  Serial.println(Serial.available());
  
  if (Serial.available()){
targetangle =  Serial.parseFloat();
Serial.flush();
  Serial.println(targetangle);
  }
}



