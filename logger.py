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


"""




	clc=ReceiveData(44,2)
--- signed conversion
	if clc > 32767 then
	clc = 65535 - clc
	clc = - clc
	end
	clc=clc * 0.05

	kth2o=ReceiveData(102,1)
	kth2o=kth2o/64*100
	ktair=ReceiveData(103,1)
	ktair=ktair/128*100


"Accel Enrichment PW","ms","AEID","ae","0,20","2","0","0,20,20,20,20,20","ae=ReceiveData(12,2)
"Actual Pedal Position 1","%","ACTPPS1ID","apps1","0,100","2","0","0,100,100,100,100,100","apps1 = ReceiveData(84,1)
"Actual Pedal Position 2","%","ACTPPS2ID","apps2","0,100","2","0","0,100,100,100,100,100","apps2 = ReceiveData(85,1)
"Actual Pedal Position","%","ACTPPSID","apps","0,100","2","0","0,100,100,100,100,100","apps = ReceiveData(83,1)
"Actual Throttle Position 1","%","ACTTPS1ID","atps1","0,100","2","0","0,100,100,100,100,100","atps1 = ReceiveData(86,1)
"Actual Throttle Position 2","%","ACTTPS2ID","atps2","0,100","2","0","0,100,100,100,100,100","atps2 = ReceiveData(87,1)
"Actual Throttle Position","%","ACTTPSID","atps","0,100","2","0","0,100,100,100,100,100","atps = ReceiveData(30,2)
"Actual Wheel Slip","%","SLIPID","slip","0,100","1","0","0,100,100,100,100,100","slip = ReceiveData(22,1)
ae=ReceiveData(12,2)
"Air Temp Correction","%","KTAIRID","ktair","100,250","0","0","100,250,250,250,250,250","ktair=ReceiveData(103,1)
apps1 = ReceiveData(84,1)
apps2 = ReceiveData(85,1)
apps = ReceiveData(83,1)
atps1 = ReceiveData(86,1)
atps2 = ReceiveData(87,1)
atps = ReceiveData(30,2)
"Barometric Pressure","mBar","BAROID","baro","600,1100","0","0","700,1050,1050,1100,600,700","baro=ReceiveData(56,2)
baro=ReceiveData(56,2)
baseboostdc=ReceiveData(49,1)
"Base Boost Duty Cycle","%","BASEBOOSTDCID","baseboostdc","0,100","1","0","0,95,95,100,100,100","baseboostdc=ReceiveData(49,1)
"Base Idle Duty Cycle","%","BASEIDLEDCID","valbaseidle","0,100","1","0","0,95,95,100,100,100","valbaseidle=ReceiveData(18,2)
"Base Injection PW","ms","INJPWID","valbaseinjpw","0,20","2","0","0,16,16,18,18,20","valbaseinjpw=ReceiveData(32,2)
basesa=ReceiveData(36,2)

Binary file gaugecatalog.csv matches
boostdc=ReceiveData(50,2)
cam1angle=ReceiveData(24,2)
cam2angle=ReceiveData(26,2)
clc1=ReceiveData(44,2)
clc=ReceiveData(44,2)
"Closed Loop Control 1","%","CLC1ID","clc1","-20,20","2","0","-18,18,18,20,-18,-20","clc1=ReceiveData(44,2)
"Closed Loop Control 2","%","CLC2ID","clc2","-20,20","2","0","-18,18,18,20,-18,-20","clc2=ReceiveData(46,2)
"Coolant Temp Correction","%","KTH2OID","kth2o","100,250","0","0","100,250,250,250,250,250","kth2o=ReceiveData(102,1)
"Crank Counter","","CNTCRKID","crkcnt","0,1023","0","0","0,1023,1023,1023,1023,1023","crkcnt=ReceiveData(104,2)
ecamtarget = ReceiveData(29,1)
"Engine Speed","rpm","RPMID","rpm","0,9000","0","0","0,7000,7000,8000,8000,9000","rpm = ReceiveData(0,2)
"Final Boost Duty Cycle","%","BOOSTDCID","boostdc","0,100","1","0","0,95,95,100,100,100","boostdc=ReceiveData(50,2)
"Final Idle Duty Cycle","%","IDLEOUTID","validleout","0,100","1","0","0,95,95,100,100,100","validleout=ReceiveData(20,2)
"Final Injection PW 1","ms","INJPW1ID","injpw1","0,20","2","0","0,16,16,18,18,20","injpw1=ReceiveData(34,2)
"Final Injection PW 2","ms","INJPWBID","injpwb","0,20","2","0","0,16,16,18,18,20","injpwb=ReceiveData(42,2)
fuelp = ReceiveData(54,2)
"Fuel Pressure","Bar","FUELPID","fuelp","0,250","1","0","100,5000,50,100,40,50","fuelp = ReceiveData(54,2)
"Gear","","GEARID","valgear","0,6","0","0","0,6,6,6,6,6","valgear = ReceiveData(123,1)
icamtarget = ReceiveData(28,1)
"Idle Learn","%","IDLELEARNID","valil","-30,30","2","2","-20,20,20,30,-20,-30","valil=ReceiveData(6,2)
injpw=ReceiveData(34,2)
kmhlf = ReceiveData(116,2)
kmhlr = ReceiveData(112,2)
kmh=ReceiveData(16,2)
kmhrf = ReceiveData(118,2)
kmhrr = ReceiveData(114,2)
ktair=ReceiveData(103,1)
kth2o=ReceiveData(102,1)


"Left Front Wheel Speed","km/h","KMHLFID","kmhlf","0,160","1","0","0,160,160,160,160,160","kmhlf = ReceiveData(116,2)
"Left Rear Wheel Speed","km/h","KMHLRID","kmhlr","0,160","1","0","0,160,160,160,160,160","kmhlr = ReceiveData(112,2)
"Manifold Pressure","mBar","MAPID","map","0,3200","0","0","0,2800,2800,3000,3000,3200","map=ReceiveData(4,2)
"MAP Correction","%","KFUELMAPID","valkfuelmap","100,250","0","0","100,250,250,250,250,250","valkfuelmap=ReceiveData(3,1)
map =ReceiveData(4,2)
map=ReceiveData(4,2)
oilp = ReceiveData(52,2)
"Oil Pressure","kPa","OILPID","oilp","0,1000","0","0","100,8000,50,100,40,50","oilp = ReceiveData(52,2)
"Raw Pedal Position 1","V","RAWPPS1ID","rpps1","0,5","2","2","0,5,5,5,5,5","rpps1 = ReceiveData(74,2)
"Raw Pedal Position 2","V","RAWPPS2ID","rpps2","0,5","2","2","0,5,5,5,5,5","rpps2 = ReceiveData(76,2)
"Raw Throttle Position 1","V","RAWTPS1ID","rtps1","0,5","2","2","0,5,5,5,5,5","rtps1 = ReceiveData(72,2)
"Raw Throttle Position 2","V","RAWTPS2ID","rtps2","0,5","2","2","0,5,5,5,5,5","rtps2 = ReceiveData(80,2)
"Right Front Wheel Speed","km/h","KMHRFID","kmhrf","0,160","1","0","0,160,160,160,160,160","kmhrf = ReceiveData(118,2)
"Right Rear Wheel Speed","km/h","KMHRRID","kmhrr","0,160","1","0","0,160,160,160,160,160","kmhrr = ReceiveData(114,2)
rpm = ReceiveData(0,2)
rpm=ReceiveData(0,2)
rpps1 = ReceiveData(74,2)
rpps2 = ReceiveData(76,2)
rtps1 = ReceiveData(72,2)
rtps2 = ReceiveData(80,2)
slip = ReceiveData(22,1)
tair=ReceiveData(91,1)
tair=ReceiveData(91,1)
targetboost=ReceiveData(62,2)
"Target Idle Speed","rpm","IDLERPMID","validlerpm","400,2000","0","0","400,2000,2000,2000,2000,2000","validlerpm=ReceiveData(110,2)

"Target Manifold Pressure","mBar","TARGETBOOSTID","targetboost","0,3200","0","0","0,2800,2800,3000,3000,3200","targetboost=ReceiveData(62,2)
"Target Throttle Position","%","TGTTPSID","ttps","0,100","2","0","0,100,100,100,100,100","ttps = ReceiveData(78,2)
"Target Wheel Slip","%","TSLIPID","tslip","0,100","1","0","0,100,100,100,100,100","tslip = ReceiveData(23,1)
tcool=ReceiveData(88,1)
"Throttle Position","%","TPSID","tps","0,100","1","0","0,90,90,95,95,100","tps = ReceiveData(2,1)

"TPS/PPS Fault Code","","TPSFAULTID","tpsfault","0,255","0","0","0,0,0,0,0,255","tpsfault = ReceiveData(82,1)
tps = ReceiveData(2,1)
tps=ReceiveData(2,1)
tslip = ReceiveData(23,1)
ttps = ReceiveData(78,2)
valae=ReceiveData(12,2)
valbaro=ReceiveData(56,2)
valbaseboostdc=ReceiveData(49,1)
valbaseidle=ReceiveData(18,2)
valbaseinjpw=ReceiveData(32,2)
valbasesa=ReceiveData(36,2)

valboostdc=ReceiveData(50,2)
valcamcount =ReceiveData(69,1)
valclc2=ReceiveData(46,2)
valclc=ReceiveData(44,2)
valclc=ReceiveData(46,2)
valclc=ReceiveData(46,2)
valcrkcnt=ReceiveData(104,2)

valdwell=ReceiveData(70,2)
valfli = ReceiveData(123,1)
valfl=ReceiveData(120,2)
valfl=ReceiveData(120,2)
valfl = ReceiveData(122,1)
valfuelp = ReceiveData(54,2)
valfuelp=ReceiveData(54,2)
valgearratio = ReceiveData(124,2)
--	valgearratio = ReceiveData(124,2)
valgear = ReceiveData(123,1)
--	valgear = ReceiveData(123,1)
valgear = ReceiveData(48,1)
valhperc=ReceiveData(11,1)
validleout=ReceiveData(20,2)
validlerpm=ReceiveData(110,2)
valinjpw=ReceiveData(34,2)
valinjpw=ReceiveData(42,2)
valinjpw=ReceiveData(42,2)
valkfuelbaro=ReceiveData(106,1)
valkfuelcrk=ReceiveData(90,1)
valkfuelmap=ReceiveData(3,1)
valkfuelp=ReceiveData(107,1)
valkmhlf = ReceiveData(116,2)
valkmhlr = ReceiveData(112,2)
valkmh=ReceiveData(16,2)
valkmhrf = ReceiveData(118,2)
valkmhrr = ReceiveData(114,2)
valktair=ReceiveData(103,1)
valktair=ReceiveData(103,1)
--	valktair=ReceiveData(103,1)
valkth2o=ReceiveData(102,1)
valkth2o=ReceiveData(102,1)
--	valkth2o=ReceiveData(102,1)


valmap =ReceiveData(4,2)
valmap=ReceiveData(4,2)
valoilp = ReceiveData(52,2)
valoilp=ReceiveData(52,2)
valosatair=ReceiveData(108,2)
valphase=ReceiveData(68,1)
valpps = ReceiveData(83,1)
val = ReceiveData(0,2)
val = ReceiveData(0,2)
val = ReceiveData(126,1)
val = ReceiveData(127,1)
val=ReceiveData(24,2)
--	val=ReceiveData(24,2)
val=ReceiveData(26,2)
val=ReceiveData(28,1)
val=ReceiveData(29,1)
--	val=ReceiveData(6,2)
val = ReceiveData(83,1)
valrpm=ReceiveData(0,2)
--	valrpm=ReceiveData(0,2)

valtairI=ReceiveData(98,2)
valtair=ReceiveData(91,1)
--	valtair=ReceiveData(91,1)
valtargetboost=ReceiveData(62,2)
valtarget=ReceiveData(41,1)
valtarget=ReceiveData(41,1)
valtcool=ReceiveData(88,1)
valth2oI=ReceiveData(92,2)
valtoilI=ReceiveData(94,2)
valtoil=ReceiveData(89,1)
valtpsi=ReceiveData(72,2)
valtpsi=ReceiveData(72,2)
valtpsi=ReceiveData(72,2)
valtps=ReceiveData(2,1)
valtps=ReceiveData(83,1)
valtps=ReceiveData(86,1)

"Vehicle Speed","kmh","KMHID","kmh","0,200","0","0","0,180,180,200,180,200","kmh=ReceiveData(16,2)


"""
if readline() == b'www.specialist-components.co.uk':
    print("1) Got SC reply")
    pass
else:
    print("didn't get sc.co.uk reply, not the right SC USB connector")
    sys.exit(1)

# get the above just from the USB being plugged in (ecu off)
# following only works with ECU on

ser.write(b's005200000000\r')

if readline() == b'01':
    print("2) got ECU reply")
    pass
else:
    print("didn't get 01 reply, something wrong, make sure ignition is on at least")
    sys.exit(1)

ser.write(b's00534001000020\r')
readline()
# ecu replies:
# [b'5', b'3', b'5', b'2', b'6', b'E', b'6', b'9', b'2', b'0', b'4', b'3', b'6', b'F', b'6', b'F', b'7', b'0', b'6', b'5', b'7', b'2', b'2', b'0', b'5', b'3', b'5', b'0', b'6', b'9', b'2', b'0', b'4', b'2', b'6', b'1', b'7', b'3', b'6', b'5', b'2', b'0', b'4', b'D', b'6', b'1', b'7', b'0', b'0', b'0', b'0', b'0', b'0', b'0', b'0', b'0', b'0', b'0', b'0', b'0', b'0', b'0', b'0', b'0']

ser.write(b's0053ffffffff\r')
readline()
# [b'0', b'0', b'0', b'E', b'3', b'A', b'0', b'8']

ser.write(b's0053000e3b5206\r')
readline()
# [b'4', b'0', b'0', b'0', b'4', b'7', b'B', b'0', b'2', b'0', b'0', b'0']

ser.write(b's0053400047b020\r')
readline()
# [b'4', b'4', b'6', b'5', b'6', b'C', b'7', b'4', b'6', b'1', b'2', b'0', b'3', b'4', b'3', b'0', b'3', b'0', b'2', b'0', b'7', b'6', b'3', b'0', b'3', b'0', b'3', b'3', b'2', b'0', b'4', b'6', b'6', b'5', b'6', b'2', b'2', b'0', b'2', b'0', b'3', b'7', b'2', b'0', b'3', b'2', b'3', b'0', b'3', b'2', b'3', b'0', b'0', b'0', b'0', b'0', b'0', b'0', b'0', b'0', b'0', b'0', b'0', b'0']

ser.write(b's005340011e6a10\r')
readline()
# [b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F', b'F']

ser.write(b's005140010020\r')
readline()
# < 0017

ser.write(b's005140010022\r')
readline()
# < 0000

ser.write(b's005140010026\r')
readline()
# <0010

ser.write(b's005140010024\r')
readline()
# ea60

ser.write(b's005140010028\r')
readline()
# 0ca2

ser.write(b's00514001002a\r')
readline()
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
