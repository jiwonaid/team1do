# test BLE Scanning software
# jcs 6/8/2014

import blescan
import sys

import bluetooth._bluetooth as bluez

import pygame
import time

pygame.mixer.init()

sound = pygame.mixer.Sound("line.wav")

dev_id = 0


def calculateD(txpower, rssi) :
    if(rssi == 0) :
        return -1.0
    ratio = rssi*1.0/txpower
    if ratio < 1.0 :
        return pow(ratio, 10)
    else :
        distance = 0.89976*pow(ratio, 7.7095) + 0.111
        return distance

try:
	sock = bluez.hci_open_dev(dev_id)
	print "ble thread started"

except:
	print "error accessing bluetooth device..."
    	sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

while True:
	returnedList = blescan.parse_events(sock, 10)
	print "----------"
	for beacon in returnedList:
                        beaconT= beacon.split(',')
                        txPower = beaconT[4]
                        txPowerint = int(txPower)
                        rssi=beaconT[5]
                        rssiint = int(rssi)
                        if (beaconT[0].lower()) == ("e7:27:42:c0:de:1b".lower()) :
                                distance = calculateD(txPowerint,rssiint)
                                if distance < 1000 :
                                        print "Near"
                                        print beacon
                                        sound.play()
                                        time.sleep(5.0)
