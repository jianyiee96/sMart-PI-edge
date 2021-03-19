### PI-EDGE DOCS

##### Install Dependencies:

On windows: 
```
pip install --upgrade firebase-admin
pip install pandas
```

On Raspberry pi: 
```
sudo pip3 install firebase-admin
sudo pip3 install xlrd
sudo pip3 install openpyxl
sudo apt-get install python3-pandas
sudo apt-get install libatlas-base-dev
```

##### Certificate:

Get `smart-mobile-application-de8a1d29af3c.json` from Me and place it in `files` folder

##### Configs:

Update the `ser` variable into `src/PI/edge_receiver.py` to your serial port.

##### Device and Pins Setup:

Connect RC522 RFID reader to Arduino UNO through this PIN setup:

| RFID-RC522 	| Arduino UNO 	|
|------------	|-------------	|
| 3.3V       	| 3.3V        	|
| RST        	| PIN 9       	|
| GND        	| GND         	|
| IRQ        	| -           	|
| MISO       	| PIN 12      	|
| MOSI       	| PIN 11      	|
| SCK        	| PIN 13      	|
| SDA        	| PIN 10      	|

Connect Micro:bit cart device to Arduino UNO through this PIN setup:

| Micro:bit 	| Arduino UNO 	|
|-----------	|-------------	|
| GND       	| GND         	|
| PIN 0     	| PIN 2       	|
| PIN 1     	| PIN 3       	|

Connect Micro:bit edge device to Raspberry PI using USB.

##### Source Codes:

###### /PI

| File                 	| Description                                       	|
|----------------------	|---------------------------------------------------	|
| edge_receiver.py     	| Main executable file for Raspberry PI device      	|
| excel_utility.py     	| Utility tool for reading sheets from mapping.xlsx 	|
| firestore_utility.py 	| Utility tool for connection with Firestore        	|

###### /Arduino

| File             	| Description                                                                                                                                      	|
|------------------	|--------------------------------------------------------------------------------------------------------------------------------------------------	|
| arduino-cart.ino 	| Reads from RC522 and transmit data to micro:bit using SoftwareSerial.<<br>Requires MFRC522 library installed through Arduino library manager. 	|

###### /Microbit

| File                     	| Description                                                                                                   	|
|--------------------------	|---------------------------------------------------------------------------------------------------------------	|
| micro-cart.js            	| Maintains the item state of cart. <br>Receives data from Arduino and relay actions to micro-edge through radio   	|
| micro-edge.js            	| Receives data from micro-cart and relay to edge_receiver.py through USB Serial                                	|
| micro-cart-simulation.js 	| Simulates adding and removing items from cart<br>Transmit actions to edge_receiver.py through USB Serial      	|