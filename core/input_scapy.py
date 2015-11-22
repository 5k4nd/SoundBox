# -*- coding: utf8 -*-

import socket
from threading import Thread
from random import randint
from time import sleep
from sys import exc_info


class daemon_glove(Thread):
    '''reçoit des packets IP en provenance de l'iPhone et les formate.

    > une classe fille 'daemon_data_network' se charge de recevoir les
        données brutes depuis l'iPhone.

    > la classe mère 'daemon_glove' se charge de les formater et de les rendre
        accessible au core via sa méthode get_data_glove

    '''

    def __init__(self, mode="ACC"):
        def init_formated_data(mode):
            if mode == "ACC":
                return {
                    'loggingTime': 0,
                    'loggingSample': 0,
                    'identifierForVendor': 0,
                    'accelerometerTimestamp_sinceReboot': 0,
                    'accelerometerAccelerationX': 0,
                    'accelerometeraccelerationY': 0,
                    'accelerometeraccelerationZ': 0
                }
        def init_raw_data(mode):
            if mode == "ACC":
                return [0]*7

        Thread.__init__(self)
        self.mode = mode  # à passer en paramètres plus tard
        self.erreurs = "none"
        self.raw_data = init_raw_data(mode)
        self.formated_data = init_formated_data(mode)

        # currently not used
        """
        self.DATASCHEME = [
            'loggingTime',
            'loggingSample',
            'identifierForVendor',
            'deviceID',
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
            'motionMagneticFieldCalibrationAccuracy',
            'IP_en0',
            'IP_pdp_ip0',
            'deviceOrientation',
            'batteryState',
            'batteryLevel',
            'state'
        ]
        """


    def run(self):
        self.d_data_network = daemon_glove.daemon_data_network(
            mother_ref=self,
            HOSTIP='192.168.1.12',
            HOSTPORT='508'
        )
        self.d_data_network.start()
        
        while 1:
            sleep(.01)
            if self.mode == 'ACC':
                self.formated_data = {
                    'loggingTime': self.raw_data[0],
                    'loggingSample': self.raw_data[1],
                    'identifierForVendor': self.raw_data[2],
                    'accelerometerTimestamp_sinceReboot': self.raw_data[3],
                    'accelerometerAccelerationX': self.raw_data[4],
                    'accelerometeraccelerationY': self.raw_data[5],
                    'accelerometeraccelerationZ': self.raw_data[6]
                }

                #print self.formated_data['loggingSample']
                #print self.formated_data['accelerometerTimestamp_sinceReboot']

            #axe de roulis
                #xData = float(self.formated_data['accelerometerAccelerationX'])
                #print str(xData)
                #sound_map(12, 5, xData)

            #axe de tangage
                #yData = float(self.formated_data['accelerometerAccelerationY'])
                #print str(yData)
                #sound_map(12, 30, yData)

            #axe de roulis ?
                #zData = float(self.formated_data['accelerometerAccelerationXZ'])
                #print str(zData)
            

    def get_data_glove(self):
        return self.formated_data

    def kill_daemon_data_network(self):
        self.d_data_network._Thread__stop()


    class daemon_data_network(Thread):
        """thread fille qui reçoit la donnée brute en continue sur le réseau
            avec TCP et des sockets.
            
        > pousse ses données brutes 'raw_data' directement
            dans mother_daemon_glove

        ToDo:
            - implémenter un truc pour relancer ce thread si on l'arrête pour
            une quelconque raison

        """

        def __init__(self, mother_ref, HOSTIP, HOSTPORT):
            Thread.__init__(self)
            self.HOSTIP=HOSTIP
            self.HOSTPORT=HOSTPORT
            self.getting_data=True  # réception réseau ON/OFF
            self.old_raw_data={}
            self.mother_daemon_glove=mother_ref

        def run(self):
            mode_len = 7
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(('192.168.1.12', 508))
                # self.sock.connect((HOSTIP, PORT))
                while 1:
                    sleep(.01)
                    receivedData = sock.recv(1024).split(',')
                    if len(receivedData) == mode_len:
                        try:
                        # I check the second field which is the count.
                        # integer means (it's just stats, hum!) data is not corrupted
                            temp = int(receivedData[1])
                            self.mother_daemon_glove.raw_data = receivedData
                            old_raw_data = self.mother_daemon_glove.raw_data
                        except:
                        # if data is corrupted, we pass the old one for this loop
                            self.mother_daemon_glove.raw_data = old_raw_data
                            pass
                        
            except:
                self.mother_daemon_glove.erreurs = "> socket errors: "\
                    + str(exc_info())
            #except socket.error, exc:
                #self.mother_daemon_glove.erreurs = exc


        def stop_reception(self):
            self.getting_data=False




# pour les tests de réception
# rappel, en console : 'nc 192.168.1.12 508'
if __name__ == '__main__':
    from os import system
    d_glove = daemon_glove()
    d_glove.start()
    sleep(.01)  # wait, pour être sûr que les thread soient bien lancés
    for i in range(1, 5000):
        system('clear')
        print d_glove.raw_data
        print d_glove.erreurs
        sleep(.001)
    d_glove.kill_daemon_data_network()
    d_glove._Thread__stop()
