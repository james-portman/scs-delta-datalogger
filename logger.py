import time
import sys
import serial # pyserial
import serial.tools.list_ports

port = None

if len(sys.argv) == 2:
    print("Using COM port you provided")
    port = sys.argv[1]
else:
    print("Checking for COM ports")
    ports = serial.tools.list_ports.comports()
    if len(ports) == 0:
        print("Didn't find any COM ports to use")
        sys.exit(1)
    elif len(ports) > 1:
        print("Found more than one COM port, don't know which to use, you can specify on the command line e.g. script.py COM1")
        sys.exit(1)
    else:
        port = ports[0]
        port = port.device

ser = serial.Serial(port, 19200, timeout=0)  # open serial port
print(ser.name)         # check which port was really used
ser.write(b'\x47\x0d\x71\x0d')

def readline():
    buffer = b''
    while True:
        reply = ser.read()
        if reply == b'':
            # time.sleep(1)
            pass
        elif reply == b'\r':
            break
        else:
            # print(reply.decode())
            buffer += reply
    # print(buffer)
    return buffer

def getdata(address):
    """
    TODO: move the addresses into the IF statements? dynamic functions?
    """
    # print(address)
    ser.write(b'b'+data_addresses[address]+b'\r')
    data = readline()
    data = data.decode() # convert from bytes to string
    data = int(data, 16) # load in from a hex string

    if address == "spark":
        # signed so if spark > 32767 then spark = 65535 - spark; spark = - spark; then * 0.25
        if data > 32767:
            data = 65535 - data
            data = 0 - data
        data = data * 0.25

    elif address == "battery":
        data=round(data*18/1023, 1)

    elif address == "tps":
        data = round(data * 0.392156862745098, 1)

    elif address == "coolant":
    	data = data + 48
    	data = data * 0.625
    	data = data - 40

    elif address == "iat":
    	data = data + 48
    	data = data * 0.625
    	data = data - 40

    elif address == "lambda":
        data = round(data * 0.00784313, 1)

    elif address == "accel_enrichment":
        data *= 0.001

    elif address == "injpw":
        data *= 0.001
    elif address == "kmh":
        data /= 10
    elif address == "mph":
        data /= 10
        data *= 0.621371

    return data


# these are in hex in byte strings, the lua defs are dec
data_addresses = {
	"accel_enrichment": b'0c02',
    "baro": b'3802',
    "battery": b'4002',
    "coolant": b'5801',
    "iat": b'5b01',
    "injpw": b'2202',
    "kmh": b'1002',
    "lambda": b'2801',
    # "lambda 2?": b'0A01', # *0.00784313
    "lambda_adaptation": b'7802',
    "lambda_target": b'2901',
    "lambda_voltage": b'6402',
    "map": b'0402',
    "mph": b'1002',
    "rpm": b'0002',
    "spark": b'2602',
    "tps": b'0201',

    "_": b'0002'
}

response = readline()
if response == b'www.specialist-components.co.uk':
    print("1) Got SC reply")
    pass
else:
    print("didn't get sc.co.uk reply, not the right SC USB connector")
    print(response)
    sys.exit(1)

# get the above just from the USB being plugged in (ecu off)
# following only works with ECU on

ser.write(b's005200000000\r')
response = readline()
if response == b'01':
    print("2) got ECU reply")
    pass
else:
    print("didn't get 01 reply, something wrong, make sure ignition is on at least")
    print(response)
    sys.exit(1)

ser.write(b's00534001000020\r')
print(readline())
# ecu replies:
# [b'5', b'3', b'5', b'2', b'6', b'E', b'6', b'9', b'2', b'0', b'4', b'3', b'6', b'F', b'6', b'F', b'7', b'0', b'6', b'5', b'7', b'2', b'2', b'0', b'5', b'3', b'5', b'0', b'6', b'9', b'2', b'0', b'4', b'2', b'6', b'1', b'7', b'3', b'6', b'5', b'2', b'0', b'4', b'D', b'6', b'1', b'7', b'0', b'0', b'0', b'0', b'0', b'0', b'0', b'0', b'0', b'0', b'0', b'0', b'0', b'0', b'0', b'0', b'0']

ser.write(b's0053ffffffff\r')
print(readline())
# [b'0', b'0', b'0', b'E', b'3', b'A', b'0', b'8']

ser.write(b's0053000e3b5206\r')
print(readline())
# [b'4', b'0', b'0', b'0', b'4', b'7', b'B', b'0', b'2', b'0', b'0', b'0']

ser.write(b's0053400047b020\r')
print(readline())
# [b'4', b'4', b'6', b'5', b'6', b'C', b'7', b'4', b'6', b'1', b'2', b'0', b'3', b'4', b'3', b'0', b'3', b'0', b'2', b'0', b'7', b'6', b'3', b'0', b'3', b'0', b'3', b'3', b'2', b'0', b'4', b'6', b'6', b'5', b'6', b'2', b'2', b'0', b'2', b'0', b'3', b'7', b'2', b'0', b'3', b'2', b'3', b'0', b'3', b'2', b'3', b'0', b'0', b'0', b'0', b'0', b'0', b'0', b'0', b'0', b'0', b'0', b'0', b'0']

ser.write(b's005340011e6a10\r')
print(readline())
# [b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F']

ser.write(b's005140010020\r')
print(readline())
# < 0017

ser.write(b's005140010022\r')
print(readline())
# < 0000

ser.write(b's005140010026\r')
print(readline())
# <0010

ser.write(b's005140010024\r')
print(readline())
# ea60

ser.write(b's005140010028\r')
print(readline())
# 0ca2

ser.write(b's00514001002a\r')
print(readline())
# < 0000

# this this is the start of loop to read gauges
logfile_name = 'logs/logfile_%s.csv' % int(time.time())
print("Starting logging to %s" % logfile_name)
with open(logfile_name, 'w') as output_file:
    csv_header = "timestamp,"+','.join(data_addresses.keys())
    output_file.write(csv_header+"\n")
    loops = 0
    started = time.time()
    last_notification = time.time()
    last_notification_line_count = 0
    while True:
        line = [str(int(time.time()))] # start each line with the timestamp
        for key in data_addresses.keys():
            data = getdata(key)
            # print("%s: %s" % (key, data))
            line.append(str(data))
        output_file.write(','.join(line)+"\n")
        loops += 1
        if time.time() > last_notification + 1:
            print("Got %s total log lines, %s/second" % (loops, loops-last_notification_line_count), end="\r")
            last_notification = time.time()
            last_notification_line_count = loops

"""
# is this telling it to stop?
706 02/12/2020 15:35:04 IRP_MJ_WRITE DOWN  73 30 30 35 31 34 30 30 31 30 30 32 30 0d  s005140010020. 14 14 COM4
"""

ser.close()             # close port
