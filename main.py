# GPS Vehicle Tracker using Raspberry Pi Pico
# Author: Shubham Sharma
# B.Tech ECE, Matoshri College of Engineering, Nashik
# Tech Stack: MicroPython, Neo-6M GPS, SIM800L GSM, RP2040

from machine import UART, Pin
import utime
from micropygps import MicropyGPS

# ─────────────────────────────────────────
# CONFIGURATION — Edit before deploying
# ─────────────────────────────────────────
ADMIN_NUMBER = "+91XXXXXXXXXX"   # Your phone number
GPS_UPDATE_INTERVAL = 10          # Seconds between GPS checks
LOCATION_INTERVAL_MS = 60 * 1000  # SMS every 60 seconds
GSM_CHECK_INTERVAL_MS = 10000     # GSM status check every 10s
local_offset = 5.5                # UTC+5:30 India

# ─────────────────────────────────────────
# HARDWARE PIN CONFIGURATION
# ─────────────────────────────────────────
# GPS Module (Neo-6M) → UART0
# GP0 (TX) → GPS RX
# GP1 (RX) → GPS TX

# GSM Module (SIM800L) → UART1
# GP4 (TX) → GSM RX
# GP5 (RX) → GSM TX

# LED Status Indicators
# GP14 → GPS Lock LED
# GP15 → GSM Network LED

# ─────────────────────────────────────────
# HARDWARE INITIALIZATION
# ─────────────────────────────────────────
uart_gps = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
uart_gsm = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

gps_led = Pin(14, Pin.OUT)
gsm_led = Pin(15, Pin.OUT)
onboard_led = Pin(25, Pin.OUT)

# GPS Parser
gps = MicropyGPS(local_offset)

# ─────────────────────────────────────────
# GSM FUNCTIONS
# ─────────────────────────────────────────
def gsm_send_command(command, delay=1000):
    """Send AT command to SIM800L GSM module"""
    uart_gsm.write(command + '\r\n')
    utime.sleep_ms(delay)
    response = ''
    while uart_gsm.any():
        response += uart_gsm.read().decode('utf-8', 'ignore')
    return response

def gsm_init():
    """Initialize GSM module"""
    print("Initializing GSM...")
    gsm_send_command('AT')           # Test connection
    gsm_send_command('AT+CMGF=1')    # Set SMS to text mode
    gsm_send_command('AT+CNMI=1,2,0,0,0')  # New SMS notification
    print("GSM Ready")

def send_sms(phone_number, message):
    """Send SMS with location data"""
    gsm_send_command('AT+CMGF=1')
    gsm_send_command(f'AT+CMGS="{phone_number}"', 500)
    uart_gsm.write(message + '\x1A')  # Ctrl+Z to send
    utime.sleep_ms(3000)
    print(f"SMS sent to {phone_number}")

def check_incoming_sms():
    """Check for incoming SMS commands"""
    if uart_gsm.any():
        data = uart_gsm.read().decode('utf-8', 'ignore')
        if 'LOCATION' in data:
            send_location()
        elif 'STATUS' in data:
            send_status()
        elif 'HELP' in data:
            send_help()

# ─────────────────────────────────────────
# GPS FUNCTIONS
# ─────────────────────────────────────────
def parse_gps():
    """Parse incoming NMEA sentences from GPS module"""
    if uart_gps.any():
        data = uart_gps.read()
        for byte in data:
            gps.update(chr(byte))

def get_location():
    """Get formatted GPS coordinates"""
    if gps.fix_stat:
        lat = gps.latitude[0] + gps.latitude[1] / 60
        lng = gps.longitude[0] + gps.longitude[1] / 60
        if gps.latitude[2] == 'S':
            lat = -lat
        if gps.longitude[2] == 'W':
            lng = -lng
        return lat, lng
    return None, None

def format_google_maps_link(lat, lng):
    """Generate Google Maps link from coordinates"""
    return f"https://maps.google.com/?q={lat},{lng}"

# ─────────────────────────────────────────
# SMS RESPONSE FUNCTIONS
# ─────────────────────────────────────────
def send_location():
    """Send current GPS location via SMS"""
    lat, lng = get_location()
    if lat and lng:
        maps_link = format_google_maps_link(lat, lng)
        message = (
            f"GPS LOCATION\n"
            f"Lat: {lat:.6f}\n"
            f"Lng: {lng:.6f}\n"
            f"Satellites: {gps.satellites_used}\n"
            f"Maps: {maps_link}"
        )
    else:
        message = "GPS: No fix yet. Please wait..."
    send_sms(ADMIN_NUMBER, message)

def send_status():
    """Send system status via SMS"""
    fix_status = "Fix acquired" if gps.fix_stat else "Searching..."
    message = (
        f"SYSTEM STATUS\n"
        f"GPS: {fix_status}\n"
        f"Satellites: {gps.satellites_used}\n"
        f"Speed: {gps.speed[2]:.1f} km/h\n"
        f"Uptime: {utime.ticks_ms() // 1000}s"
    )
    send_sms(ADMIN_NUMBER, message)

def send_help():
    """Send available commands via SMS"""
    message = (
        "COMMANDS:\n"
        "LOCATION - Get GPS coords\n"
        "STATUS - System status\n"
        "HELP - This message"
    )
    send_sms(ADMIN_NUMBER, message)

# ─────────────────────────────────────────
# LED STATUS INDICATORS
# ─────────────────────────────────────────
def update_leds():
    """Update LED status indicators"""
    # GPS LED: solid if fix acquired, blink if searching
    if gps.fix_stat:
        gps_led.value(1)
    else:
        gps_led.toggle()

    # GSM LED: blink to show network activity
    gsm_led.toggle()

# ─────────────────────────────────────────
# MAIN LOOP
# ─────────────────────────────────────────
def main():
    print("GPS Vehicle Tracker Starting...")
    print("Author: Shubham Sharma")
    print("Matoshri College of Engineering, Nashik")
    print("─" * 40)

    # Initialize hardware
    onboard_led.value(1)
    gsm_init()

    last_location_time = utime.ticks_ms()
    last_gsm_check = utime.ticks_ms()
    last_led_update = utime.ticks_ms()

    print("Waiting for GPS fix...")

    while True:
        current_time = utime.ticks_ms()

        # Parse GPS data continuously
        parse_gps()

        # Send location SMS every LOCATION_INTERVAL_MS
        if utime.ticks_diff(current_time, last_location_time) >= LOCATION_INTERVAL_MS:
            send_location()
            last_location_time = current_time

        # Check incoming SMS commands every GSM_CHECK_INTERVAL_MS
        if utime.ticks_diff(current_time, last_gsm_check) >= GSM_CHECK_INTERVAL_MS:
            check_incoming_sms()
            last_gsm_check = current_time

        # Update LEDs every 500ms
        if utime.ticks_diff(current_time, last_led_update) >= 500:
            update_leds()
            last_led_update = current_time

        utime.sleep_ms(10)

# Run
if __name__ == '__main__':
    main()
