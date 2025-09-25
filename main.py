# -*- coding: utf-8 -*-er
from gpiozero import LED
import subprocess
import signal
import time
import re
import os



def get_connected_devices(led_process = None):
    # Utilise arp-scan pour scanner le réseau local
    led_process = subprocess.Popen(["python3", "led_orange_clignotement.py"])
    
    try:
        result = subprocess.check_output("sudo arp-scan --localnet --timeout=1 --retry=1 --interval=1", shell=True).decode('utf-8')
        print(result)
    except subprocess.CalledProcessError as e:
        print("Erreur lors du scan réseau:", e)
        return []

    # Filtrer les lignes contenant des adresses IP et MAC


    for line in result.splitlines():
        match = re.match(r"(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F:]+)\s+(.+)", line)
        if match is not None:
            return match.group(1), led_process
    return None



def main():
    while True:
        print("Scan du réseau...")
        device, led_process = get_connected_devices()
        print(device)
        if device is not None:
            if int(device.split(".")[3]) >= 30:
                if device not in [d for d in os.listdir("librarien/") if os.path.isdir(os.path.join("librarien/", d))]:
                    subprocess.Popen(["python3", "create_librarian_on_connect.py", device])
                    os.kill(led_process.pid, signal.SIGTERM)
                    led_process = subprocess.Popen(["python3", "led_verte.py"])
						
                else:
                    if subprocess.Popen(["python3", "dechiffrer.py", device]):
                        os.kill(led_process.pid, signal.SIGTERM)
                        led_process = subprocess.Popen(["python3", "led_verte.py"])
                    else:
                        led_process = subprocess.Popen(["python3", "led_rouge.py"])
            
            
    
               
        else:
            led_process = subprocess.Popen(["python3", "led_rouge.py"])

        

        # Attendre un certain temps avant de scanner à nouveau (ex. 10 secondes)
        time.sleep(100)
        os.kill(led_process.pid, signal.SIGTERM)

if __name__ == "__main__":
    main()
