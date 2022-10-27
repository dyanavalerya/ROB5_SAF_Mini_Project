import csv
import socket
import xml.sax

class ParseRFIDData(xml.sax.handler.ContentHandler):

    def __init__(self):
        self.currentTag = ""
        # initialize a list of strings
        self.data = []

    def print(self):
        print(self.data)

    def startElement(self, name, attrs):
        self.currentTag = name
        if name == "RFID":
            print("\nRFID data parsed from XML file: ")

    def characters(self, content):
        if self.currentTag == "carrierID":
            self.data.append(content)
        elif self.currentTag == "stationID":
            self.data.append(content)
        elif self.currentTag == "dateAndTime":
            self.data.append(content)


    def endElement(self, name):
        self.currentTag = ""


#  Function to return indices of a given
#  string from the multidimensional array

def findIndex(stringArr, keyString):
    #  Initialising result array to -1
    #  in case keyString is not found
    result = []

    #  Iteration over all the elements
    #  of the 2-D array

    #  Rows
    for i in range(len(stringArr)):

        #  Columns
        for j in range(len(stringArr[i])):
            #  If keyString is found
            if stringArr[i][j] == keyString:
                result.append(i)
                result.append(j)
                return result
    result.append(-1)
    result.append(-1)
    #  If keyString is not found
    #  then -1 is returned
    return result

# If you pass an empty string, the server will accept connections on all available IPv4 interfaces.
# HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
HOST = "172.20.66.106"
PORT = 6666  # Port to listen on (non-privileged ports are > 1023)
SIZE = 512
FORMAT = "utf-8"

def main():
    # Parse the CSV file containing the processing times for each carrier
    file = open('procssing_times_table.csv')

    type(file)

    csvreader = csv.reader(file, delimiter=';')

    processing_times_rows = []
    for row in csvreader:
        processing_times_rows.append(row)

    # TCP Server Connection

    # socket type. AF_INET is the Internet address family for IPv4
    # SOCK_STREAM is the socket type for TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Close the socket left open by a killed program
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # The .bind() method is used to associate the socket with a specific network interface and port number
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        # The with statement is used with conn to automatically close the socket at the end of the block
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(512)
                if str(data) == "b'\\x00'":
                    break
                elif not data:
                    break
                with open("plc_data.xml", "w") as f:
                    # Remove last elements after and including "end" from the incoming string, and the first two elements - b',
                    # since we don't want them as part of the XML file
                    f.write(str(data).split("b'", 1)[1].split("end", 1)[0])

                # Parse the XML data received by the TCP Client
                rfid_data = ParseRFIDData()
                parser = xml.sax.make_parser()
                parser.setContentHandler(rfid_data)
                parser.parse('plc_data.xml')
                rfid_data.print()

                processing_time = 0
                keyString = processing_times_rows[0][int(rfid_data.data[1].split("STPLC_", 1)[1])]
                stationPos = findIndex(processing_times_rows, processing_times_rows[0][int(rfid_data.data[1].split("STPLC_", 1)[1])])[1]
                carrierPos = findIndex(processing_times_rows, processing_times_rows[int(rfid_data.data[0])][0])[0]

                # loop through rows containing carrier IDs
                for row in range(1, len(processing_times_rows)):
                    # loop through columns representing station IDs
                    for col in range(1, len(processing_times_rows[0])):
                        # if carrier number in the csv file is the same as carrier number sent by the plc
                        # and if the station number in the csv file (containing processing times) is the same
                        # as the station number sent by the plc
                        # then access the specific processing time for that case
                        if processing_times_rows[row][0].split("Carrier#", 1)[1] == rfid_data.data[0] and processing_times_rows[0][col].split("Station#", 1)[1] == rfid_data.data[1].split("STPLC_", 1)[1]:
                            processing_time = processing_times_rows[carrierPos][stationPos]

                print(processing_time)
                # conn.send(str(processing_time).encode(FORMAT))
                # send data back to the TCP client
                conn.sendall(processing_time.encode())

if __name__ == "__main__":
    main()