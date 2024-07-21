import atexit
import enum
import smbus
bus = smbus.SMBus(1)

ADD = 0x1B

class MotorDirection(enum.Enum):
    FORWARD = 1
    BACKWARD = 0 

class ExtensionBoard():

    def __init__(self):
        atexit.register(self._release)
        
    def set_motor(self, motor_id, value):
        """Sets motor value between [-1, 1]"""
        mapped_value = int(255.0 * value)
        speed = min(max(abs(mapped_value), 0), 255)
        if mapped_value > 0:
            forward = [1,speed]
            bus.write_i2c_block_data(ADD, 0x03 + motor_id,forward)
        else:
            backward = [0,speed]
            bus.write_i2c_block_data(ADD, 0x03 + motor_id, backward)

    def set_both_motors(self, motor1_speed, motor2_speed=None):
        """Sets motor value between [-1, 1]"""
        mapped_value1 = int(255.0 * motor1_speed)
        mapped_value2 = int(255.0 * motor2_speed) if motor2_speed else mapped_value1

        speed_motor1 = min(max(abs(mapped_value1), 0), 255)
        speed_motor2 = min(max(abs(mapped_value2), 0), 255)

        print(f"speed1: {speed_motor1}, speed2: {speed_motor2}")

        bus.write_i2c_block_data(ADD, 0x01, [int(mapped_value1 > 0), speed_motor1, int(mapped_value2 > 0), speed_motor2])

    def rotate_right(self, speed):
        self.set_both_motors(speed, -speed)

    def rotate_left(self, speed):
        self.set_both_motors(-speed, speed)

    def stop_motors(self):
        self._release()

    def buzz(self, value):
        bus.write_i2c_block_data(ADD, 0x06, [value])
    
    def servo_control(self, value1, value2):
        bus.write_i2c_block_data(ADD, 0x03, [value1, value2])
    
    def _release(self):
        """Stops motor by releasing control"""
        bus.write_byte_data(ADD,0x02,0x00)

