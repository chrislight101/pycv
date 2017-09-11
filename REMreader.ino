const int SAMPLERATE = 50;
const int ARRAY10S = SAMPLERATE * 10;
const int ARRAY30S = 3;

int sensorValue;
static int samples[ARRAY10S] = {0};
static int i;
static long long sum;
static long avg;
static int delayms;
static int count;
unsigned long time;

int freeRam () {
  extern int __heap_start, *__brkval; 
  int v; 
  return (int) &v - (__brkval == 0 ? (int) &__heap_start : (int) __brkval); 
}
void printTime(){
  Serial.print("Time: ");
  time = millis();
  //prints time since program started
  Serial.println(time);
}

void setup() {
  Serial.begin(9600);
  i = 0;
  sum = 0;
  count = 0;
  delayms = 1000 / SAMPLERATE;
}

void loop() {
  sampleAndAvg();
}

// sample without average
void simpleSample() {
  sensorValue = analogRead(A0);  
  Serial.println(sensorValue);

  delay(delayms);
}

// sample at specified rate and average
void sampleAndAvg() {
  sum -= samples[i];
  sensorValue = analogRead(A0);
  samples[i] = sensorValue;
  sum += samples[i];
  i++;
  i = i % ARRAY10S;
  if (count < ARRAY10S) count++;
  
  avg = sum / count;

  Serial.print(sensorValue);
  Serial.print("\t");
  Serial.println(avg);
  
  delay(delayms); // 20ms delay between samples for 50Hz sample rate
}

