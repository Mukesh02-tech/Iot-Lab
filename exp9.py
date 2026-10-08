import time
import smbus


# ============================================================
# MAX30100 LIBRARY
# ============================================================

INT_STATUS   = 0x00
INT_ENABLE   = 0x01
FIFO_WR_PTR  = 0x02
OVRFLOW_CTR  = 0x03
FIFO_RD_PTR  = 0x04
FIFO_DATA    = 0x05
MODE_CONFIG  = 0x06
SPO2_CONFIG  = 0x07
LED_CONFIG   = 0x09
TEMP_INTG    = 0x16
TEMP_FRAC    = 0x17
REV_ID       = 0xFE
PART_ID      = 0xFF

I2C_ADDRESS = 0x57

PULSE_WIDTH = {
    200: 0,
    400: 1,
    800: 2,
    1600: 3
}

SAMPLE_RATE = {
    50: 0,
    100: 1,
    167: 2,
    200: 3,
    400: 4,
    600: 5,
    800: 6,
    1000: 7
}

LED_CURRENT = {
    0: 0,
    4.4: 1,
    7.6: 2,
    11.0: 3,
    14.2: 4,
    17.4: 5,
    20.8: 6,
    24.0: 7,
    27.1: 8,
    30.6: 9,
    33.8: 10,
    37.0: 11,
    40.2: 12,
    43.6: 13,
    46.8: 14,
    50.0: 15
}

MODE_HR = 0x02
MODE_SPO2 = 0x03


def _get_valid(dictionary, value):
    try:
        return dictionary[value]
    except KeyError:
        raise KeyError(
            "Invalid value: {}. Use one of: {}".format(
                value, list(dictionary.keys())
            )
        )


class MAX30100:

    def __init__(
        self,
        i2c=None,
        mode=MODE_HR,
        sample_rate=100,
        led_current_red=11.0,
        led_current_ir=11.0,
        pulse_width=1600,
        max_buffer_len=10000
    ):

        self.i2c = i2c if i2c else smbus.SMBus(1)

        self.buffer_red = []
        self.buffer_ir = []

        self.max_buffer_len = max_buffer_len

        self.set_mode(MODE_HR)
        self.set_led_current(
            led_current_red,
            led_current_ir
        )
        self.set_spo_config(
            sample_rate,
            pulse_width
        )

    @property
    def red(self):
        if self.buffer_red:
            return self.buffer_red[-1]
        return None

    @property
    def ir(self):
        if self.buffer_ir:
            return self.buffer_ir[-1]
        return None

    def set_led_current(
        self,
        led_current_red=11.0,
        led_current_ir=11.0
    ):

        red = _get_valid(
            LED_CURRENT,
            led_current_red
        )

        ir = _get_valid(
            LED_CURRENT,
            led_current_ir
        )

        value = (red << 4) | ir

        self.i2c.write_byte_data(
            I2C_ADDRESS,
            LED_CONFIG,
            value
        )

    def set_mode(self, mode):

        reg = self.i2c.read_byte_data(
            I2C_ADDRESS,
            MODE_CONFIG
        )

        self.i2c.write_byte_data(
            I2C_ADDRESS,
            MODE_CONFIG,
            reg & 0x74
        )

        self.i2c.write_byte_data(
            I2C_ADDRESS,
            MODE_CONFIG,
            reg | mode
        )

    def set_spo_config(
        self,
        sample_rate=100,
        pulse_width=1600
    ):

        reg = self.i2c.read_byte_data(
            I2C_ADDRESS,
            SPO2_CONFIG
        )

        # Set sample rate bits
        rate = _get_valid(
            SAMPLE_RATE,
            sample_rate
        )

        # Set pulse width bits
        width = _get_valid(
            PULSE_WIDTH,
            pulse_width
        )

        # Clear sample-rate and pulse-width bits
        reg = reg & 0x00

        # Sample rate is bits 2-4
        reg |= (rate << 2)

        # Pulse width is bits 0-1
        reg |= width

        self.i2c.write_byte_data(
            I2C_ADDRESS,
            SPO2_CONFIG,
            reg
        )

    def enable_spo2(self):
        self.set_mode(MODE_SPO2)

    def disable_spo2(self):
        self.set_mode(MODE_HR)

    def read_sensor(self):

        data = self.i2c.read_i2c_block_data(
            I2C_ADDRESS,
            FIFO_DATA,
            4
        )

        ir_value = (data[0] << 8) | data[1]
        red_value = (data[2] << 8) | data[3]

        self.buffer_ir.append(ir_value)
        self.buffer_red.append(red_value)

        self.buffer_ir = self.buffer_ir[-self.max_buffer_len:]
        self.buffer_red = self.buffer_red[-self.max_buffer_len:]

    def shutdown(self):

        reg = self.i2c.read_byte_data(
            I2C_ADDRESS,
            MODE_CONFIG
        )

        self.i2c.write_byte_data(
            I2C_ADDRESS,
            MODE_CONFIG,
            reg | 0x80
        )

    def reset(self):

        reg = self.i2c.read_byte_data(
            I2C_ADDRESS,
            MODE_CONFIG
        )

        self.i2c.write_byte_data(
            I2C_ADDRESS,
            MODE_CONFIG,
            reg | 0x40
        )

    def get_part_id(self):

        return self.i2c.read_byte_data(
            I2C_ADDRESS,
            PART_ID
        )


# ============================================================
# MAIN PROGRAM
# ============================================================

print("Starting MAX30100...")

try:
    # Create MAX30100 object
    mx30 = MAX30100()
    # Enable SpO2 mode
    mx30.set_mode(MODE_SPO2)
    print("MAX30100 started.")
    print("Place your finger on the sensor.")
    print("Press Ctrl+C to stop.")
    print("--------------------------------")
    while True:
        mx30.read_sensor()
        print(
            "IR: {:5d}   RED: {:5d}".format(
                mx30.ir,
                mx30.red
            )
        )
        time.sleep(0.5)
except KeyboardInterrupt:
    print("\nProgram stopped.")
except Exception as e:
    print("\nERROR:")
    print(e)