#include <Entropy.h>
const int sizex = 171;
const double delay_us = 1000;
const int Range_lower = 0;
const int Range_higher = 10;
unsigned int array[sizex];
double one = 1.0;
void setup() 
{
  Entropy.Initialize();
  pinMode(LED_BUILTIN, OUTPUT);
   //Fill the array
   //Serial.addMemoryForWrite(serial_buffer, 256)
}

void loop() 
{
  while(true){
      
      digitalWrite(LED_BUILTIN, HIGH);
 
      for (int i=0; i < sizex; i++) 
      {
        array[i] = Entropy.random(Range_lower, Range_higher);
      }
      
      Serial.write((uint8_t*)&(array), sizeof(unsigned int)*sizex);

      //----
      
      digitalWrite(LED_BUILTIN, LOW);
      delayMicroseconds(delay_us);
  } //Infinite Loop Block
}
