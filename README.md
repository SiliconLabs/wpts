# wpts
Wireshark Packet Trace Server


The Wireshark Packet Trace Server forms a connection between a packet sniffer application such as Wireshark
and hardware running Silicon Labs railtest firmware connected to PC's serial port.
 
The server receives the data frames over the serial interface, packages it with a short header in UDP datagrams 
and sent to a specified host IP address.

The packet sniffer application must be run on the same PC as this application.


Usage example:

C:\wpts> python "Wireshark Packet Trace Server.py"
Available ports :  ['COM3']
Select the port to connect: COM3
port is opened!
enter the channel: 14

