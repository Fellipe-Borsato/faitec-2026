import usb.core
import usb.util
import libusb_package

from PIL import Image, ImageDraw, ImageFont, ImageOps
from random import randrange


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

    def print_mirrored_text(self, text, font_size=32):
        # POS-58 is normally 384 dots wide
        printer_width = 384

        # Leave a small margin on both sides
        margin = 10
        max_text_width = printer_width - (margin * 2)

        # Use a Windows font that supports Portuguese characters
        font = ImageFont.truetype(
            r".\Fonts\Roboto-Regular.ttf",
            font_size
        )

        # Temporary image used for measuring text
        dummy = Image.new("L", (1, 1), 255)
        draw = ImageDraw.Draw(dummy)

        # Convert the text into lines based on actual pixel width
        paragraphs = text.split('\n')
        lines = []

        for paragraph in paragraphs:

            # Preserve empty lines
            if not paragraph.strip():
                lines.append('')
                continue

            words = paragraph.split()
            current_line = ''

            for word in words:

                # Try adding the next word
                if current_line:
                    test_line = current_line + ' ' + word
                else:
                    test_line = word

                bbox = draw.textbbox(
                    (0, 0),
                    test_line,
                    font=font
                )

                text_width = bbox[2] - bbox[0]

                # Word still fits
                if text_width <= max_text_width:
                    current_line = test_line

                else:
                    # Save the current line
                    if current_line:
                        lines.append(current_line)

                    # Check whether the word itself is too large
                    word_bbox = draw.textbbox(
                        (0, 0),
                        word,
                        font=font
                    )

                    word_width = word_bbox[2] - word_bbox[0]

                    if word_width <= max_text_width:
                        current_line = word

                    else:
                        # The word itself is wider than the printer.
                        # Split it character-by-character based on
                        # actual pixel width.
                        current_line = ''

                        for char in word:

                            test_char_line = current_line + char

                            char_bbox = draw.textbbox(
                                (0, 0),
                                test_char_line,
                                font=font
                            )

                            char_width = (
                                char_bbox[2] - char_bbox[0]
                            )

                            if char_width <= max_text_width:
                                current_line = test_char_line

                            else:
                                if current_line:
                                    lines.append(current_line)

                                current_line = char

            if current_line:
                lines.append(current_line)

        # Calculate line height
        line_bbox = draw.textbbox(
            (0, 0),
            "Ag",
            font=font
        )

        line_height = line_bbox[3] - line_bbox[1]

        # Space between lines
        line_spacing = 4

        # Total image height
        image_height = (
            margin * 2
            + (line_height * len(lines))
            + (line_spacing * max(0, len(lines) - 1))
        )

        # Width is always the full printer width
        image_width = printer_width

        # Width must be divisible by 8
        image_width = ((image_width + 7) // 8) * 8

        image = Image.new(
            "L",
            (image_width, image_height),
            255
        )

        draw = ImageDraw.Draw(image)

        # Draw each wrapped line
        y = margin

        for line in lines:

            # Calculate actual width of this line
            bbox = draw.textbbox(
                (0, 0),
                line,
                font=font
            )

            line_width = bbox[2] - bbox[0]

            # Center the line horizontally
            x = (printer_width - line_width) // 2

            draw.text(
                (x, y),
                line,
                font=font,
                fill=0
            )

            y += line_height + line_spacing

        # Flip horizontally
        image = ImageOps.mirror(image)

        # Convert pixels to ESC/POS bitmap data
        width, height = image.size

        data = bytearray()

        for y in range(height):

            for x in range(0, width, 8):

                byte = 0

                for bit in range(8):

                    pixel = image.getpixel(
                        (x + bit, y)
                    )

                    # Black pixel = 1
                    if pixel < 128:
                        byte |= (1 << (7 - bit))

                data.append(byte)

        # Number of bytes per horizontal row
        width_bytes = width // 8

        xL = width_bytes & 0xFF
        xH = (width_bytes >> 8) & 0xFF

        yL = height & 0xFF
        yH = (height >> 8) & 0xFF

        # GS v 0
        command = (
            b"\x1d\x76\x30\x00"
            + bytes([xL, xH, yL, yH])
            + data
        )

        self.device.write(
            0x01,
            command
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
       
    def get_random_phrase(self):
        conn = sqlite3.connect(self.DB_FILE)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT frase, tipo
            FROM biscoito
            ORDER BY RANDOM()
            LIMIT 1
        """)

        result = cursor.fetchone()

        conn.close()

        if result is None:
            return None

        return [
            value.replace("\xa0", " ") if isinstance(value, str) else value
            for value in result
        ]

    def __del__(self):
        try:
            if self.device is not None:
                usb.util.dispose_resources(self.device)
        except:
            pass


# ============================================================
# SINGLE SHARED PRINTER
# ============================================================

printer = thermal()

# Only one thread can communicate with the printer at a time
printer_lock = threading.Lock()

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

    def print_mirrored_text(self, text, font_size=32):
        # POS-58 is normally 384 dots wide
        printer_width = 384

        # Leave a small margin on both sides
        margin = 10
        max_text_width = printer_width - (margin * 2)

        # Use a Windows font that supports Portuguese characters
        font = ImageFont.truetype(
            r"C:\Users\MOACIR\AppData\Local\Roblox\Versions\version-48a28da848b7420d\content\fonts\Roboto-Regular.ttf",
            font_size
        )

        # Temporary image used for measuring text
        dummy = Image.new("L", (1, 1), 255)
        draw = ImageDraw.Draw(dummy)

        # Convert the text into lines based on actual pixel width
        paragraphs = text.split('\n')
        lines = []

        for paragraph in paragraphs:

            # Preserve empty lines
            if not paragraph.strip():
                lines.append('')
                continue

            words = paragraph.split()
            current_line = ''

            for word in words:

                # Try adding the next word
                if current_line:
                    test_line = current_line + ' ' + word
                else:
                    test_line = word

                bbox = draw.textbbox(
                    (0, 0),
                    test_line,
                    font=font
                )

                text_width = bbox[2] - bbox[0]

                # Word still fits
                if text_width <= max_text_width:
                    current_line = test_line

                else:
                    # Save the current line
                    if current_line:
                        lines.append(current_line)

                    # Check whether the word itself is too large
                    word_bbox = draw.textbbox(
                        (0, 0),
                        word,
                        font=font
                    )

                    word_width = word_bbox[2] - word_bbox[0]

                    if word_width <= max_text_width:
                        current_line = word

                    else:
                        # The word itself is wider than the printer.
                        # Split it character-by-character based on
                        # actual pixel width.
                        current_line = ''

                        for char in word:

                            test_char_line = current_line + char

                            char_bbox = draw.textbbox(
                                (0, 0),
                                test_char_line,
                                font=font
                            )

                            char_width = (
                                char_bbox[2] - char_bbox[0]
                            )

                            if char_width <= max_text_width:
                                current_line = test_char_line

                            else:
                                if current_line:
                                    lines.append(current_line)

                                current_line = char

            if current_line:
                lines.append(current_line)

        # Calculate line height
        line_bbox = draw.textbbox(
            (0, 0),
            "Ag",
            font=font
        )

        line_height = line_bbox[3] - line_bbox[1]

        # Space between lines
        line_spacing = 4

        # Total image height
        image_height = (
            margin * 2
            + (line_height * len(lines))
            + (line_spacing * max(0, len(lines) - 1))
        )

        # Width is always the full printer width
        image_width = printer_width

        # Width must be divisible by 8
        image_width = ((image_width + 7) // 8) * 8

        image = Image.new(
            "L",
            (image_width, image_height),
            255
        )

        draw = ImageDraw.Draw(image)

        # Draw each wrapped line
        y = margin

        for line in lines:

            # Calculate actual width of this line
            bbox = draw.textbbox(
                (0, 0),
                line,
                font=font
            )

            line_width = bbox[2] - bbox[0]

            # Center the line horizontally
            x = (printer_width - line_width) // 2

            draw.text(
                (x, y),
                line,
                font=font,
                fill=0
            )

            y += line_height + line_spacing

        # Flip horizontally
        image = ImageOps.mirror(image)

        # Convert pixels to ESC/POS bitmap data
        width, height = image.size

        data = bytearray()

        for y in range(height):

            for x in range(0, width, 8):

                byte = 0

                for bit in range(8):

                    pixel = image.getpixel(
                        (x + bit, y)
                    )

                    # Black pixel = 1
                    if pixel < 128:
                        byte |= (1 << (7 - bit))

                data.append(byte)

        # Number of bytes per horizontal row
        width_bytes = width // 8

        xL = width_bytes & 0xFF
        xH = (width_bytes >> 8) & 0xFF

        yL = height & 0xFF
        yH = (height >> 8) & 0xFF

        # GS v 0
        command = (
            b"\x1d\x76\x30\x00"
            + bytes([xL, xH, yL, yH])
            + data
        )

        self.device.write(
            0x01,
            command
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
       
    def get_random_phrase(self):
        conn = sqlite3.connect(self.DB_FILE)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT frase, tipo
            FROM biscoito
            ORDER BY RANDOM()
            LIMIT 1
        """)

        result = cursor.fetchone()

        conn.close()

        if result is None:
            return None

        return [
            value.replace("\xa0", " ") if isinstance(value, str) else value
            for value in result
        ]

    def __del__(self):
        try:
            if self.device is not None:
                usb.util.dispose_resources(self.device)
        except:
            pass


# ============================================================
# SINGLE SHARED PRINTER
# ============================================================

printer = thermal()

# Only one thread can communicate with the printer at a time
printer_lock = threading.Lock()
