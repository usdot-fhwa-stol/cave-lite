This mobile.sh script will listen to broadcasts in the network it is connected to and broadcast to the same network.
It is specifically looking for SAE J2735 SPaT messages. Once SPaT is received, the message is decoded and phase information 
is extracted. This phase state and timing information is used to control the motor of a 1/10th scale vehicle. 

The following prerequisites can be installed using the script found at scripts/install_dependencies.sh

Prerequisites: 
* python3
* gpiozero

Mobile Kit Raspberry Pi default Static IP set to: 192.168.0.110

1. Install dependencies:
	```
	cd ~/cave-lite/scripts
	sudo ./install_dependencies.sh
	```

2. Run mobile kit:
	```
	cd ~/cave-lite/src/mobile
	bash mobile.sh
	```
	
3. To stop script: 
	```
	<Ctrl-C>
	```
