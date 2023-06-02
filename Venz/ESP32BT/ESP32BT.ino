#include <ArduinoBLE.h>

int connection = 0;
int advertised = 0;
BLEService crService("19B10000-E8F2-537E-4F6C-D104768A1214");
BLEStringCharacteristic crCharacteristic("19B10001-E8F2-537E-4F6C-D104768A1214", BLERead | BLEWrite | BLENotify, 20);

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

