
# This file is responsible for creating the internet connection and verifying if the connection is established
import network
import time
    
class Connection:

        
    def __init__(self, wifi_name, password):
        
        self.wifi_name=wifi_name
        self.password=password
        self.con = network.WLAN(network.STA_IF)

    # This function is responsible for establishing
    # an internet connection with the data established 
    # in the configuration file, and if a connection 
    # is not achieved within 30 seconds, it abandons the function.
    def createConnection(self):                 

        elapsed_time = 0
        try:
            self.con.active(True)
            self.con.connect(self.wifi_name, self.password)
            while not self.con.isconnected():
                print("connecting...  time elapsed: ", elapsed_time ,"seconds")
                time.sleep(1)
                elapsed_time += 1
                if elapsed_time == 30:
                    break
        except OSError as e:
            print("An error has occurred in the connection: ",e)
        finally:
            if not self.con.isconnected():
                raise Exception("The connection has not been possible, check your name and password")
            else:
                pass
    
    # Checks if the connection is established and returns the status
    def coneectionIsSuccessful(self):
        return self.con.isconnected()
    
        