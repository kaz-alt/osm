# DBやパスの設定
DB_CONFIG = {
    'dbname': 'osm',
    'user': 'postgres',
    'password': 'password',
    'host': 'localhost',
    'port': '5432'
}

GEOCODE_DICT_PATH = 'data/japan_address_geo.csv'   # 住所 → 緯度経度 辞書
ADDRESS_INPUT = 'data/addresses.csv'
GEO_OUTPUT = 'data/geocoded.csv'
RESULT_OUTPUT = 'data/results.csv'
