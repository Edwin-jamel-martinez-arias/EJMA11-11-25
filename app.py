from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)

API = "https://pokeapi.co/api/v2/pokemon/"

app.secret_key = "Edwin"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_pokemon():
    pokemon_name = request.form.get('pokemon_name', '')

    if not pokemon_name:
        flash("Por favor, escribe el nombre o ID de un Pokémon.")
        return redirect(url_for('index'))

    pokemon_data = None
    
    try:
        resp = requests.get(f"{API}{pokemon_name}")

        if resp.status_code == 200:
            pokemon_data = resp.json()
            
            pokemon_info =  {
                'name': pokemon_data['name'].title(),
                'id': pokemon_data['id'],
                'height': pokemon_data['height'] / 10,
                'weight': pokemon_data['weight'] / 10,
                'image': pokemon_data['sprites']['front_default'],
                'types': [t['type']['name'].title() for t in pokemon_data['types']],
                'abilities': [a['ability']['name'].title() for a in pokemon_data['abilities']]
            }

    except resp.status_code == 500:
        flash(f"Ocurrió un error inesperado al procesar la información:")
        return redirect(url_for('index'))
    return render_template('respuesta.html', pokemon=pokemon_info)

if __name__ == '__main__':
    app.run(debug=True)
