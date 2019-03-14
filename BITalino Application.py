from pyqtgraph.Qt import QtGui, QtCore
import csv
import pyqtgraph as pg
from bitalino import *
import SensorsRadioButtons as srb
import TransferFunctions as tf
import time


## Checks if the operative system is Windows or Linux, or if it is another OS
if platform.system() == 'Windows' or platform.system() == 'Linux':
    macAddress = '20:18:06:13:02:54'
else:
    # VCP=Virtual COM Port, on Mac OS it is not possible to use the MAC address get connected to the board
    macAddress = '/dev/tty.BITalino-02-54-DevB'

## Menu with radio buttons to choose sensor and sampling rate
sensor, sRate = srb.chooseSensorAndSamplingRate()

## Sets the number of samples acquired in each
## data acquisition according to the chosen sample rate
if sRate == 10:
    nSamples = 1
elif sRate == 100:
    nSamples = 10
elif sRate == 1000:
    nSamples = 100

analogChannels = [0, 1, 2, 3, 4, 5]
digitalOutput = [1, 1]
labels = ['nSeq', 'I1', 'I2', 'O1', 'O2', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6']
mytimer = 0

## Creates the window that will hold the plot
win = pg.GraphicsWindow(title="BITalino")
win.resize(1000, 600)
win.setWindowTitle('BITalino')

## Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)

## Creates the plot
plot = win.addPlot(title="BITalino Sensor plot")
plot.showGrid(x=True, y=True)
plot.setLabel('bottom', 'Time', units='s')

## Empty lists that will hold the plotted data
xaxis = []
yaxis = []

## Sets the Y-axis limits and labels depending on the connected sensor
if sensor == 'ACC':
    plot.setLimits(yMin=-4, yMax=4, xMin=0)
    plot.setLabel('left', 'ACC: g-force', units='g')
elif sensor == 'LUX':
    plot.setLabel('left', 'LUX: Luminosity', units='%')
    plot.setLimits(yMin=-1, yMax=101, xMin=0)
elif sensor == 'ECG':
    plot.setLabel('left', 'ECG:', units='mV')
    plot.setLimits(yMin=-2, yMax=2, xMin=0)
elif sensor == 'EMG':
    plot.setLabel('left', 'EMG:', units='mV')
    plot.setLimits(yMin=-2, yMax=2, xMin=0)
elif sensor == 'EDA':
    plot.setLabel('left', 'EDA:', units='')
    plot.setLimits(yMin=-1, yMax=1000, xMin=0)

plot.setRange(rect=None, xRange=None, yRange=(0, 100),
              padding=None, update=False, disableAutoRange=True)
curve = plot.plot(xaxis, yaxis, pen='y')

## Creates .csv file
dt = time.strftime("%Y-%m-%d_%H-%M-%S")
with open(dt + '_' + sensor + '.csv', mode='w') as bitalino_file:
    bitalino_writer = csv.writer(bitalino_file, delimiter='\t', quotechar='"',
                                 quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    bitalino_writer.writerow(['# Date and time: ' + dt])
    bitalino_writer.writerow(['# Device name: ' + macAddress])
    bitalino_writer.writerow(['# Sensor: ' + sensor])
    bitalino_writer.writerow(['# Analog channel: ' + 'A1'])
    bitalino_writer.writerow(['# Sampling rate (Hz): ' + str(sRate)])
    bitalino_writer.writerow(['# EndOfHeader'])
    bitalino_writer.writerow(['TIMESTAMP', 'RAW VALUE', 'REAL VALUE'])
bitalino_file.close()

def writeToCSVFile(timestamp, rawValue, realValue):
    global dt, sensor
    with open(dt + '_' + sensor + '.csv', mode='a') as bitalino_file:
        bitalino_writer = csv.writer(bitalino_file, delimiter='\t', quotechar='"',
                                     quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        bitalino_writer.writerow([timestamp, rawValue, realValue])
    bitalino_file.close()

def closeConnection(device):
    device.close()
    print('CONNECTION CLOSED')

def stopDevice(device):
    device.stop()
    print('DEVICE STOPPED')

def update():
    global curve, data, xaxis, yaxis, sensor, mytimer
    try:
        data = device.read(nSamples) ## reads samples

        for sample in data:
            rawValue = sample[5]
            yValue = tf.transferFunction(rawValue, sensor) ## data after applying transfer function
            yaxis.append(yValue)
            xaxis.append(mytimer)

            writeToCSVFile(mytimer, rawValue, yValue)
            mytimer += 1 / sRate

        curve.setData(xaxis, yaxis)
        plot.setRange(rect=None, xRange=(mytimer-10, mytimer+10),
                      padding=None, update=False, disableAutoRange=True)

        ## after some time the first values of the xaxis and yaxis
        ## lists are eliminated to prevent them from growing with no limits
        if len(xaxis) >= sRate * 30:
            del xaxis[:sRate*10]
            del yaxis[:sRate*10]

    except:
        stopDevice(device)
        closeConnection(device)
        sys.exit(0)


timer = QtCore.QTimer()
timer.timeout.connect(update)  ## the update function is called every time the timeout signal is emitted
timer.start(10)  ## emits a timeout signal every 10 mSec

if __name__ == '__main__':
    import sys
    print('CONNECTING...')
    device = BITalino(macAddress)  ## creates a new connection with the board
    print('CONNECTED')

    device.start(sRate, analogChannels)  ## starts the acquisition of data
    try:
        QtGui.QApplication.instance().exec_()

    except:
        stopDevice(device)
        closeConnection(device)
        sys.exit(0)

    finally:
        stopDevice(device)
        closeConnection(device)
        sys.exit(0)
