## Overview
CAVe-Lite is the smaller version of CAVe-in-a-Box. CAVe-Lite is meant to be used in a classroom setting to teach and demonstrate
the network connections and message flow for SAE J2735 messages. This script will allow for a SPaT (Signal Phase and Timing) message to 
be translated from a pre-recorded Traffic Signal Controller (NTCIP 1202) message. The SPaT Message is broadcast to the network the 
Raspberry Pi is connected to. A traffic light and CARMA 1-Tenth or CAVe-Mobile vehicle are used to demonstrate how SAE J2735 Messages can be used. 

Instructions for using CAVe-Mobile can be found in the src/mobile folder. Dependencies are installed using the same script below.

The attached NTCIP 1202 cycle contains the following signal phases:
Green state = 15 seconds
Yellow state = 3 seconds
Red state = Green + Yellow + 2 second all phases red (20 seconds)

## Prerequisites:
* V2X Hub (arm64, latest) https://github.com/usdot-fhwa-OPS/V2X-Hub
* V2X Hub installation instructions: https://usdot-carma.atlassian.net/wiki/spaces/V2XH/pages/1886158849/V2X-Hub+Docker+Deployment


## Usage
CAVe-Lite Raspberry Pi default Static IP set to: 192.168.0.146

1. Install dependencies:
	```
	cd ~/cave-lite/scripts
	./install_dependencies.sh
	```

2. To run:
	```
	cd ~/cave-lite/src/infrastructure
	./rc.local start
	```

3. To stop:
	```
	./rc.local stop
	```

## License information
Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
