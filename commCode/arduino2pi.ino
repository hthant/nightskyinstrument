int ib = 0; 
int no = 0;
String s = "";
int n = 0;
void setup() {
  Serial.begin(9600);              //Starting serial communication
}
void loop() {
  if(Serial.available() > 0) {
    ib = Serial.read();
    if(ib == 48) no = 0;
    else if(ib == 49) no = 1;
    else if(ib == 50) no = 2;
    else if(ib == 51) no = 3;
    else if(ib == 52) no = 4;
    else if(ib == 53) no = 5;
    else if(ib == 54) no = 6;
    else if(ib == 55) no = 7;
    else if(ib == 56) no = 8;
    else if(ib == 57) no = 9;
    else Serial.println();
//    s = s+String(no);
//  }
//  n = atoi(s);
}
    Serial.println(no);
}

