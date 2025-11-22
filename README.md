# Observatorio Ambiental - CCOMUSOC

Este proyecto automatiza la recolección de noticias ambientales de Argentina (incendios, deforestación, derrames, contaminación) usando RSS de Google News.  

- Noticias se guardan en base de datos SQLite (`data/ambiental.db`)  
- Se genera un CSV actualizado para la web (`data/ambiental.csv`)  
- Se genera un gráfico de picos por tema (`charts/picos.png`)  
- Página web: `index.html` muestra últimas noticias y gráfico  
- GitHub Actions actualiza todo automáticamente cada día
