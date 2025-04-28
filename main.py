import serial
import pyautogui
import time

try:
    porta_seriale = 'COM5'  # Cambia con la tua porta seriale
    velocita_baud = 9600
    ser = serial.Serial(porta_seriale, velocita_baud)
    print(f"Connesso a {porta_seriale} alla velocità di {velocita_baud}")
except serial.SerialException as e:
    print(f"Errore nell'apertura della porta seriale: {e}")
    exit()

last_pressed = 0

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            stream = [n for n in line.split(',')]
            # Check necessario per accedere a tutti i 7 valori dei sensori per non avere errori
            if len(stream) == 7:
                # Formattaazione dei valori di accelerometro (x, y, z), giroscopio (x, y, z) e flex sensor su terminale
                length = 8
                formatted_line = ""
                for element in stream:
                    formatted_line += f"{element:<{length}}"
                print(formatted_line)
                #print(stream[2])

                current_time = time.time()

                gyro_x = int(stream[3])
                if gyro_x > 32000:
                    if (current_time - last_pressed > 0.5):
                        pyautogui.press('left')
                        current_time = last_pressed = time.time()
                elif gyro_x < -32000:
                    if (current_time - last_pressed > 0.5):
                        pyautogui.press('right')
                        current_time = last_pressed = time.time()




except KeyboardInterrupt:
    print("\nProgramma terminato.")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Porta seriale chiusa.")
