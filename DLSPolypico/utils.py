from serial.tools import list_ports


def get_likely_com_port() -> str:
    com_ports = list_ports.comports()

    for port in com_ports:
        print(port.device)

    # # Operating system have  different port naming
    # os = platform.system()
    # if (os == "Windows"):
    #     stport = "COM"
    #     MAXCOMPORTN = 14 # Max COM Port  Number for listing
    # else:
    #     stport = "/dev/ttyUSB"
    #     MAXCOMPORTN = 4 # Max COM Port  Number for listing

    # allPorts = [] #list of all possible COM ports
    # for i in range(0,MAXCOMPORTN):
    #     allPorts.append(stport + str(i))

    # if (os == "Windows"):
    #     allPorts.reverse() # Most likely port is on top

    # ports = [] #a list of COM ports with devices connected
    # k = 1
    # for port in allPorts:
    #     try:
    #         s = serial.Serial(port) #attempt to connect to the device
    #         s.close()
    #         ports.append(port) #if it can connect, add it the the list
    #         if (prnt):
    #             print( " ListN = " +str(k)+ " Accesible"  + "  " + str(port) + "  " + str (serial.Serial(port)) )
    #     except:
    #         pass #if it can't connect, don't add it to the list
    #         if (prnt):
    #             print( (" ListN = " + str(k) + " Unaccesible ").ljust(50,' ') + " " + str(port)  )
    #     k = k+1
    # k = k-1
