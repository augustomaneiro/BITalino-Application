def transferFunction(rawData, sensor):

    cmin = 379 ## minimum calibration value for accelerometer
    cmax = 696 ## maximum calibration value for accelerometer
    value = 0

    if sensor == 'ACC':
        value = ((rawData - cmin) / (cmax - cmin)) * 2 - 1
    elif sensor == 'LUX':
        value = (rawData / 2**10) * 100
    elif sensor == 'ECG':
        value = ((((rawData / 2**10) - 1/2) * 3.3) / 1100) * 1000
    elif sensor == 'EMG':
        value = ((((rawData / 2**10) - 1/2) * 3.3) / 1000) * 1000
    elif sensor == 'EDA':
        value = 1 / (1 - (rawData / 2**10))

    return value
