from flask import Flask
import folium

app = Flask(__name__)

@app.route("/")
def map_view():
    # Coordenadas predefinidas
    coords = {
        "MEX": (19.4361, -99.0719),
        "CUN": (21.0365, -86.8771),
        "GDL": (20.5218, -103.3120),
        "MTY": (25.7783, -100.1070),
        "PVR": (20.6800, -105.2530),
        "TIJ": (32.5414, -116.9700),
        "SJD": (23.1516, -109.7210),
        "VER": (19.1457, -96.1870),
        "HUX": (15.7755, -96.2618),
        "OAX": (17.0385, -96.7216),
        "JFK": (40.6413, -73.7781),
        "LAX": (33.9416, -118.4085),
        "MIA": (25.7959, -80.2871),
    }

    import pandas as pd
    from collections import defaultdict

    df = pd.read_excel("Total_vuelos_por_ruta_XA-VIR.xlsx", sheet_name="Hoja 1")
    df["Ruta"] = df["Ruta"].str.strip()
    df["Cantidad de vuelos"] = pd.to_numeric(df["Cantidad de vuelos"], errors="coerce").fillna(0)

    totales_ciudad = defaultdict(int)
    for _, row in df.iterrows():
        try:
            origen, destino = [x.strip() for x in row["Ruta"].split("-")]
        except ValueError:
            continue
        vuelos = int(row["Cantidad de vuelos"])
        totales_ciudad[origen] += vuelos
        totales_ciudad[destino] += vuelos

    mapa = folium.Map(location=[23.0, -100.0], zoom_start=4, tiles="cartodbpositron")

    for _, row in df.iterrows():
        try:
            origen, destino = [x.strip() for x in row["Ruta"].split("-")]
        except ValueError:
            continue
        vuelos = row["Cantidad de vuelos"]
        if origen in coords and destino in coords:
            line_coords = [coords[origen], coords[destino]]
            folium.PolyLine(
                locations=line_coords,
                color="darkgreen",
                weight=4,
                opacity=0.8,
                tooltip=str(int(vuelos))
            ).add_to(mapa)

    for ciudad, total in totales_ciudad.items():
        if ciudad in coords:
            folium.CircleMarker(
                location=coords[ciudad],
                radius=8,
                fill=True,
                color="blue",
                fill_opacity=0.7,
                popup=f"{ciudad}: {total} vuelos"
            ).add_to(mapa)
            folium.Marker(
                location=coords[ciudad],
                icon=folium.DivIcon(html=f"<div style='font-size:10px'>{ciudad}</div>")
            ).add_to(mapa)

    mapa.save("templates/mapa.html")
    return open("templates/mapa.html").read()