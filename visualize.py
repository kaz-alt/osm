import folium
from folium.plugins import MarkerCluster
import csv

def generate_map(result_csv, output_html='pharmacy_map.html', max_points=5000):
    m = folium.Map(location=[35.68, 139.76], zoom_start=6)
    marker_cluster = MarkerCluster().add_to(m)

    with open(result_csv, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i >= max_points:
                break  # 地図を軽く保つために制限
            name = row['pharmacy_name']
            lat = float(row['lat'])
            lon = float(row['lon'])
            dist = row['distance_m']
            address_id = row['address_id']

            folium.Marker(
                location=[lat, lon],
                popup=f"<b>{name}</b><br>住所ID: {address_id}<br>距離: {dist}m",
                icon=folium.Icon(color='blue', icon='plus', prefix='fa')
            ).add_to(marker_cluster)

    m.save(output_html)
    print(f"✅ 地図を保存しました: {output_html}")
