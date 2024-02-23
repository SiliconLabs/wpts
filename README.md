# wpts
Wireshark Packet Trace Server


The Wireshark Packet Trace Server forms a connection between a packet sniffer application such as Wireshark
and hardware running Silicon Labs railtest firmware connected to PC's serial port.

Please refer to 
https://www.silabs.com/documents/public/user-guides/ug409-railtest-users-guide.pdf
for more information on this application. 

You can build the railtest application for any of the silicon Labs supported platforms and the sniffer should work with that. 
The wpts has been tested on MG21 based devices and on Simplicity Studio Version: SV5.8.1.0
Please refer to silicon Labs website https://www.silabs.com/ for further details on HW, Simplicity Studio and other developer resources.
 
The server receives the data frames over the serial interface, packages it with a short header in UDP datagrams 
and sent to a specified host IP address.

The packet sniffer application must be run on the same PC as this application.

#Using wpts with wireshark

Install the latest version of wireshark 
https://www.wireshark.org/download.html

The Wireshark installer contains the latest Npcap installer.

If you don’t have Npcap installed you won’t be able to capture live network traffic but you will still be able to 
open saved capture files. By default the latest version of Npcap will be installed. 
If you don’t wish to do this or if you wish to reinstall Npcap you can check the Install Npcap box as needed.
For more information about Npcap see https://npcap.com/ and https://gitlab.com/wireshark/wireshark/-/wikis/Npcap.

#Manual Npcap Installation
As mentioned above, the Wireshark installer also installs Npcap. 
If you prefer to install Npcap manually or want to use a different version than the one included in the Wireshark installer, 
you can download Npcap from the main Npcap site at https://npcap.com/.


#Capturing traffic on wireshark
1. Open wireshark application
2. From the Menu options select capture->Refresh Interfaces
3. From the list of interfaces listed , place cursor and highlight "Adapter for loopback traffic capture"
4. In the box adjacent to ...using this filter , add "udp port 17754" and press enter
5. This should now open the wireshark capture
 

Usage example for the Wireshark Packet Trace Server:

C:\wpts> python "Wireshark Packet Trace Server.py"
Available ports :  ['COM3']
Select the port to connect: COM3
port is opened!
enter the channel: 14

