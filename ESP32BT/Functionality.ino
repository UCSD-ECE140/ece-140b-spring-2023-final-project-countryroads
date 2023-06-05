void setupButtons() {
  pinMode(15, INPUT_PULLUP); // Let Me Merge
  pinMode(4, INPUT_PULLUP); // Going Right
  pinMode(5, INPUT_PULLUP); // Going Left
  pinMode(18, INPUT_PULLUP); // Going Forward
  pinMode(19, INPUT_PULLUP); // Going Back
  pinMode(21, INPUT_PULLUP); // Connect
  pinMode(22, INPUT_PULLUP); // Disconnect
  pinMode(23, OUTPUT); // BTLED
  pinMode(32, OUTPUT); // sentDataLED
}

void createBluetooth() {
  if (!BLE.begin()) {
    // Serial.println("Starting BLE failed!");
    while (1);
  }
  BLE.setLocalName("CountryRoadsController");
  BLE.setAppearance(0x06);
  BLE.setAdvertisedService(crService);
  crService.addCharacteristic(crCharacteristic);
  BLE.addService(crService);
}

void searchConnection() {
  BLE.advertise();
  // Serial.println("Searching for Connection");
  connection = 1;
  advertised = 1;
  delay(1000);
}

void disconnectBluetooth() {
  BLE.disconnect();
  BLE.stopAdvertise();
  // Serial.println("Disconnecting");
  connection = 0;
}

void searchBTLED() {
  digitalWrite(23, HIGH);
  delay(100);
  digitalWrite(23, LOW);
  delay(99);
}

void onBTLED() {
  digitalWrite(23, HIGH);
}

void offBTLED(){
  digitalWrite(23, LOW);
}

void stopSearch(){
  advertised = 0;
  connection = 0;
  BLE.stopAdvertise();
  // Serial.println("Stopped Searching");
  delay(1000);
}

void confirmDataSent(){
  digitalWrite(32, HIGH);
  delay(100);
  digitalWrite(32, LOW);
  delay(10);
  digitalWrite(32, HIGH);
  delay(100);
  digitalWrite(32, LOW);
}