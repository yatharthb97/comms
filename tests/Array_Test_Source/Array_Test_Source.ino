#include <Entropy.h>
const int sizex = 1;
const double delay_us = 0;
long int counter;
int array[sizex];

void setup() 
{
  Entropy.Initialize();
  pinMode(LED_BUILTIN, OUTPUT);
   //Fill the array
}

void loop() 
{
  while(true){
      
      digitalWrite(LED_BUILTIN, HIGH);
      counter++;
      for (int i=0; i < sizex; i++) 
      {
        array[i] = counter;
      }

      //-- Send → Serial Out
      for (int i = 0; i < sizex-1; i++) 
      {
        Serial.print(array[i]);
        Serial.print(",");
      }
      Serial.println(array[sizex-1]);
      Serial.flush();
      //----
      
      digitalWrite(LED_BUILTIN, LOW);
      delayMicroseconds(delay_us);
  } //Infinite Loop Block
}
