import usb.core
import usb.util
import libusb_package
class thermal:

    def __init__(self):
        self.backend = libusb_package.get_libusb1_backend()
        self.device = usb.core.find(
            idVendor=0x0416,
            idProduct=0x5011,
            backend=self.backend
        )
        if self.device is None:
            raise Exception("Printer not found!")
        self.device.write(0x01, b"\x1b\x40")
        self.device.set_configuration()
        # CP860 / code page 3
        self.device.write(
            0x01,
            b"\x1b\x74\x03"
        )

    def print_text(self, text, max_chars=32):
        """
        Print text with automatic word wrapping.

        Words are never split unless a single word itself is
        longer than max_chars.
        """
        # Make sure we're working with a string
        text = str(text)
        # Preserve manually inserted line breaks
        paragraphs = text.split('\n')
        output_lines = []
        for paragraph in paragraphs:
            # Preserve completely empty lines
            if not paragraph.strip():
                output_lines.append('')
                continue
            words = paragraph.split()
            current_line = ''
            for word in words:
                # Normal case: word fits on the current line
                if len(current_line) + len(word) + 1 <= max_chars:
                    if current_line:
                        current_line += ' ' + word
                    else:
                        current_line = word
                else:
                    # Current line is full
                    if current_line:
                        output_lines.append(current_line)
                    # If the word itself is too long, split it
                    # because there is no space where we can break it.
                    while len(word) > max_chars:
                        output_lines.append(word[:max_chars])
                        word = word[max_chars:]
                    current_line = word
            if current_line:
                output_lines.append(current_line)
        # Add newline between every printed line
        output = '\n'.join(output_lines)
        self.device.write(
            0x01,
            output.encode('cp860')
        )

    def print_qr(self, data):
        data = data.encode("utf-8")

        # QR Model 2
        self.device.write(
            0x01,
            b"\x1d\x28\x6b\x04\x00\x31\x41\x32\x00"
        )

        # Size
        self.device.write(
            0x01,
            b"\x1d\x28\x6b\x03\x00\x31\x43\x05"
        )

        # Error correction = L
        self.device.write(
            0x01,
            b"\x1d\x28\x6b\x03\x00\x31\x45\x30"
        )

        # Store data
        length = len(data) + 3
        pL = length & 0xFF
        pH = (length >> 8) & 0xFF

        command = (
            b"\x1d\x28\x6b"
            + bytes([pL, pH])
            + b"\x31\x50\x30"
            + data
        )

        self.device.write(
            0x01,
            command
        )

        # Print
        self.device.write(
            0x01,
            b"\x1d\x28\x6b\x03\x00\x31\x51\x30"
        )

    def underline(self, toggle=False):
        if toggle:
            self.device.write(
                0x01,
                b"\x1b\x2d\x32"
            )
        else:
            self.device.write(
                0x01,
                b"\x1b\x2d\x00"
            )

    def center(self, toggle=False):
        if toggle:
            self.device.write(
                0x01,
                b"\x1b\x61\x01"
            )
        else:
            self.device.write(
                0x01,
                b"\x1b\x61\x00"
            )
            
    def cut(self):
        self.print_text("\n\n\n\n\n")
  
    def __del__(self):
        try:
            if self.device is not None:
                usb.util.dispose_resources(self.device)
        except:
            pass
