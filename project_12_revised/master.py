import threading
import time
from tag import Tag
from control import Wheels
from listen import Listen
from ultrasonic import UltrasonicSensor


class Master:
    def __init__(self):
        self.tag = Tag()  # Create an instance of the Tag class
        self.listen = Listen()
        self.control = Wheels()
        self.ultra = UltrasonicSensor(18, 24)
        self.obstacle_threshold = 50  # Represents 50 cm
        self.label = {'go to the starting quadrant':  0, 'go to the charging station': 1, 'go to hunters office': 2, 'go to the restroom': 3}
        self.logging_tag = False
        self.stop_event = threading.Event()

    def run(self):
        try:
            # Start monitoring tag and listening in separate threads
            threading.Thread(target=self.tag_monitor).start()
            threading.Thread(target=self.ultra_monitor).start()
            while not self.stop_event.is_set():
                time.sleep(1)
        except KeyboardInterrupt:
            print("KeyboardInterrupt received. Stopping threads...")
            self.stop()

    def stop(self):
        self.stop_event.set()
        self.control.stop()

    def tag_monitor(self):
        print("Tag monitoring started\n")
        while not self.stop_event.is_set():
            try:
                distances = self.tag.get_current_distances()
                #print(distances)
                closest_anchor = min(distances, key=distances.get)
                #print("Closest anchor", closest_anchor)
            except KeyboardInterrupt:
                print("Tag monitor stopped due to KeyboardInterrupt")
            except Exception as e:
                print("Error in tag monitor\n:", e)
            time.sleep(0.2)

    def ultra_monitor(self):
        print("Obstacle detection started\n")
        while not self.stop_event.is_set():
            try:
                obstacle = self.ultra.measure_distance()
                if obstacle < self.obstacle_threshold:
                    self.control.stop()
                    self.listen_monitor()
                else:
                    pass
            except KeyboardInterrupt:
                print("Obstacle detection stopped due to KeyboardInterrupt")
            except Exception as e:
                print("Error in ultra monitor\n:", e)
            time.sleep(0.2)

    def listen_monitor(self):
        print("Listening monitor started\n")
        try:
            command = self.listen.listen_and_respond()
            if command is not None:
                command = command.lower()
                print("Command:", command)
                if command in self.label.keys():
                    self.move_to_quadrant(self.label[command])
        except KeyboardInterrupt:
            print("Listening monitor stopped due to KeyboardInterrupt")
        except Exception as e:
            print("Error in listening monitor\n:", e)
        time.sleep(0.2)
        return command

    def move_to_quadrant(self, quadrant):
        print("Called")
        while True:
            try:
                self.control.forward(90)
                time.sleep(1)
                dist_dict = self.tag.get_current_distances()
                if quadrant in dist_dict and dist_dict[quadrant] < 100:
                    print(f"FUCK YA")
                    self.listen.affirm_location_with_speech(quadrant)
                    break
                elif quadrant in dist_dict:
                    print(f"Moving towards {quadrant}....")
                    self.control.forward(90)
                    time.sleep(0.1)
                else:
                    print("Turning 90 degrees....")
                    self.control.right(90)
                    time.sleep(0.1)
            except KeyboardInterrupt:
                print("Stopped stopped due to KeyboardInterrupt")
                self.control.stop()
            except Exception as e:
                print("Error in Navigation\n:", e)
                self.control.stop()
            time.sleep(0.2)     

def main():
    master = Master()
    master.run()

if __name__ == "__main__":
    main()
