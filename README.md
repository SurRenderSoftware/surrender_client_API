# SurRender software client interface

The SurRender software is a powerful image renderer developed by the Image Processing advanced studies team of Airbus Defence & Space.
It is specially designed for space applications such as vision-based navigation (planetary approach and landing, in orbit rendezvous, etc.). 
It uses raytracing (CPU) or openGL (GPU) and it is highly optimized for space scenes (sparse scenes, reflections and shadows, large distance dynamics, huge datasets). 
Users can input various data at standard formats (Digital Elevation Models, images, meshes), and configure models for various properties such as materials and sensors (shutter type, noises, integration time, etc.). SurRender simulations aim at physical representativeness as needed for the development and validation of  computer vision algorithms.

## Getting Started
The SurRender software works on a client-server mode using a TCP/IP link. 
The GitHub project offers access to the client interface. The client can connnect to the server using the available interfaces, here Python.
The rendering engine runs on the server side. The server may be provided to interested user upon request by contacting surrender.software@airbus.com. Please provide basic information about your project and your institution or company with your demand.
Once the server is installed, the client interfaces are readily usable. First tests can be performed using the demo scripts of the user manual.

## Prerequisite
A standard Python3 installation is prerequisited, e.g. Anaconda.
The server is delivered with all the needed dependencies.

## Running the tests
Start the server in a terminal by runnning 
`./start_server.sh`
Run tests in Python by executing for exemple:
`python3 script_00_installation_control.py`

## Contributing
Users are invited to share their scenarios in a similar format to available examples such as script_08_itokawa_mesh.py and script_09_ceres_landing.py
Self-sufficient explanation should be provided in order to retrieve the needed data.

# License
This project is licensed under the Apache License Version 2.0 of January 2004. See the LICENSE file for details.
(C) 2019 Airbus copyright all rights reserved

### References
Information about the software is available at https://www.airbus.com/SurRenderSoftware.html
https://arxiv.org/abs/1810.01423 and in the embedded doxygen documentation

