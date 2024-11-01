import os
from flask import Flask, render_template, request, flash, redirect, url_for
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Ruta principal que muestra el formulario de escaneo de puertos
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para escanear puertos
@app.route('/portscan', methods=['POST'])
def portscan():
    if request.method == 'POST':
        direccion = request.form['direccion']
        
        # Verificación básica de IP/dominio
        if not direccion:
            flash("Por favor ingrese una dirección válida", "danger")
            return redirect(url_for('index'))

        # Llamar a la API de escaneo de puertos
        api_key = os.getenv('VIEWDNS_API_KEY')
        url = f"https://api.viewdns.info/portscan/?host={direccion}&apikey={api_key}&output=json"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                resultados = response.json()
                if 'response' in resultados and 'port' in resultados['response']:
                    # Filtrar los puertos abiertos
                    ports = [port for port in resultados['response']['port'] if port['status'] == 'open']
                    return render_template('index.html', ports=ports, direccion=direccion)
                else:
                    flash("No se encontraron resultados para el escaneo de puertos.", "warning")
            else:
                flash("Error al conectarse a la API de ViewDNS.", "danger")
        except Exception as e:
            flash(f"Error: {e}", "danger")
        
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
