# SurRender software client interface

The SurRender software is a powerful image renderer developed by the Image Processing Advanced Studies team of Airbus Defence & Space.
It is specially designed for space applications such as vision-based navigation (planetary approach and landing, in orbit rendezvous, etc.). 
It uses raytracing (CPU) or openGL (GPU) and it is highly optimized for space simulations (sparse scenes, reflections and shadows, large distance dynamics, huge datasets). 
Users can input various data at standard formats (Digital Elevation Models, images, meshes), and configure models for various properties such as materials and sensors (shutter type, noises, integration time, etc.). SurRender simulations aim at physical representativeness as needed for the development and validation of  computer vision algorithms.
This GitHub project offers acces to the SurRender client.

## Getting Started

The SurRender software works on a client-server mode using a TCP/IP link. 
The rendering engine runs on the server side. The server may be provided to interested user upon request by contacting surrender.software@airbus.com. Please provide basic information about your project and your institution or company with your demand.
The client connnects to the server using the available interfaces. The GitHub project offers access to the client Python API. 
Once the server is installed, the client is readily usable. First tests can be performed using the demonstration scripts available in the example folder.

## Prerequisite

A standard Python3 installation is required, e.g. Anaconda.
The server is delivered with all the needed dependencies.

## License

This project is licensed under the Apache License Version 2.0 of January 2004. See the LICENSE file for details.
(C) 2019 Airbus copyright all rights reserved

## References

Information about the software is available at <https://www.airbus.com/en/products-services/space/exploration/moon#surrender>
https://arxiv.org/abs/1810.01423 and in the embedded doxygen documentation

