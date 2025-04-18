import requests

GOOGLE_MAPS_API_KEY = 'AIzaSyD6weEz28oqcKlc7FOgA9zKxJRf3uAHpU8'

@app.route('/')
def index():
    origin = "Bangalore, India"
    destination = "Indiranagar, Bangalore, India"

    # Google Maps Directions API call
    directions_url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(directions_url)
    data = response.json()

    if data['status'] == 'OK':
        steps = data['routes'][0]['legs'][0]['steps']
        duration = data['routes'][0]['legs'][0]['duration']['text']

        path = " → ".join([origin] + [step['html_instructions'] for step in steps] + [destination])

    else:
        path = "No route found"
        duration = "N/A"

    # Dummy graph for visualization
    G = nx.Graph()
    G.add_edge('A', 'D', weight=1)
    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_size=800, node_color='lightgreen', font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels={('A', 'D'): 'Real-Time'})

    img_io = io.BytesIO()
    plt.savefig(img_io, format='png')
    img_io.seek(0)
    img_data = base64.b64encode(img_io.getvalue()).decode('utf-8')

    return render_template('index.html', path=path, total_time=duration, img_data=img_data)
