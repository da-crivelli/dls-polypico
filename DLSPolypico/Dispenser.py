import serial
import warnings
from .utils import get_likely_com_port


SERIAL_BAUD = 115200
SERIAL_TIMEOUT = 0.1
PURGE_CONST = 100


class Dispenser:
    def __init__(self, port=None) -> None:
        if port is None:
            get_likely_com_port()
        else:
            self.serial_port_name = port

        self._initialise_serial(port, baud=SERIAL_BAUD, timeout=SERIAL_TIMEOUT)

    def __del__(self):
        # close the serial port if left open
        self.serial.close()

    def dispense(self, mode):
        """Starts dispensing. Mode can be "continuous" or "packet"."""
        if mode == "continuous":
            self.dispense_continuous()
        elif mode == "packet":
            self.dispense_packet(packet_length=self.options["packet_length"])
        else:
            warnings.warn("Mode not recognised; stopping dispense")
            self.dispense_stop()

    def dispense_continuous(self):
        """Starts continuous dispensing"""
        self._serial_write("PGD")

    def dispense_packet(self, packet_length):
        """Starts packet dispensing"""
        self._serial_write("PN1", packet_length)
        self._serial_write("PGP")

    def dispense_stop(self):
        """Stops dispensing"""
        self._serial_write("PGS")

    def purge(self, purge_time=PURGE_CONST):
        """Run purge"""
        self._serial_write("PC", purge_time)

    def _initialise_serial(self, port: str, baud, timeout) -> None:
        self.serial = serial.Serial(port, baud, timeout=timeout)

    def _serial_write(self, cmd_string, cmd_val="") -> None:
        # TODO: do clipping here and raise a warning if out of bounds?
        self.serial.write(f"{cmd_string}{cmd_val}\r")
        # TODO: then check for the readback
