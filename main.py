import serial
import serial.tools.list_ports
import time

def find_circuitpython_port():
    ports = serial.tools.list_ports.comports()

    for p in ports:
        description = p.description.lower()
        vid = p.vid

        # Known Adafruit VID for M0/M4 boards
        if vid == 0x239A:
            return p.device

        # Fallback if description matches
        if "circuitpython" in description or "adafruit" in description:
            return p.device

    # No specific board but ports exist
    if ports:
        return ports[0].device

    return None


def connect_serial():
    """Returns an open serial connection or None."""
    port = find_circuitpython_port()

    if not port:
        print("❌ No COM ports found.")
        return None

    try:
        ser = serial.Serial(port, 115200, timeout=1)
        time.sleep(2)  # Let board reboot
        print(f"✅ Connected to {port}")
        return ser
    except Exception as e:
        print("❌ Failed to connect:", e)
        return None


def send_command(ser, cmd):
    """Sends a command string to the board."""
    if ser is None:
        print("❌ Serial port not connected.")
        return
    ser.write((cmd + "\n").encode())

def sc(ser, cmd):
    if ser is None: return
    ser.write((cmd + "\n").encode())

def servo_turn(ser, pin, angle):
    send_command(ser, "Servo " + str(pin) + " " + str(angle))

def digital_pin(ser, pin, state):
    send_command(ser, "Digital " + str(pin) + " " + state)

def analog_pin(ser, pin, value):
    send_command(ser, "Analog " + str(pin) + " " + str(value))

# ------------------- TEST MODE -------------------
if __name__ == "__main__":
    ser = connect_serial()

    if ser is None:
        quit()

    print("Type commands. Type 'exit' to quit.")

    while True:
        cmd = input("> ")

        if cmd.lower() == "exit":
            break

        send_command(ser, cmd)
