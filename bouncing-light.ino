#define NPINS 10

const int freq = 20;

void setup() {
  // put your setup code here, to run once:
  for (int i = 0; i < NPINS; i++) {
    pinMode(i, OUTPUT);
  }
}

void loop() {

  // for(int i = 0; i < NPINS; i++) {
  //   digitalWrite(!i ? NPINS-1 : i-1, LOW);
  //   digitalWrite(i, HIGH);
  //   delay(int(1000/freq));
  // }
  int dir = 1;
  int i = 0;
  int last_pin = 0;
  
  while (1) {
    digitalWrite(last_pin, LOW);
    digitalWrite(i, HIGH);
    
    last_pin = i;
    i += dir;
    
    if (i == 0)
      dir = 1;
    else if (i == NPINS-1)
      dir = -1;

    delay(int(1000/freq));
  }

}
