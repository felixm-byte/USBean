import serial
import time

def send_msg(content, port, baud_rate = 115200, is_temporary=False, display_time=0):
# Open connection
    try:
        ser = serial.Serial(port, baud_rate, timeout=1)
        time.sleep(2) # Wait for the board to reset/initialize
        # Send message to RP2040
        ser.write(content.encode('utf-8'))
        print(f"Sent: {content.strip()}")
        if is_temporary:
            time.sleep(display_time)
            ser.write("".encode('utf-8'))         
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ser.close()

def pi_active_at(port, baud_rate = 115200):
    try: 
        ser = serial.Serial(port, baud_rate, timeout=1)
        print(f"Success: connection established with {ser}")
    except Exception as e:
        print(f"Failure: connection failed with exception {e}")
        return False
    
def time_in_words(secs):
    text = ""
    hrs = 0
    mins = 0
    if secs >= 3600:
        hrs = secs // 3600
        secs -= hrs*3600
    if secs >= 60:
        mins = secs // 60
        secs -= mins*60
    
    if hrs >= 1:
        text = f"{hrs}:{'0' if len(str(mins)) != 2 else ''}{mins}:{'0' if len(str(secs)) != 2 else ''}{secs}"
    elif mins >=1:
        text = f"{mins}:{'0' if len(str(secs)) != 2 else ''}{secs}"
    else:
        text = f"{secs} seconds"
    return text
#def start_timer(duration): #Duration in seconds

def timer(time, port, baud_rate = 115200):
    if pi_active_at(port, baud_rate):
        send_msg(f"{time_in_words(time)} timer, starting soon :>", port, baud_rate)
        time.sleep(7)
        n = time
        while n >= 0:
            n-= 1
            text = time_in_words(time)
            send_msg(f"{time_in_words(time)} remaining", port, baud_rate)
            time.sleep(1)
        send_msg("Time's up!!", port, baud_rate, is_temporary=True, display_time=15)
    else:
        return False
        
