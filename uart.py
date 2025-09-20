'''
Created on Jun 8, 2018

@author: David
'''
# serial interface functions

import struct
import serial
#import definitions


def openUART():
    """ This function will open the uart port """
#    PORT = 'COM9'
    PORT = '/dev/ttyUSB0'
    BAUDRATE = 19200
    BYTESIZE = serial.EIGHTBITS
    PARITY = serial.PARITY_NONE
    STOPBITS = serial.STOPBITS_ONE
    XONOFF = True
    ser = serial.Serial(PORT, BAUDRATE, BYTESIZE, PARITY, STOPBITS, XONOFF)
    ser.timeout = None
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    print (ser.name)
    return(ser)


def close(ser):
    """ This function will close the uart port """
    print 'closing UART port'
    ser.reset_input_buffer()
    ser.reset_output_buffer()

    ser.close()


def send(ser, value):
    """ This function will send a value to the uart port """
    ser.write(value)


def receive(ser, no_bytes):
    """ This function will receive a packet from the uart port """
    result = ser.read(no_bytes)
    return result


def sendCommand(ser, command):
    """ This function will send a command to the console """
    ser.write(command)
