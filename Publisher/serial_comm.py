import time
import serial


def read_sensor():
    ser = serial.Serial(

        port='/dev/ttyAMA0',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )
    output_name = "reception.yml"

    while ser.inWaiting() == 0:
        pass

    size_to_read = ser.readline()
    size_as_int = int(size_to_read)

    if int(size_as_int) > 0:
        ser.write("A".encode('utf-8'))

    while ser.inWaiting() == 0:
        pass

    x = ser.read(size_as_int)
    with open(output_name, 'w+') as f:
        f.write(x.decode('utf-8'))

    return output_name


if __name__ == "__main__":
    while 1:
        read_sensor();