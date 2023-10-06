import tkinter as tk
import requests


# Montagem da janela e da seção de leitura mais recente

window = tk.Tk()
window.title("Consumidor")
window.geometry("600x375")
window.configure(bg='#003884')

last_reading_label = tk.Label(window, text="Última Leitura:", font=(
    "Helvetica", 12, 'bold'), bg='#003884', fg='#ffffff')
last_reading_label.grid(row=0, column=0, padx=10, pady=10)

last_reading_data = tk.Label(window, text="", font=(
    "Helvetica", 12, 'bold'), bg='#003884', fg='#ffffff')
last_reading_data.grid(row=0, column=1, padx=10, pady=10)

last_reading_time = tk.Label(window, text="", font=(
    "Helvetica", 12, 'bold'), bg='#003884', fg='#ffffff')
last_reading_time.grid(row=1, column=1, padx=10, pady=10)


# Função para requisitar uma query

def graphql_request(query):
    url = "http://localhost:5000/graphql"
    response = requests.post(url, json={'query': query})
    return response.json()


# Função para atualizar e recuperar a última leitura

def update_last_reading():
    data = graphql_request('''
    query {
        lastId
    }
    ''')
    last_id = data['data']['lastId']

    data = graphql_request(f'''
    query {{
        sensorData(id: "{last_id}") {{
            id
            temperature
            humidity
            light
            timestamp
        }}
    }}
    ''')

    sensor_data = data['data']['sensorData']

    last_reading_data['text'] = f"ID: {sensor_data['id']}\nTemperatura: {sensor_data['temperature']}°C\nUmidade: {sensor_data['humidity']}%\nLuminosidade: {sensor_data['light']}"
    last_reading_time['text'] = f"Data e hora do registro: {sensor_data['timestamp']}"


# Botão "Atualizar"

update_button = tk.Button(window, text="Atualizar",
                          command=update_last_reading)
update_button.grid(row=2, column=0, padx=10, pady=10)


# Seção para requisitar uma data e hora e específica

select_label = tk.Label(
    window, text="Digite uma data e hora: \n(AAAA-MM-DDTHH:MM:SS)", font=(
        "Helvetica", 12, 'bold'), bg='#003884', fg='#ffffff')
select_label.grid(row=3, column=0, padx=10, pady=10)

select_entry = tk.Entry(window, width=24, font=(
    "Helvetica", 12, 'bold'))
select_entry.grid(row=3, column=1, padx=10, pady=10)

selected_data_label = tk.Label(window, text="", font=(
    "Helvetica", 12, 'bold'), bg='#003884', fg='#ffffff')
selected_data_label.grid(row=4, column=1, padx=10, pady=10)


# Função para procurar por uma data e hora específica

def search_data():
    timestamp = select_entry.get()

    data = graphql_request(f'''
    query {{
        sensorDataByTime(timestamp: "{timestamp}") {{
            id
            temperature
            humidity
            light
        }}
    }}
    ''')

    if 'errors' in data or data['data']['sensorDataByTime'] is None:
        selected_data_label['text'] = "Nenhum dado encontrado\n para essa data e hora."
    else:
        sensor_data = data['data']['sensorDataByTime']
        selected_data_label['text'] = f"ID: {sensor_data['id']}\nTemperatura: {sensor_data['temperature']}°C\nUmidade: {sensor_data['humidity']}%\nLuminosidade: {sensor_data['light']}"


# Botão "Buscar"

search_button = tk.Button(window, text="Buscar", command=search_data)
search_button.grid(row=4, column=0, padx=10, pady=10)

window.mainloop()
