# ROB5_SAF_Mini_Project
TCP Client-Server to inferface with FESTO PLCs

### Desctiption

The miniproject includes two programs:

    A PLC program (TCP client) that controls the physical system (FESTO PLC)
    A PC program (TCP server) that monitors the behavior of the physical system.

The programs perform the following operations:

    Reads the pallet RFID tag when a pallet moves to the module you are working on
    Sends the RFID info to a PC via TCP/IP as an XML-encoded string
    The PC program decodes the information and displays the relevant information on screen during program execution
    The PC program returns an estimated processing time to the PLC via TCP/IP
    The PLC simulates the physical processing time by letting the pallet wait for the returned time.
    The decoded data is stored in a file on the PC, so that it can be analyzed later.

The "estimated processing time" is given a priori as a CSV-file and is read into memory before realtime execution on the PC.

### How to run

TCP Server and Client are runned separatelly. First, Server needs to be runned. Make sure that both programs have the same IP address and Port number. The Port number has to be a four digit number bigger than 1023, to avoid accessing privileged ports. The IP address is the IPv4 address of the Server. Note that the IP address changes every time the host where the Server is running establishes a new internet connection, if the addresses are assigned dynamically.

Once that is set up, in the terminal go to the file location of the TCP Server and run `python Server.py`. Next step is to run the TCP Client. To do that import the Rob563SAFMiniProject.project into Codesys, then Login with online change or login with download and press the Run button. 

To verify if the connection was established, look for a similar print in the terminal where Server is running: `Connected by ('172.20.15.1', 35578)` where IP and Port are examples of TCP Client information, and in your case there will be different values. 
