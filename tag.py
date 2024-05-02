import serial
import time

class Tag:
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
        # Open the serial port when Tag object is initialized

    def interpret_distance(self, dist) -> int:
        if dist == "ffffffff":
            self.throwAnchorError()
        dist = dist.lstrip("0")  # Remove leading zeros
        if not dist:  # If the string becomes empty after stripping zeros
            dist = "0"  # Set it to "0" to represent zero
        return int(dist, 16)

    def get_current_distances(self) -> dict:
        toReturn = {}
        try:
            while True:
                data = self.ser.readline().decode().strip()  
                dataList = data.split(" ")

                if len(dataList) < 9:
                    continue

                if "ffffffff" not in dataList:
                    toReturn = {
                        "0": self.interpret_distance(dataList[2]),
                        "1": self.interpret_distance(dataList[3]),
                        "2": self.interpret_distance(dataList[4]),
                        "3": self.interpret_distance(dataList[5])
                    }
                    break

        except KeyboardInterrupt:
            self.ser.close()
        except Exception as e:
            print("ERROR:", e)

        return toReturn

    def close(self):
        self.ser.close()

def main():
    tag = Tag()
    try:
        while True:
            distances = tag.get_current_distances()
            print("Distances:", distances)
            time.sleep(0.2)
    finally:
        tag.close() 

if __name__ == "__main__":
    main()
