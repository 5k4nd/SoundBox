# -*- coding: utf8 -*-

import threading
import socket
from time import sleep
from curses import start_color, init_pair, color_pair, COLOR_GREEN, COLOR_BLACK


class DataServer:
    """process all our wonderful data, from recept to format.
            all Across the Stars (or, at least, this program)

    Attributes:
      * row_data -- dictionary of SensorLog data

    Methods:
      * getDataThread() -- continuously receives data from smartphone
      * data_format() -- check that data isn't corrupted and then format it for human needs
            return True in case of success, False if data is corrupted

    """
    DATASCHEME = [ # may be useful for data_format() for optimization. maybe list.join() method, or something like that?
    # schema when 'HEAD', 'GYRO', 'ACC' and 'DM' are checked
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
        self.row_data = []
        self.formated_data = {}
        self.getData = True

        thread = threading.Thread(target=self.getDataThread, args=(self.HOSTIP, self.PORT))
        thread.daemon = True
        thread.start()


    def getDataThread(self, HOSTIP, PORT):
        """thread: get data continuously from the network (with socket)"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOSTIP, PORT))
        while self.getData == True:
            receivedData = self.sock.recv(1024).split(',')
            try:
            # I check the second field which is the count.
            # integer means (it's just probability!) data is not corrupted
                temp = int(receivedData[1])
                self.row_data = receivedData
            except:
                self.row_data = [0]
                pass
            sleep(.01) # no need to go too fast!


    def data_format(self):
        """check that data isn't corrupted and then format it for human needs"""
        if len(self.row_data) == 39: #complexifier ce test pour ignnorer les valeurs aberrantes
            self.formated_data = {
                'loggingTime': self.row_data[0],
                'loggingSample': self.row_data[1],
                'locationHeadingTimestamp_since1970': self.row_data[2],
                'locationHeadingX': self.row_data[3],
                'locationHeadingY': self.row_data[4],
                'locationHeadingZ': self.row_data[5],
                'locationTrueHeading': self.row_data[6],
                'locationMagneticHeading': self.row_data[7],
                'locationHeadingAccuracy': self.row_data[8],
                'accelerometerTimestamp_sinceReboot': self.row_data[9],
                'accelerometerAccelerationX': self.row_data[10],
                'accelerometeraccelerationY': self.row_data[11],
                'accelerometeraccelerationZ': float(self.row_data[12]),
                'gyroTimestamp_sinceReboot': self.row_data[13],
                'gyroRotationX': self.row_data[14],
                'gyroRotationY': self.row_data[15],
                'gyroRotationZ': self.row_data[16],
                'motionTimestamp_sinceReboot': self.row_data[17],
                'motionYaw': self.row_data[18],
                'motionRoll': self.row_data[19],
                'motionPitch': self.row_data[20],
                'motionRotationRateX': self.row_data[21],
                'motionRotationRateY': self.row_data[22],
                'motionRotationRateZ': self.row_data[23],
                'motionUserAccelerationX': self.row_data[24],
                'motionUserAccelerationY': self.row_data[25],
                'motionUserAccelerationZ': self.row_data[26],
                'motionAttitudeReferenceFrame': self.row_data[27],
                'motionQuaternionX': self.row_data[28],
                'motionQuaternionY': self.row_data[29],
                'motionQuaternionZ': self.row_data[30],
                'motionQuaternionW': self.row_data[31],
                'motionGravityX': self.row_data[32],
                'motionGravityY': self.row_data[33],
                'motionGravityZ': self.row_data[34],
                'motionMagneticFieldX': self.row_data[35],
                'motionMagneticFieldY': self.row_data[36],
                'motionMagneticFieldZ': self.row_data[37],
                'motionMagneticFieldCalibrationAccuracy': self.row_data[38]
            }
            return True
        else:
        # else, means "erreur réception de données.
        # please check that checkboxes 'HEAD', 'GYRO', 'ACC' and 'DM' are checked"
            return False # we can therefore use the old data, which wasn't corrupted! (except if it's the first loop...)
        



class DataBoard:
    """display data from DataServer, with ncurses
    
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

        # defines ncurses colors
        start_color()
        init_pair(1, COLOR_GREEN, COLOR_BLACK)




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

        elif mode == 'ALL':
        # schema when 'HEAD', 'GYRO', 'ACC' and 'DM' are checked
            print 'toDo!'


    def update_screen(self, mode, datumFocus):
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
            self.scr.addstr(10, 55, str(zData), color_pair(1))
            
            self.scr.refresh()

        elif 'ALL':
        # are 'HEAD', 'GYRO', 'ACC' and 'DM' checked?
            self.scr.addstr(10, 5, str("None"))

