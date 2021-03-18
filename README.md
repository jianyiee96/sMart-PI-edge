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
