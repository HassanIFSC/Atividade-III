import tkinter as tk
import time
import random
import threading
import requests


# Definição de váriaveis para limitar o alcance na hora de gerar dados

TEMP_MIN = 24.2
TEMP_MAX = 27.3
HUM_MIN = 69.0
HUM_MAX = 82.0
LIGHT_MIN = 69.0
LIGHT_MAX = 82.0


# Gerando dados

def generate_data():
    return {
        'temperature': format(random.uniform(TEMP_MIN, TEMP_MAX), '.1f'),
        'humidity': format(random.uniform(HUM_MIN, HUM_MAX), '.1f'),
        'light': format(random.uniform(LIGHT_MIN, LIGHT_MAX), '.1f')
    }


# Formatando dados para a janela

def format_data(data):
    return f"  ID: {data['id']}  |  Temperatura: {data['temperature']}  |  Umidade: {data['humidity']}  |  Luminosidade: {data['light']}  |  Registro: {data['timestamp']}"


# Atualizando a janela

def update_listbox(listbox):
    while True:
        data = generate_data()
        formatted_data = format_data(data)
        listbox.insert(tk.END, formatted_data)
        time.sleep(10)


# Enviando dados para o Web Service

def send_data(data):
    url = "http://localhost:5000/graphql"
    mutation = f'''
    mutation {{
        createSensorData(input: {{temperature: {data['temperature']}, humidity: {data['humidity']}, light: {data['light']}}}) {{
            sensorData {{
                id
                temperature
                humidity
                light
                timestamp
            }}
        }}
    }}
    '''
    try:
        response = requests.post(url, json={'query': mutation})
        response_json = response.json()
        print(response_json)
        return response_json["data"]["createSensorData"]["sensorData"]
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar dados: {e}")

# Enviando dados para a janela

def start_sending_data(listbox=None):
    while True:
        data = generate_data()
        sent_data = send_data(data)
        if listbox:
            formatted_data = format_data(sent_data)
            listbox.insert(tk.END, formatted_data)
        time.sleep(10)


# Definindo a interface

def create_gui():
    root = tk.Tk()
    root.title("Sensor")

    frame = tk.Frame(root)
    frame.pack()

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = tk.Listbox(frame, height=16, width=96, font=(
        "Helvetica", 12, 'bold'), yscrollcommand=scrollbar.set)
    listbox.pack(side=tk.LEFT, fill=tk.X, anchor='nw')

    scrollbar.config(command=listbox.yview)

    threading.Thread(target=start_sending_data,
                     args=(listbox,), daemon=True).start()

    root.mainloop()


if __name__ == "__main__":
    create_gui()
