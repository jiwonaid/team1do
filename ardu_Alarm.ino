#include <LoRaShield.h>

// digital pin 
int LED_Pin = 13;

int speakerPin = 12;
int numTones = 10;
int tones[] = {261, 330, 392, 261};


// LoRa Shield RX = 10 / TX = 11 
LoRaShield LoRa(10, 11);

void setup() {
  
  // Serial Port setup 
  Serial.begin(115200);

  LoRa.begin(38400);
// Room Light initialize 
//  roomLight.begin();
  pinMode(LED_Pin, OUTPUT);

}

// Global counter for sensor interval 
// int cnt = 0;

void loop() {

  while (LoRa.available())  {
    // ReadLine 필수 구현 
    String s = LoRa.ReadLine();
    Serial.println(s);

    // LoRa 네트워크 수신 사용자 정의 제어 명령 
    String m = LoRa.GetMessage();
 if (m == "280100") {
      Serial.println("[[ Light Off ]]");
      digitalWrite(13, LOW);
      for (int i = 0; i < numTones; i++) {
       tone(speakerPin, tones[i]);
       delay(500);
      }
      noTone(speakerPin);
    }
    else if (m == "280101") {
      Serial.println("[[ Light On ]]");
      digitalWrite(13, HIGH);
      for (int i = 0; i < numTones; i++) {
       tone(speakerPin, tones[i]);
       delay(500);
      }
      noTone(speakerPin);
      delay(1000);
      digitalWrite(13, LOW);
    } 
  } }

