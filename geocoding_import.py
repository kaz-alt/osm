import csv
import psycopg2

# 接続設定（適宜変更）
conn = psycopg2.connect(
    dbname="osm",
    user="postgres",
    password="password",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# テーブル作成
cur.execute('DROP TABLE IF EXISTS address_geo')
cur.execute('''
    CREATE TABLE address_geo (
        zipcode TEXT,
        address TEXT,
        lat DOUBLE PRECISION,
        lon DOUBLE PRECISION
    )
''')

# インデックス（検索高速化用）
cur.execute('CREATE INDEX idx_address ON address_geo(address)')

# 国土地理院データの読み込み
print("Loading geolocation data...")
geo_dict = {}

with open("japan_address_geo.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = row["都道府県名"] + row["市区町村名"] + row["大字町丁目名"]
        geo_dict[key] = (float(row["緯度"]), float(row["経度"]))

# 郵便番号データ（日本郵便）の処理
print("Processing postal data...")
with open("utf_ken_all.csv", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        zipcode = row[2]
        pref = row[6]
        city = row[7]
        town = row[8].replace("（", "").replace("）", "")
        address = pref + city + town

        if address in geo_dict:
            lat, lon = geo_dict[address]
            cur.execute('''
                INSERT INTO address_geo (zipcode, address, lat, lon)
                VALUES (%s, %s, %s, %s)
            ''', (zipcode, address, lat, lon))

# コミット・終了処理
conn.commit()
cur.close()
conn.close()
print("PostgreSQLへのインポート完了 ✅")
