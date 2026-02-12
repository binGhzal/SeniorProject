"""Archived Raspberry Pi-specific sensor implementation kept for reference only."""

import time

try:
    import smbus2  # type: ignore
except ImportError:  # pragma: no cover
    smbus2 = None

try:
    import cv2  # type: ignore
except ImportError:  # pragma: no cover
    cv2 = None

try:
    import RPi.GPIO as GPIO  # type: ignore
except ImportError:  # pragma: no cover
    GPIO = None

# BMI160 Constants
BMI160_ADDR = 0x68
REG_ACCEL_X = 0x12
REG_CMD = 0x7E
CMD_SOFT_RESET = 0xB6

class IMUSensor:
    """Legacy IMU wrapper with hardwired Raspberry Pi assumptions."""

    def __init__(self, bus_num=1):
        if smbus2 is None:
            class _StubBus:
                def write_byte_data(self, *_args, **_kwargs):
                    """No-op write for non-Raspberry Pi environments."""
                    return None

                def read_i2c_block_data(self, *_args, **_kwargs):
                    """Return zeroed sample data for non-hardware execution."""
                    return [0, 0, 0, 0, 0, 0]

            self.bus = _StubBus()
        else:
            self.bus = smbus2.SMBus(bus_num)
        self.address = BMI160_ADDR
        self._init_sensor()

    def _init_sensor(self):
        # Soft reset to ensure clean state
        try:
            self.bus.write_byte_data(self.address, REG_CMD, CMD_SOFT_RESET)
            time.sleep(0.1)
            # Configure accelerometer (normal power mode) - strict implementation required here
            # For prototype: assuming default config works after reset
        except (OSError, AttributeError) as e:
            print(f"IMU Init Error: {e}")

    def read_accel(self):
        """Reads X, Y, Z acceleration data."""
        try:
            # Read 6 bytes starting from REG_ACCEL_X
            data = self.bus.read_i2c_block_data(self.address, REG_ACCEL_X, 6)

            # Convert 2's complement
            x = self._bytes_to_int(data[1], data[0])
            y = self._bytes_to_int(data[3], data[2])
            z = self._bytes_to_int(data[5], data[4])

            # Convert to 'g' (assuming default range +/- 2g)
            scale = 16384.0
            return (x/scale, y/scale, z/scale)
        except (OSError, AttributeError, IndexError, TypeError, ValueError):
            return (0, 0, 0)

    def _bytes_to_int(self, msb, lsb):
        val = (msb << 8) | lsb
        if val & 0x8000:
            return -((val ^ 0xFFFF) + 1)
        return val

class CameraModule:
    """Legacy camera wrapper using OpenCV capture."""

    def __init__(self):
        if cv2 is None:
            self.cap = None
            return
        # Index 0 is usually the default Pi Camera
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def get_frame(self):
        """Return latest frame or None if unavailable."""
        if self.cap is None:
            return None
        ret, frame = self.cap.read()
        if ret:
            return frame
        return None

    def release(self):
        """Release the camera capture handle."""
        if self.cap is not None:
            self.cap.release()

class IRSys:
    """Controls the IR LED array via GPIO."""

    def __init__(self, pin=18):
        self.pin = pin
        self.pwm = None
        if GPIO is None:
            return

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 100)  # 100Hz frequency
        self.pwm.start(0)

    def set_brightness(self, duty_cycle):
        """0 to 100% brightness."""
        if self.pwm is not None:
            self.pwm.ChangeDutyCycle(duty_cycle)

    def cleanup(self):
        """Release PWM and GPIO resources if initialized."""
        if self.pwm is not None:
            self.pwm.stop()
        if GPIO is not None:
            GPIO.cleanup()
