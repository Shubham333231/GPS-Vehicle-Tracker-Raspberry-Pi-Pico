# ═══════════════════════════════════════════════════
# GPS Vehicle Tracker - Configuration File
# Author: Shubham Sharma
# B.Tech ECE, Matoshri College of Engineering, Nashik
# ═══════════════════════════════════════════════════

# ─────────────────────────────────────────
# ADMIN SETTINGS
# ─────────────────────────────────────────
ADMIN_NUMBER = "+91XXXXXXXXXX"   # Replace with your phone number (with country code)

# ─────────────────────────────────────────
# GPS SETTINGS
# ─────────────────────────────────────────
GPS_BAUDRATE = 9600              # Neo-6M default baud rate
GPS_UPDATE_INTERVAL = 10         # Seconds between GPS reads (10s testing, 60s production)
local_offset = 5.5               # UTC+5:30 for India

# ─────────────────────────────────────────
# GSM SETTINGS
# ─────────────────────────────────────────
GSM_BAUDRATE = 9600              # SIM800L default baud rate
GSM_CHECK_INTERVAL_MS = 10000   # Check incoming SMS every 10 seconds
LOCATION_INTERVAL_MS = 60000    # Auto-send location every 60 seconds (1 minute)

# ─────────────────────────────────────────
# PIN CONFIGURATION
# ─────────────────────────────────────────
# GPS UART0
GPS_TX_PIN = 0                   # GP0 → GPS RX
GPS_RX_PIN = 1                   # GP1 ← GPS TX

# GSM UART1
GSM_TX_PIN = 4                   # GP4 → GSM RX
GSM_RX_PIN = 5                   # GP5 ← GSM TX

# LED Indicators
GPS_LED_PIN = 14                 # GP14 → GPS Lock LED
GSM_LED_PIN = 15                 # GP15 → GSM Network LED
ONBOARD_LED_PIN = 25             # GP25 → Onboard LED

# ─────────────────────────────────────────
# REWARD / ACCURACY SETTINGS
# ─────────────────────────────────────────
GPS_ACCURACY_METERS = 2.5        # Neo-6M accuracy in meters
MIN_SATELLITES_REQUIRED = 4      # Minimum satellites for valid fix
SPEED_UNIT = 'kph'               # Speed unit: 'kph' or 'mph'

# ─────────────────────────────────────────
# DEBUG SETTINGS
# ─────────────────────────────────────────
DEBUG_MODE = True                # Set False in production
SERIAL_MONITOR = True            # Print logs to Thonny serial monitor
