#include <SoftwareSerial.h>
#include <SPI.h>
#include <MFRC522.h>

SoftwareSerial microbitSerial(2, 3);
MFRC522 mfrc522(10, 9);

void setup() {
    SPI.begin();        
    mfrc522.PCD_Init();
    microbitSerial.begin(9600);
}

void loop() {
    if (!mfrc522.PICC_IsNewCardPresent())
        return;

    if (!mfrc522.PICC_ReadCardSerial())
        return;

    transmit_byte_array(mfrc522.uid.uidByte, mfrc522.uid.size);
    delay(1000);
}

void transmit_byte_array(byte *buffer, byte bufferSize) {
    if(bufferSize > 4) {
        bufferSize = 4;
    }
    for (byte i = 0; i < bufferSize; i++) {
        if(buffer[i] < 0x10) {
            microbitSerial.print("0");
        }
        microbitSerial.print(buffer[i], HEX);
    }
    microbitSerial.print("=");
}
