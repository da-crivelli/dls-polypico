# Linux command line control for Polypico dipenser 
# python 3 style
# v5 :Rying to make both Linux/Windows compartible , SO usb/ IN PORT NAMES 24Apr2023
VER = " V5, Apr 2023 "


from tkinter import filedialog
from tkinter import *
from collections import OrderedDict

import serial

import ast
import time 
import signal
import sys
import glob
#import keyboard
import readchar
import platform


# ==== Constants

AMP_ADJ_DELTA = 0.5 # Half percent

PURGE_CONST = 100
F0 = 16.0 # 16.0 MHz  clock of the strobe timer 

# Serial port

# Operating system have  different port naming 
os = platform.system()
if (os == "Windows"):
    stport = "COM"
    MAXCOMPORTN = 14 # Max COM Port  Number for listing 
else:
    stport = "/dev/ttyUSB"
    MAXCOMPORTN = 4 # Max COM Port  Number for listing 

BAUDRATE = 115200
SER_TIMEOUT = 0.1 # 0.1sec 
# global 
SerialObj = " "
com_name = " "

# Alighment of the menu text 
SWIDITH1 = 52 # String width for padding in the menu 
SWIDITH2 = 30

#=========================================
# Serail port functions

def list_comports(prnt = False):
    
    allPorts = [] #list of all possible COM ports
    for i in range(0,MAXCOMPORTN):
        allPorts.append(stport + str(i))

    if (os == "Windows"):
        allPorts.reverse() # Most likely port is on top
        
    ports = [] #a list of COM ports with devices connected
    k = 1
    for port in allPorts:
        try:
            s = serial.Serial(port) #attempt to connect to the device
            s.close()
            ports.append(port) #if it can connect, add it the the list
            if (prnt):
                print( " ListN = " +str(k)+ " Accesible"  + "  " + str(port) + "  " + str (serial.Serial(port)) )
        except:
            pass #if it can't connect, don't add it to the list
            if (prnt):
                print( (" ListN = " + str(k) + " Unaccesible ").ljust(50,' ') + " " + str(port)  )
        k = k+1
    k = k-1 
    return(ports,k)

#================
def set_serial(com_name, reopen=False):
    global SerialObj
    try:
        print( "Opening " + com_name)
        SerialObj = serial.Serial(com_name)  # COMxx   format on Windows
                                             # ttyUSBx format on Linux
        SerialObj.baudrate = BAUDRATE  # set Baud rate to 9600
        SerialObj.bytesize = 8     # Number of data bits = 8
        SerialObj.parity   ='N'    # No parity
        SerialObj.stopbits = 1     # Number of Stop bits = 1
        SerialObj.timeout = SER_TIMEOUT
        SerialObj.isOpen() # try to open port, if possible print message and proceed with 'while True:'

    except IOError: # if port is already opened, close it and open it again and print message
        if (reopen):
            SerialObj.close()
            SerialObj.open()
            print ("  port was already open, was closed and opened again!  ")
    except:
        print ("\n COM port error !!! ")
        return -1 # bad end
    print (" Opened  Serial Port " + str(com_name)+ str(SerialObj))
    return 1
# ===========

def close_serial():
    global SerialObj
    try:
        SerialObj.close()
    except:
        print ("\n COM port closing error !!! ")
#=============
        
def send_command(cm, show_readback = True):
    global SerialObj
    global com_name
    global Pdisp
    # Setting serial port if not open yet
    if (com_name == " " ):
        com_name = list_comports()[0][ Pdisp.com_port-1 ]

        if ( set_serial(com_name) <=0 ): # proceed
            print (" Serial Port opening error !! ")
            return
    # end of serial port
    
    try: 
        #SerialObj.reset_input_buffer() # for proper readback
        cm = cm.encode()
        SerialObj.write( cm )
        rbline = SerialObj.readline() # readback
        if (show_readback):
            print (" Readback= "+ str(rbline))
        if ( rbline != cm ):
            print ("  !! Wrong response of the Dispense Controller  board !! ")
    except:
        print(" USB error! : is USB connector plugged? ")
    

#===========================================================
# All parameters used for dipensing ( to be copied from dictionary)
class ParamDisp:

    freq = 1000
    amp = 20.0

    pwidth = 50.0

    ext_trig = False
    dispon = False

    pulse_train = 1        

    strobe_amp = 10.0
    strobe_delay = 100.0

    com_port = 1

#global Pdisp
Pdisp = ParamDisp()

# Clip
def myclip (value, rangelist):
        if (value < min (rangelist)):
                value =  min (rangelist)
                print (" Value clipped to the low range ")
                return value
        if (value > max (rangelist )):
                value =  max (rangelist )
                print (" Value clipped to the high range ")
                return value
        return value 


# ---- 
class kontrol():

        smenu = "\n\t\t ***  Main menu : Linux Command Line Polypico Dipenser Controller  { To be run in terminal! } " + VER + "  ***"

        mmenu = ( "Update hardware parameters to current", "Save to File", "Read From File",  "Start Dipensing (Continious or Packet)",  "Stop Dipensing", "Use Internal trigger", "Use External trigger",\
                  "List Serial Ports", "Purge", "Adjust amplitude with +-", "Ping The board", "Exit Program" )

        sdict = "\n -- Parameters menu -- \n"
 
        mdict = { "Dispension Frequency Hz": 100 , "Dipension Amplitude 0..100%":20.0, "Pulse Width":50.0, "Packet Length":1,  \
                  "External (1) or Internal (0)  = 0/1" : 0 , "Dispersion is OFF(0) ON(1) or PACKET (2)  = 0/1/2" : 0 ,
                  "Strobe_delay in uS":100.0, "Strobe_Amplitude":20, "Serial Port ListN: ":1 
                 }
        
        mdict_ranges = { "Dispension Frequency Hz": {10,10000}, "Dipension Amplitude 0..100%":{0.0,100.0}, "Pulse Width":{10.0,100.0}, "Packet Length":{1,10000},  \
                  "External (1) or Internal (0)  = 0/1" : {0,1} , "Dispersion is OFF(0) ON(1) or PACKET (2)  = 0/1/2" : {0,1,2} ,
                  "Strobe_delay in uS":{0.6,312.5}, "Strobe_Amplitude":{0.0,100.0}, "Serial Port ListN: ": {1,   list_comports(False)[1] }
                  }

        mdict = OrderedDict (mdict)
        mdict_ranges = OrderedDict (mdict_ranges)
        
        mdict_recom = mdict.copy() # ssave reccomended values

        Pdisp.com_port = int( mdict["Serial Port ListN: "]) # Comport already copied 

        def menuk(self): 
                print(self.smenu)
                print(" Please choose Menu item or parameter to change by dialing its number and hit Enter  { NumLOCK should be ON if small keaypad is used ! }  : \n")
                k = 0

                for mmd in  self.mmenu :
                        print( str(k)+"\t"+str( mmd ) )
                        k = k+1

                 # other part of menu
                print(self.sdict)
                
                for md in  self.mdict.items() :
                        st1 = str(k)+"\t"+str( md[0] )
                        st1 = st1.ljust(SWIDITH1,' ' )

                        st2 =  str(md[1]) + "\t  reccomended value = " + str(self.mdict_recom[md[0]])
                        st2 = st2.ljust(SWIDITH2,' ' )

                        print( st1 + "\t" + st2 + "\t in range of " + str(self.mdict_ranges[md[0]]) )
                        k = k+1
                        
                while (True):
                        choice = int(input("? "))
                        if ( choice < (len(self.mdict) + len(self.mmenu))  and choice >=0 ):
                                break
                        
                kj = len(self.mmenu) # now seraching for number choice
                
                if (choice >= kj):
                        for md in self.mdict.items():
                                if ( kj == choice):
                                        print( "  was " + str( md[0] )+ "\t" + str(md[1]) )
                                        nv = input(" new value ? ")
                                        if (type (md[1]) == type (0.0) ):
                                            nv = float(nv)
                                        elif (type (md[1]) == type (5) ):
                                            nv = int(nv)
                                        nv = myclip( nv, self.mdict_ranges[ md[0] ] )
                                        self.mdict[md[0]] = nv
                                        break 
                                kj = kj+1
                else:
                                     
                      # now seraching for main menu choice (only remaining possibility) 

                        print( " Menu item choosen  :: " + str( self.mmenu[choice] )+"\n" )

                        if (choice==0 ):
                                self.set_hardware()
                        elif (choice==1):
                                self.savef()
                        elif (choice==2 ):
                                self.readf()

                        elif (choice==3 ):
                             if (self.mdict["Dispersion is OFF(0) ON(1) or PACKET (2)  = 0/1/2"] == 2):
                                 print(" Packet Dipensing activated now !   "  )
                                 Pdisp.pulse_train = int( self.mdict["Packet Length"])
                                 send_command('PN1'+ str (Pdisp.pulse_train) +  '\r')
                                 send_command('PGP' +  '\r')
                             else:
                                print("  Continious Dipensing ... "  )
                                Pdisp.dispon = 1
                                self.mdict["Dispersion is OFF(0) ON(1) or PACKET (2)  = 0/1/2"] = 1
                                send_command('PGD' +  '\r')

                        elif (choice==4):  #  
                                print("  ... STOP!!! "  )
                                Pdisp.dispon = 0
                                self.mdict["Dispersion is OFF(0) ON(1) or PACKET (2)  = 0/1/2"] = 0
                                send_command('PGS' +  '\r')
                                
                        elif (choice==5):  #  
                                print("  Internal trigger choosen "  )
                                self.mdict["External (1) or Internal (0)  = 0/1"] = 0
                                Pdisp.ext_trig == 0
                                send_command('PX0' +  '\r')                                

                        elif (choice==6):  #  
                                print("  External trigger choosen "  )
                                self.mdict["External (1) or Internal (0)  = 0/1"] = 1
                                Pdisp.ext_trig == 1
                                send_command('PX1' +  '\r')

                        elif (choice==7):  #
                                if (SerialObj != " "):
                                    print (" Currently using serial port : \n " + " "+ str(com_name) + "       " + str (SerialObj) )
                                print ( "\n ======== Listing all alternative available Serial Ports ...  " + str( list_comports()[1] ) + ' of serial ports found:  '  )
                                list_comports(prnt = True)
                                print ("\n ======== Listing finished. \n")

                        elif (choice==8):  #
                                print("  Purging ... \n"  )
                                send_command("PC" + str(PURGE_CONST) + '\r')

                        elif (choice==9):  #  
                                print(  "Adjust amplitude using UP and DOWN keyboard arrows , any other key to espace "  )
                                while (True):
                                    key = readchar.readkey()
                                     
                                    if (key == readchar.key.UP):
                                        Pdisp.amp = Pdisp.amp + AMP_ADJ_DELTA
                                        ampd = int ( round (min ( 10.23*Pdisp.amp   , 1023)))
                                        send_command('PA1'+ str (ampd)  + '\r' , show_readback=False )
                                        print ( "\t Amp = "+ "{:6.2f}".format (Pdisp.amp) +" %")
                                    elif (key == readchar.key.DOWN):
                                        Pdisp.amp = Pdisp.amp - AMP_ADJ_DELTA
                                        ampd = int( round (max  ( 10.23*Pdisp.amp  , 0)))
                                        send_command('PA1'+ str (ampd) +  '\r', show_readback=False)
                                        print ( "\t Amp = "+ "{:6.2f}".format(Pdisp.amp) +" %")
                                    else:
                                        print ("\n\n ### Finished incremental  amplitude adjustment ... ")
                                        self.mdict["Dipension Amplitude 0..100%"] = Pdisp.amp
                                        print ( " Finished with Amp = "+ "{:6.2f}".format(Pdisp.amp) +" %")
                                         
                                        break 
                        elif(choice==10):
                                        print(" Pinging the board ... ")
                                        send_command('P?ERR' + '\r' )                                                        
                        elif (choice==11):
                                print("\n Exiting ...\n")
                                if (SerialObj  !=  " "):
                                    close_serial()
                                exit(1)               
                return 0
        # ================================== end of menu 

        def set_hardware(self):
        
                Pdisp.disp = int( self.mdict["Dispension Frequency Hz"])
                send_command('PF'+ str (Pdisp.disp) +  '\r')
                
     
                Pdisp.amp = float( self.mdict["Dipension Amplitude 0..100%"])
                ampd = int (round  ( 10.23*Pdisp.amp  ))
                send_command('PA1'+ str (ampd) +  '\r')

                Pdisp.pwidth = float( self.mdict["Pulse Width"])
                wd = int (round  ( 10.23*Pdisp.pwidth  ))
                send_command('PW1'+ str (wd) +  '\r')

                Pdisp.ext_trig = int( self.mdict["External (1) or Internal (0)  = 0/1"])
                if ( Pdisp.ext_trig == 0):
                        send_command('PX0' +  '\r')
                else:
                        send_command('PX1' +  '\r')                            
                                                     
                Pdisp.dispon = int( self.mdict["Dispersion is OFF(0) ON(1) or PACKET (2)  = 0/1/2"])
                if ( Pdisp.dispon == 0):
                    send_command('PGS' +  '\r')
                elif(Pdisp.dispon == 1):
                    send_command('PGD' +  '\r')
                elif(Pdisp.dispon == 2):
                    send_command('PGS' +  '\r')

                Pdisp.strobe_amp = float( self.mdict["Strobe_Amplitude"])
                ampd = int( round (Pdisp.strobe_amp*10.23) )
                send_command('PS4'+ str (ampd) +  '\r')
                                                     
                Pdisp.strobe_delay = float( self.mdict["Strobe_delay in uS"])
                dd = int( round (Pdisp.strobe_delay*F0)) # F0 =16 Mhz 
                send_command('PS1'+ str (dd) +  '\r')


                print(" Finished configuring Dispenser Controller ")


                
        # +++++++++++++++++ File routines ++++++++++++++

        def readf(self): # Read from file
                print("\n reading file ")
                root = Tk()
                file_path_string = filedialog.askopenfilename( )
                mfile =open(file_path_string,"r+")
                file_string = mfile.read()
                full_dict = ast.literal_eval(file_string)
                print ("file read = \n ",full_dict)
                self.mdict= OrderedDict( full_dict  )
                    #ents_choices = full_dict ['choices']
                mfile.close()
                root.destroy()
            
        def savef(self):# Save to file
            print("\n saving file")
            #self.update()
            root = Tk()
            file_path_string = filedialog.asksaveasfilename( )
            mfile =open(file_path_string,"w+")
            
            data_string = str (dict (self.mdict)) # regular dict out of Ordered Dict 

            mfile.write ( data_string )
            mfile.close()
            root.destroy()

#main() =====================================================================================================

kont = kontrol()
while(True):
        # Looping through paramaters
         kont.menuk()  
 
### END  

# Pins ??
# In case pins are needed for other purposes 
# Note RPI GPIO library GPIOs are different !!!
# Output for the BLOWER
#pBLOW = 20 # (pin 38 of the connector)
#GPIO.setup(pBLOW,GPIO.OUT)
#GPIO.output(pBLOW, GPIO.HIGH)


