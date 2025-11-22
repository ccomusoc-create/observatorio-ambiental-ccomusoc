import feedparser
import sqlite3
from datetime import datetime
import os
import matplotlib.pyplot as plt
import pandas as pd

# Temas y feeds RSS de Argentina
RSS_FEEDS = {
    "incendios": "https://news.google.com/rss/search?q=incendio+site:argentina.gob.ar&hl=es-419&gl=AR&ceid=AR:es-419",
    "deforestación": "https://news.google.com/rss/search?q=deforestación+site:argentina.gob.ar&hl=es-419&gl=AR&ceid=AR:es-419",
    "derrames": "https://news.google.com/rss/search?q=derrames+site:argentina.gob.ar&hl=es-419&gl=AR&ceid=AR:es-419",
    "contaminación": "https://news.google.com/rss/search?q=contaminación+site:argentina.gob.ar&hl=es-419&gl=AR&ceid=AR:es-419"
}

DB_FILE = "data/ambiental.db"
CHART_FILE = "charts/picos.png"

def crear_db():
    os.makedirs('data', exist_ok=True)
    os.makedirs('charts', exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS noticias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            tema TEXT,
            titulo TEXT,
            link TEXT UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

def obtener_noticias():
    noticias = []
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    for tema, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)
        for entry in feed.entries:
            titulo = entry.title.replace(',', ' -')
            link = entry.link
            noticias.append([fecha_hoy, tema, titulo, link])
    return noticias

def guardar_db(noticias):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    for fecha, tema, titulo, link in noticias:
        try:
            c.execute('INSERT INTO noticias (fecha, tema, titulo, link) VALUES (?, ?, ?, ?)',
                      (fecha, tema, titulo, link))
        except sqlite3.IntegrityError:
            pass
    conn.commit()
    conn.close()

def generar_grafico():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT fecha, tema, COUNT(*) as cantidad FROM noticias GROUP BY fecha, tema", conn)
    conn.close()

    plt.figure(figsize=(10,5))
    temas = df['tema'].unique()
    for tema in temas:
        df_tema = df[df['tema'] == tema]
        plt.plot(df_tema['fecha'], df_tema['cantidad'], marker='o', label=tema)

    plt.title("Picos de noticias ambientales en Argentina", color='black')
    plt.ylabel("Número de noticias")
    plt.xlabel("Fecha")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(CHART_FILE, facecolor='white')
    plt.close()

def main():
    crear_db()
    noticias = obtener_noticias()
    guardar_db(noticias)
    generar_grafico()
    print("Base de datos actualizada y gráfico de picos generado.")

if __name__ == "__main__":
    main()
