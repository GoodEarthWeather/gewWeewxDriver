'''
Created on Jun 8, 2018

@author: David
'''

import uart
import struct
import time
import sys
#import syslog
import logging
#from definitions import *

# definitions for ID
NODE_ID = 0xFE
HUB_ID = 0x01

'''
Command dictionaries
A command is defined by 3 items - command name, command id,
and the command length.
Three dictionaries are defined for handling commands -
cmdID - where the key is the command name and the value is the command ID
cmdName - where the key is the command ID and the value is the command name
cmdLength - where the key is the command name, and the value is the packet length (not including the length byte)

'''
cmdID = {}
cmdName = {}
cmdFormat = {}

# define commands
cmdID['CMD_NULL'] = 0
cmdID['CMD_NODE_READY'] = 1
cmdID['CMD_REQ_HT'] = 2
cmdID['CMD_RTN_HT'] = 3
cmdID['CMD_REQ_WIND'] = 4
cmdID['CMD_RTN_WIND'] = 5
cmdID['CMD_REQ_RAIN'] = 6
cmdID['CMD_RTN_RAIN'] = 7
cmdID['CMD_REQ_POWER'] = 8
cmdID['CMD_RTN_POWER'] = 9
cmdID['CMD_REQ_HTP'] = 10
cmdID['CMD_RTN_HTP'] = 11
cmdID['CMD_SET_NODE_ETIME'] = 12
cmdID['CMD_REQ_NODE_ETIME'] = 13
cmdID['CMD_RTN_NODE_ETIME'] = 14
cmdID['CMD_SET_SLEEP'] = 15
cmdID['CMD_REQ_PRESSURE'] = 16
cmdID['CMD_RTN_PRESSURE'] = 17
cmdID['CMD_SET_RFID'] = 18
cmdID['CMD_REQ_NODE_RSSI'] = 19
cmdID['CMD_RTN_NODE_RSSI'] = 20
cmdID['CMD_ACK'] = 21
cmdID['CMD_SET_HUB_ETIME'] = 22
cmdID['CMD_SET_CMDLIST'] = 23   # length is variable
cmdID['CMD_ENDRESPONSE'] = 24
cmdID['CMD_REQ_HUB_RSSI'] = 25
cmdID['CMD_RTN_HUB_RSSI'] = 26
cmdID['CMD_REQ_NODE_SYS'] = 27
cmdID['CMD_RTN_NODE_SYS'] = 28
cmdID['CMD_REQ_HUB_SYS'] = 29
cmdID['CMD_RTN_HUB_SYS'] = 30
cmdID['CMD_CLR_NODE_SYS'] = 31
cmdID['CMD_CLR_HUB_SYS'] = 32
cmdID['CMD_SET_WAKEUP'] = 33
cmdID['CMD_REQ_CLR_RAIN'] = 34
cmdID['CMD_SET_AUTO_CMDLIST'] = 35  # length is variable
cmdID['CMD_REQ_IHT'] = 36
cmdID['CMD_RTN_IHT'] = 37


cmdName[0] = 'CMD_NULL'
cmdName[1] = 'CMD_NODE_READY'
cmdName[2] = 'CMD_REQ_HT'
cmdName[3] = 'CMD_RTN_HT'
cmdName[4] = 'CMD_REQ_WIND'
cmdName[5] = 'CMD_RTN_WIND'
cmdName[6] = 'CMD_REQ_RAIN'
cmdName[7] = 'CMD_RTN_RAIN'
cmdName[8] = 'CMD_REQ_POWER'
cmdName[9] = 'CMD_RTN_POWER'
cmdName[10] = 'CMD_REQ_HTP'
cmdName[11] = 'CMD_RTN_HTP'
cmdName[12] = 'CMD_SET_NODE_ETIME'
cmdName[13] = 'CMD_REQ_NODE_ETIME'
cmdName[14] = 'CMD_RTN_NODE_ETIME'
cmdName[15] = 'CMD_SET_SLEEP'
cmdName[16] = 'CMD_REQ_PRESSURE'
cmdName[17] = 'CMD_RTN_PRESSURE'
cmdName[18] = 'CMD_SET_RFID'
cmdName[19] = 'CMD_REQ_NODE_RSSI'
cmdName[20] = 'CMD_RTN_NODE_RSSI'
cmdName[21] = 'CMD_ACK'
cmdName[22] = 'CMD_SET_HUB_ETIME'
cmdName[23] = 'CMD_SET_CMDLIST'   # length is variable
cmdName[24] = 'CMD_ENDRESPONSE'
cmdName[25] = 'CMD_REQ_HUB_RSSI'
cmdName[26] = 'CMD_RTN_HUB_RSSI'
cmdName[27] = 'CMD_REQ_NODE_SYS'
cmdName[28] = 'CMD_RTN_NODE_SYS'
cmdName[29] = 'CMD_REQ_HUB_SYS'
cmdName[30] = 'CMD_RTN_HUB_SYS'
cmdName[31] = 'CMD_CLR_NODE_SYS'
cmdName[32] = 'CMD_CLR_HUB_SYS'
cmdName[33] = 'CMD_SET_WAKEUP'
cmdName[34] = 'CMD_REQ_CLR_RAIN'
cmdName[35] = 'CMD_SET_AUTO_CMDLIST'  # length is variable
cmdName[36] = 'CMD_REQ_IHT'
cmdName[37] = 'CMD_RTN_IHT'


cmdFormat[0] = '=3B'  # 'CMD_NULL'
cmdFormat[1] = '=5B4H3L2H'  # 'CMD_NODE_READY'
cmdFormat[2] = '=3B'  # 'CMD_REQ_HT'
cmdFormat[3] = '=3BHHL'  # 'CMD_RTN_HT'
cmdFormat[4] = '=3B'  # 'CMD_REQ_WIND'
cmdFormat[5] = '=3B4H3L2H'  # 'CMD_RTN_WIND'
cmdFormat[6] = '=4B'  # 'CMD_REQ_RAIN'
cmdFormat[7] = '=4BL'  # 'CMD_RTN_RAIN'
cmdFormat[8] = '=3B'  # 'CMD_REQ_POWER'
cmdFormat[9] = '=3B3HL'  # 'CMD_RTN_POWER'
cmdFormat[10] = '=3B'  # 'CMD_REQ_HTP'
cmdFormat[11] = '=3BHHLLL'  # 'CMD_RTN_HTP'
cmdFormat[12] = '=3BL'  # 'CMD_SET_NODE_ETIME'
cmdFormat[13] = '=3B'  # 'CMD_REQ_NODE_ETIME'
cmdFormat[14] = '=3BL'  # 'CMD_RTN_NODE_ETIME'
cmdFormat[15] = '=3B'  # 'CMD_SET_SLEEP'
cmdFormat[16] = '=3B'  # 'CMD_REQ_PRESSURE'
cmdFormat[17] = '=3BL'  # 'CMD_RTN_PRESSURE'
cmdFormat[18] = '=5B'  # 'CMD_SET_RFID'
cmdFormat[19] = '=3B'  # 'CMD_REQ_NODE_RSSI'
cmdFormat[20] = '=3BH'  # 'CMD_RTN_NODE_RSSI'
cmdFormat[21] = '=3B'  # 'CMD_ACK'
cmdFormat[22] = '=3BL'  # 'CMD_SET_HUB_ETIME'
cmdFormat[23] = ''  # 'CMD_SET_CMDLIST'   # length is variable
cmdFormat[24] = '=3B'  # 'CMD_ENDRESPONSE'
cmdFormat[25] = '=3B'  # 'CMD_REQ_HUB_RSSI'
cmdFormat[26] = '=3BH'  # 'CMD_RTN_HUB_RSSI'
cmdFormat[27] = '=3B'  # 'CMD_REQ_NODE_SYS'
cmdFormat[28] = '=3BHL6H'  # 'CMD_RTN_NODE_SYS'
cmdFormat[29] = '=3B'  # 'CMD_REQ_HUB_SYS'
cmdFormat[30] = '=3BHL6H'  # 'CMD_RTN_HUB_SYS'
cmdFormat[31] = '=3B'  # 'CMD_CLR_NODE_SYS'
cmdFormat[32] = '=3B'  # 'CMD_CLR_HUB_SYS'
cmdFormat[33] = '=4B'  # 'CMD_SET_WAKEUP'
cmdFormat[34] = '=4B'  # 'CMD_REQ_CLR_RAIN'
cmdFormat[35] = ''  # 'CMD_SET_AUTO_CMDLIST'  # length is variable
cmdFormat[36] = '=3B'  # 'CMD_REQ_IHT'
cmdFormat[37] = '=3BHHL'  # 'CMD_RTN_IHT'


def logmsg(level, msg):
    #syslog.syslog(level, 'gws: %s' % msg)
    pass


def logdbg(msg):
    #logmsg(syslog.LOG_DEBUG, msg)
    pass


def loginf(msg):
    #logmsg(syslog.LOG_INFO, msg)
    pass


def logerr(msg):
    #logmsg(syslog.LOG_ERR, msg)
    pass


def local_loginf(msg):
    logging.info(msg)


def getPacket(ser):
    length = uart.receive(ser, 1)
    result = length
    result += uart.receive(ser, ord(length))
    # print "in getPacket - result = ", result
    return result

# Routine to get Humidity, Temperature


def getHT(pkt, command, data):
    h = pkt[3] * 125.0 / 65536.0 - 6.0
    t = (pkt[4] * 175.72 / 65536 - 46.85) * 1.8 + 32.0
    if command == cmdID['CMD_RTN_HT']:
        data['out_Temperature'] = t
        data['out_Humidity'] = h
        local_loginf('outdoor humidity = %f' % h)
        local_loginf('outdoor temperature = %f degF' % t)
    else:
        data['in_Temperature'] = t
        data['in_Humidity'] = h
        local_loginf('indoor humidity = %f' % h)
        local_loginf('indoor temperature = %f degF' % t)
    local_loginf('temperature/humidity received time = %s' %
                 str(time.asctime(time.localtime(pkt[5]))))

# Routine to get Humidity, Temperature and Pressure


def getHTP(pkt, data):
    h = pkt[3] * 125.0 / 65536.0 - 6.0
    t = (pkt[4] * 175.72 / 65536 - 46.85) * 1.8 + 32.0
    p = pkt[6] * 0.000295333727
    data['out_Temperature'] = t
    data['out_Humidity'] = h
    data['pressure'] = p
    local_loginf('outdoor humidity = %f' % h)
    local_loginf('outdoor temperature = %f degF' % t)
    local_loginf('pressure = %f inHg' % p)
    local_loginf('temperature/humidity received time = %s' %
                 str(time.asctime(time.localtime(pkt[5]))))
    local_loginf('pressure received time = %s' %
                 str(time.asctime(time.localtime(pkt[7]))))

# Routine to get pressure


def getPressure(pkt, data):
    data['pressure'] = pkt[3] * 0.000295333727
    local_loginf('pressure = %f inHg' % (pkt[3] * 0.000295333727))
    local_loginf('pressure received time = %s' %
                 str(time.asctime(time.localtime(pkt[4]))))

# Routine to get node stats


def getSysState(pkt, command):
    etime = (int(time.time()))
    if command == cmdID['CMD_RTN_NODE_SYS']:
        local_loginf('For Node')
    elif command == cmdID['CMD_RTN_HUB_SYS']:
        local_loginf('For Hub')
    local_loginf('\ttime out count = %d start time = %s' %
                 (pkt[3], str(time.asctime(time.localtime(etime - pkt[4])))))
    local_loginf('\tpktRX count = %d pktTX count = %d' % (pkt[5], pkt[6]))
    local_loginf('\tcrc error count = %d  length error count = %d' %
                 (pkt[7], pkt[8]))
    local_loginf('\tfifo error count = %d number of retries = %d',
                 (pkt[9], pkt[10]))
    local_loginf('\tup time = %f minutes,  %f hours , %f days' %
                 (pkt[4] / 60.0, (pkt[4] / 60.0) / 60.0, ((pkt[4] / 60.0) / 60.0) / 24.0))

# Routine to get response to QCMD_POWER


def getPower(pkt, data):
    battery = (pkt[3] / 4096.0) * 1.2 * (4.57)
    superCap = (pkt[4] / 4096.0) * 1.2 * (4.57)
    vbatok = (pkt[5] / 4096.0) * 1.2 * (4.57)
    if vbatok > 0.5:
        data['supercap'] = superCap
        local_loginf('Using solar: superCap voltage = %f volts' % superCap)
    else:
        data['battery'] = battery
        local_loginf(
            'Using LiIon battery: battery voltage = %f volts' % battery)
    local_loginf('power received time = %s' %
                 str(time.asctime(time.localtime(pkt[6]))))


# Routine to get response to CMD_WIND


def getWind(pkt, command, data):
    windSpeedOffset = 0.35  # meters/second
    windSpeedGain = 0.758  # meters/second/Hertz
    windSpeedSampleRate = 60.0  # 60 second wind speed sample rate
    gustSpeedSampleRate = 5.0  # 5 second wind speed sample rate
    if command == cmdID['CMD_RTN_WIND']:
        offset = 0
    elif command == cmdID['CMD_NODE_READY']:
        offset = 2
    count = pkt[3 + offset] * 1.0
    speed = (windSpeedOffset + windSpeedGain *
             (count / windSpeedSampleRate)) * 2.23693629
    if speed < 1.0:
        speed = 0.0
    data['windSpeed'] = speed
    local_loginf('Wind Speed = %f mph, Count = %d' % (speed, count))
    count = pkt[4 + offset] * 1.0
    speed = (windSpeedOffset + windSpeedGain *
             (count / gustSpeedSampleRate)) * 2.23693629
    if speed < 1.0:
        speed = 0.0
    data['windGust'] = speed
    local_loginf('Gust Speed = %f mph, Count = %d' % (speed, count))
    dirCodeRatio = ((pkt[5 + offset] * 1.0) - 0.5) / \
        ((pkt[10 + offset] * 1.0) - 0.5)
    dirDegrees = 4.0 + (dirCodeRatio - 1.0 / 102.0) * (359.04)
    gustDirCodeRatio = ((pkt[6 + offset] * 1.0) - 0.5) / \
        ((pkt[11 + offset] * 1.0) - 0.5)
    gustDirDegrees = 4.0 + (gustDirCodeRatio - 1.0 / 102.0) * (359.04)
    data['windDirection'] = dirDegrees
    data['gustDirection'] = gustDirDegrees
    local_loginf('Wind Direction = %f degrees' % dirDegrees)
    local_loginf('Gust Direction = %f degrees' % gustDirDegrees)
    local_loginf('Wind Time = %s' %
                 str(time.asctime(time.localtime(pkt[7 + offset]))))
    local_loginf('Gust Time = %s' %
                 str(time.asctime(time.localtime(pkt[8 + offset]))))
    local_loginf('Direction Time = %s' %
                 str(time.asctime(time.localtime(pkt[9 + offset]))))


# Routine to get response to QCMD_RAIN


def getRain(pkt, data):
    data['rain'] = pkt[3]
    local_loginf('Rain Count = %d' % pkt[3])
    local_loginf('Rain Time = %s' % str(time.asctime(time.localtime(pkt[4]))))


# Routine to set epoch time on hub and node
def set_time(ser):
    etime = int(time.time())
    b1 = etime & 255
    b2 = (etime >> 8) & 255
    b3 = (etime >> 16) & 255
    b4 = (etime >> 24) & 255
    c = [6, NODE_ID, cmdID['CMD_SET_HUB_ETIME'], b1, b2, b3, b4]
    uart.send(ser, c)
    # now send command to update node time
    sendCmdList(ser, [cmdID['CMD_SET_NODE_ETIME']], cmdID['CMD_SET_CMDLIST'])

# Routine to send list of commands to node


def sendCmdList(ser, cmdList, command):
    length = len(cmdList) + 2
    c = [length, NODE_ID, command]
    list.extend(c, cmdList)
    uart.send(ser, c)
    # print "cmdList sent ..."

# Routine to build packet for hub rssi


def requestHubRSSI(ser):
    length = 2
    c = [length, NODE_ID, cmdID['CMD_REQ_HUB_RSSI']]
    uart.send(ser, c)

# routine to clear hub system data


def requestClearHubSys(ser):
    length = 2
    c = [length, NODE_ID, cmdID['CMD_CLR_HUB_SYS']]
    uart.send(ser, c)

# Routine to build packet for hub system state


def requestHubSys(ser):
    length = 2
    c = [length, NODE_ID, cmdID['CMD_REQ_HUB_SYS']]
    uart.send(ser, c)

# Routine to build packet for hub humidity/temperature


def requestIHT(ser):
    length = 2
    c = [length, NODE_ID, cmdID['CMD_REQ_IHT']]
    uart.send(ser, c)


# Calculate the time difference (offset) between node and actual time
def setNodeETimeOffset(pkt):
    local_loginf('Node ETime = %s' % str(time.asctime(time.localtime(pkt[3]))))
    nodeTimeOffset = int(time.time()) - pkt[3]  # current time minus
    local_loginf('Node Time Offset = %d' % nodeTimeOffset)


# Routine to set RF addresses/IDs


def setRFID(ser):
    c = [4, NODE_ID, cmdID['CMD_SET_RFID'], NODE_ID, HUB_ID]
    uart.send(ser, c)

# Routine to get rssi value from node or hub


def getRSSI(pkt, command):
    val = -((~pkt[3] & 0xFFFF) + 1)  # convert two's complement number
    if command == cmdID['CMD_RTN_NODE_RSSI']:
        local_loginf('node received rssi = %d dBm' % val)
    elif command == cmdID['CMD_RTN_HUB_RSSI']:
        local_loginf('hub received rssi = %d dBm' % val)


def genLoopPackets():
    while True:
        data = {'dateTime': int(time.time() + 0.5),
                'usUnits': 'weewx.US'}   # for now, just have units value as a string
        command = cmdID['CMD_NULL']
        while command != cmdID['CMD_ENDRESPONSE']:
            packet = getPacket(ser)
            command = ord(packet[2])
            pkt = struct.unpack_from(cmdFormat[command], packet)
            if command == cmdID['CMD_RTN_HT'] or command == cmdID['CMD_RTN_IHT']:
                getHT(pkt, command, data)
            elif (command == cmdID['CMD_NODE_READY']) or (command == cmdID['CMD_RTN_WIND']):
                getWind(pkt, command, data)
            elif command == cmdID['CMD_RTN_HTP']:
                getHTP(pkt, data)
            elif command == cmdID['CMD_RTN_POWER']:
                getPower(pkt, data)
            elif command == cmdID['CMD_RTN_RAIN']:
                getRain(pkt, data)
            elif (command == cmdID['CMD_RTN_NODE_RSSI']) or (command == cmdID['CMD_RTN_HUB_RSSI']):
                getRSSI(pkt, command)
            elif command == cmdID['CMD_RTN_PRESSURE']:
                getPressure(pkt, data)
            elif (command == cmdID['CMD_RTN_NODE_SYS']) or (command == cmdID['CMD_RTN_HUB_SYS']):
                getSysState(pkt, command)
            elif command == cmdID['CMD_RTN_NODE_ETIME']:
                setNodeETimeOffset(pkt)
        yield data


if __name__ == '__main__':

    logging.basicConfig(filename='gws.log', level=logging.DEBUG)
    # logging.disable(logging.INFO)  # disable logging
    logging.disable(logging.NOTSET)  # enables logging

    try:
        ser = uart.openUART()
        time.sleep(0.1)
        set_time(ser)  # initialize time on hub and node

        # define command lists
        initCommandList = [cmdID['CMD_SET_NODE_ETIME']]
        nodeStatCommandList = [
            cmdID['CMD_REQ_NODE_RSSI'],  cmdID['CMD_REQ_NODE_SYS']]
        autoCommandList = [cmdID['CMD_REQ_HTP'], cmdID['CMD_REQ_RAIN'],
                           cmdID['CMD_REQ_POWER'], cmdID['CMD_REQ_NODE_ETIME']]

        # send command lists
        # send list of commands to hub
        # sendCmdList(ser, initCommandList, cmd['CMD_SET_CMDLIST'])
        # send list of commands to hub
        sendCmdList(ser, autoCommandList, cmdID['CMD_SET_AUTO_CMDLIST'])

        while True:
            for data in genLoopPackets():
                for key in data:
                    print key, ' : ', data[key]
                requestIHT(ser)   # get internal humidity, temperature
    except KeyboardInterrupt:
        print '\nkeyboard interrupt'
        uart.close(ser)
        logging.shutdown()
        sys.exit(0)
