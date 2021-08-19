import serial_comm
import mqtt_publisher
import sys

if __name__ == "__main__":

    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))

    if len(sys.argv) != 2:
        raise SyntaxError("Wrong amount of arguments.")

    while 1:
        print("Starting serial comm...")
        file_name = serial_comm.read_sensor()
        print("OK!")
        print("Starting to publish file:", file_name, "...")
        mqtt_publisher.publish(file_name, sys.argv[1])
        print("OK!")
