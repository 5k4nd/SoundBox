# -*- coding: utf8 -*-

import threading
import socket
from time import sleep

class DataServer:
    """process all our wonderful datum, from reception to formatting.
    all Across the Stars (or, at least, this program)

    Attributes:
      * data -- dictionary of SensorLog data

    Methods:
      * getDataThread() -- continuously receives data from smartphone

    """
    DATASCHEME = [
        'loggingTime',
        'loggingSample',
        'locationHeadingTimestamp_since1970',
        'locationHeadingX',
        'locationHeadingY',
        'locationHeadingZ',
        'locationTrueHeading',
        'locationMagneticHeading',
        'locationHeadingAccuracy',
        'accelerometerTimestamp_sinceReboot',
        'accelerometerAccelerationX',
        'accelerometeraccelerationY',
        'accelerometeraccelerationZ',
        'gyroTimestamp_sinceReboot',
        'gyroRotationX',
        'gyroRotationY',
        'gyroRotationZ',
        'motionTimestamp_sinceReboot',
        'motionYaw',
        'motionRoll',
        'motionPitch',
        'motionRotationRateX',
        'motionRotationRateY',
        'motionRotationRateZ',
        'motionUserAccelerationX',
        'motionUserAccelerationY',
        'motionUserAccelerationZ',
        'motionAttitudeReferenceFrame',
        'motionQuaternionX',
        'motionQuaternionY',
        'motionQuaternionZ',
        'motionQuaternionW',
        'motionGravityX',
        'motionGravityY',
        'motionGravityZ',
        'motionMagneticFieldX',
        'motionMagneticFieldY',
        'motionMagneticFieldZ',
        'motionMagneticFieldCalibrationAccuracy'
    ]


    def __init__(self, HOSTIP, PORT):
        """create an unique instance of DataServer.

        ToDo: 
          * MUST BE UNIQUE => SINGLETON !
                et du coup implémenter un accesseur de cette instance unique :-)
          * implémenter un truc pour mettre en pause le thread de réception de data
                (qu'il arrête VRAIMENT de recevoir au moment de l'appui sur 's' !)

        """
        self.HOSTIP = HOSTIP
        self.PORT = PORT
        self.data = []
        self.getData = True

        thread = threading.Thread(target=self.getDataThread, args=(self.HOSTIP, self.PORT))
        thread.daemon = True
        thread.start()


    def getDataThread(self, HOSTIP, PORT):
        """thread which continuously get data from the network (with socket)"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOSTIP, PORT))
        while self.getData == True:
            receivedData = self.sock.recv(1024).split(',')
            try:
            # I check the second field which is the count.
            # integer means (it's just probability!) data is not corrupted
                temp = int(receivedData[1])
                self.data = receivedData
            except:
                pass
            sleep(.01) # no need to go too fast!

        



class DataBoard:
    """format and display data from DataServer
    
    Attributes:
    X,Y : horizontal and vertical size of the board

    Methods:
    display(update_board) -- If update_board is true, compute the
                             next generation.  Then display the state
                             of the board and refresh the screen.

    """

    def __init__(self, scr):
        """create a new DataBoard instance.

        scr -- curses screen object to use for display
        """
        self.scr = scr
        Y, X = self.scr.getmaxyx()
        self.X, self.Y = X-2, Y-2-1
        self.scr.clear()

        # Draw a border around the board
        border_line = '+'+(self.X*'-')+'+'
        self.scr.addstr(0, 0, border_line)
        self.scr.addstr(self.Y+1,0, border_line)
        for y in range(0, self.Y):
            self.scr.addstr(1+y, 0, '|')
            self.scr.addstr(1+y, self.X+1, '|')
        self.scr.refresh()



    def set_screen(self, mode):
        """set the board depending the mode"""
        self.scr.addstr(2, 5, 'logSample')
        self.scr.addstr(2, 30, 'logTime_sinceReboot')

        if mode == 'ACC':
        #note utile : les axes prennent en compte... l'accélération (obvious!)
        #axe de roulis
            self.scr.addstr(8, 5, 'xAxis')

        #axe de tangage
            self.scr.addstr(8, 30, 'yAxis')

        #axe de roulis ?
            self.scr.addstr(8, 55, 'zAxis')


    def update_screen(self, mode, data):
        """update the board with data received from the phone, formated depending the mode"""
        X,Y = self.X, self.Y

        if mode == 'ACC':
            data = {
                'logTime': data[0],
                'logSample': data[1],
                'logTime_sinceReboot': data[2],
                'xAxis': data[3],
                'yAxis': data[4],
                'zAxis': data[5]
            }

            self.scr.addstr(4, 5, data['logSample'])
            self.scr.addstr(4, 30, data['logTime_sinceReboot'])
        #axe de roulis
            xData = float(data['xAxis'])
            self.scr.addstr(10, 5, str(xData))
            #sound_map(12, 5, xData)

        #axe de tangage
            yData = (float(data['yAxis']))
            self.scr.addstr(10, 30, str(yData))
            #sound_map(12, 30, yData)

        #axe de roulis ?
            zData = float(data['zAxis'])
            self.scr.addstr(10, 55, str(zData))

            
            self.scr.refresh()

    def data_format(self, data):
        if len(data.data) == 39:
            data.data = {
                'loggingTime': data.data[0],
                'loggingSample': data.data[1],
                'locationHeadingTimestamp_since1970': data.data[2],
                'locationHeadingX': data.data[3],
                'locationHeadingY': data.data[4],
                'locationHeadingZ': data.data[5],
                'locationTrueHeading': data.data[6],
                'locationMagneticHeading': data.data[7],
                'locationHeadingAccuracy': data.data[8],
                'accelerometerTimestamp_sinceReboot': data.data[9],
                'accelerometerAccelerationX': data.data[10],
                'accelerometeraccelerationY': data.data[11],
                'accelerometeraccelerationZ': data.data[12],
                'gyroTimestamp_sinceReboot': data.data[13],
                'gyroRotationX': data.data[15],
                'gyroRotationY': data.data[16],
                'gyroRotationZ': data.data[17],
                'motionTimestamp_sinceReboot': data.data[18],
                'motionYaw': data.data[19],
                'motionRoll': data.data[20],
                'motionPitch': data.data[21],
                'motionRotationRateX': data.data[22],
                'motionRotationRateY': data.data[23],
                'motionRotationRateZ': data.data[24],
                'motionUserAccelerationX': data.data[25],
                'motionUserAccelerationY': data.data[26],
                'motionUserAccelerationZ': data.data[27],
                'motionAttitudeReferenceFrame': data.data[28],
                'motionQuaternionX': data.data[29],
                'motionQuaternionY': data.data[30],
                'motionQuaternionZ': data.data[31],
                'motionQuaternionW': data.data[32],
                'motionGravityX': data.data[33],
                'motionGravityY': data.data[34],
                'motionGravityZ': data.data[35],
                'motionMagneticFieldX': data.data[36],
                'motionMagneticFieldY': data.data[37],
                'motionMagneticFieldZ': data.data[38],
                'motionMagneticFieldCalibrationAccuracy': data.data[39]
            }
        # else, means "erreur réception de données.
        # please check that checkboxes 'HEAD', 'GYRO', 'ACC' and 'DM' are checked"
