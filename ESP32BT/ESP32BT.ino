#include <ArduinoBLE.h>

int connection = 0;
int advertised = 0;
BLEService crService("99a1f7e6-2827-4ac4-8130-c58416fdac68");
BLEStringCharacteristic crCharacteristic("10b4b19c-d0f2-4571-9363-6c52986587df", BLERead | BLEWrite | BLENotify, 20);

void setup() {
  Serial.begin(9600);
  setupButtons();
  createBluetooth();
}

void loop() {
  if(digitalRead(21) == LOW){
    if(advertised) {
      stopSearch();
    } else {
      searchConnection();
    }
  } else if(connection){
    searchBTLED();
    BLEDevice central = BLE.central();
    if (central) {
      // Serial.println("Connected to:" + central.address());
      onBTLED();
      while (central.connected()) {
        if (digitalRead(15) == LOW) {
          crCharacteristic.writeValue("Merge");
          confirmDataSent();
        } else if(digitalRead(4) == LOW){
          crCharacteristic.writeValue("Right");
          confirmDataSent();
        } else if(digitalRead(5) == LOW){
          crCharacteristic.writeValue("Left");
          confirmDataSent();
        } else if(digitalRead(18) == LOW){
          crCharacteristic.writeValue("Forward");
          confirmDataSent();
        } else if(digitalRead(19) == LOW){
          crCharacteristic.writeValue("Backward");
          confirmDataSent();
        } else if(digitalRead(22) == LOW){
          disconnectBluetooth();
        } 
      }
      // Serial.println("Disconnected from Device: " + String(central.address()));
      offBTLED();
      connection = 0;
      advertised = 0;
    }
  }
}

