import psycopg2
import folium

def find_nearby_pharmacies_osm(lat, lon, radius_m=1000):
    conn = psycopg2.connect(
        dbname="osm",
        user="postgres",
        password="password",
        host="localhost",  # docker-compose のサービス名でも可
        port="5432"
    )
    cur = conn.cursor()

    query = """
        SELECT
            name,
            ST_Y(ST_Transform(way, 4326)) AS lat,
            ST_X(ST_Transform(way, 4326)) AS lon,
            ST_Distance(
                ST_Transform(way, 4326)::geography,
                ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography
            ) AS distance_m
        FROM planet_osm_point
        WHERE (
            amenity = 'pharmacy' OR shop = 'chemist'
        )
        AND ST_DWithin(
            ST_Transform(way, 4326)::geography,
            ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography,
            %s
        )
        ORDER BY distance_m
        LIMIT 50;
    """

    cur.execute(query, (lon, lat, lon, lat, radius_m))
    results = cur.fetchall()

    cur.close()
    conn.close()
    return results

latitude = 35.757149
longitude = 139.79809
results = find_nearby_pharmacies_osm(latitude, longitude)

for name, lat, lon, dist in results:
    print(f"{name or '名称なし'}（{lat}, {lon}）→ 約{int(dist)}m")

# 🗺️ 地図の初期化
m = folium.Map(location=[latitude, longitude], zoom_start=15)

# 🔵 中心点（検索元）
folium.Marker(
    [latitude, longitude],
    popup="検索中心",
    icon=folium.Icon(color="blue", icon="search")
).add_to(m)

# 🏥 検出された薬局をマップに追加
for name, lat, lon, dist in results:
    folium.Marker(
        [lat, lon],
        popup=f"{name or '名称なし'}<br>{int(dist)}m",
        icon=folium.Icon(color="red", icon="plus-sign")
    ).add_to(m)

# ⭕ 検索範囲（半径2km）の円を描画
folium.Circle(
    location=[latitude, longitude],
    radius=1000,
    color='green',
    fill=True,
    fill_opacity=0.05
).add_to(m)

# 💾 地図をHTMLとして保存
m.save("pharmacies_map.html")
print("マップを pharmacies_map.html として保存しました ✅")
