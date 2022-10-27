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
