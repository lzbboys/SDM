Simple README for SDM Demo code
Zheng Lu
Dec.13, 2013

0. You need SL4A and python interpreter on your phone to run this demo.
To run main application, run cControl.py
To run calibration application, run magCalib.py

1. cControl.py and sInterpreter.py is our main work. 
The first one include all the control logic and is specialized for the demo.
The second one include all the sensor descriptive algorithms which is not limited to this demo.

2. We implement magnetometer calibration as a seperate part, because we don't need to run it every time. To calibrate, run the magCalib.py and change your phone's orientation as a circle.

3. We only use GPS to get initial location, it's very short, so we merge it in the cControl.py

4. Py4A lack certain map API, so we output our result to an html which is generated based on polyline.temp. The Demo works in an offline mode, but the file is generated in an online way. So it's easy to show the result in an online fashion.

