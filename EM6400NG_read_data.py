import os
import struct
from os import path
import time
import pymodbus
import serial
from pymodbus.pdu import ModbusRequest
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.transaction import ModbusRtuFramer
from pymodbus.transaction import ModbusRtuFramer


def write_csv_header(csv_file, header):
    with open(csv_file, 'a') as f:
        f.write(header)


def convert_to_str(s):
    return str(struct.unpack("<f", struct.pack("<I", s))[0])

def write_csv(csv_path, data):
    with open(csv_path, 'a') as f:
         f.write(data)

DATA_PATH = r"C:\Users\Sajal Sirohi.DESKTOP-RTVGPUA\Desktop\meter_NG6400"

register_record_array = [2999, 3009, 3035, 3053, 3109, 3191]
block_size_record_arr = [6, 2, 2, 24, 2, 2]
no_of_meters = 4
answer = ""
meter_id = 1
l = 1
params_recorded =  "Current Phase 1 (A1),Current Phase 2 (A2), Current Phase 3 (A3), Current Average(A),Avg. Line to Neutral Voltage(VLN),Active Power Phase 1 (W1), Active Power Phase 2 (W2), Active Power Phase 3 (W3),Total Active Power(W),Reactive Power Phase 1 (VAR1), Reactive Power Phase 2 (VAR2), Reactive Power Phase 3 (VAR3), Total Reactive Power(VAR), Apparent Power Phase 1 (VA1), Apparent Power Phase 2 (VA2),Apparent Power Phase 3 (VA3), Total Apparent Power(VA), Frquency (F), Total Power Factor(PF)"


try:
    client = ModbusClient(method="rtu", port="COM5", stopbits=1, bytesize=8, parity='E', baudrate=19200)
    connection = client.connect()
except:
    print("Unable to connect to the Com Port, Please try Again \n")

while (l <= no_of_meters):
    csv_file_path = os.path.join(DATA_PATH, "meter_id_" + str(l) + ".csv")
    if path.isfile(csv_file_path):
        break
    else:
        write_csv_header(csv_file_path, "Timestamp," +
                         params_recorded + "\n")
    l += 1
data = ""
while True:
    try:
        if meter_id > no_of_meters:
            meter_id = 1
        print("Reading Data from Meter ID : " + str(meter_id))
        answer = []
        data= ""
        for (base_reg, block_size) in zip(register_record_array, block_size_record_arr):
            q = divmod(block_size, 12)
            i = 1
            while i <= q[0]:
                result = client.read_holding_registers(base_reg, 12, unit=meter_id)
                answer += result.registers
                base_reg += 12
                i += 1
            if q[0] == 0:
                result = client.read_holding_registers(base_reg, q[1], unit = meter_id)
        for i in range(len(answer)):
            answer[i] = str(answer[i])
        for i in range(0, len(answer), 2):
            j = int(i / 2)
            answer[j] = answer[i] + answer[i + 1]
        answer = answer[:int(len(answer) / 2)]
        for x in range(len(answer)):
            answer[x] = str(answer[x])
        for x in answer:
            data+=answer + ","
        csv_file_path = os.path.join(DATA_PATH, "meter_id_" + str(meter_id) + ".csv")
        write_csv(csv_file_path, data)
        meter_id += 1

    except:
        print("Error Reading from the Meter ID : " + str(meter_id))
        if meter_id < no_of_meters:
            meter_id += 1
        elif meter_id == no_of_meters:
            meter_id = 1
    time.sleep(1)


