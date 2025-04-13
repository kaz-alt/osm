import csv
from config import GEOCODE_DICT_PATH

# 住所から緯度経度を取得（オフライン辞書）
def load_geocode_dict():
    geocode_map = {}
    with open(GEOCODE_DICT_PATH, encoding='utf-8') as f:
        for row in csv.DictReader(f):
            address = row['都道府県名'] + row['市区町村名'] + row['大字町丁目名']
            geocode_map[address] = (float(row['緯度']), float(row['経度']))
    return geocode_map

def geocode_addresses(address_file, output_file):
    geo_dict = load_geocode_dict()
    with open(address_file, encoding='utf-8') as fin, open(output_file, 'w', newline='', encoding='utf-8') as fout:
        reader = csv.DictReader(fin)
        writer = csv.DictWriter(fout, fieldnames=['id', 'address', 'lat', 'lon'])
        writer.writeheader()
        for row in reader:
            addr = row['address']
            if addr in geo_dict:
                lat, lon = geo_dict[addr]
                writer.writerow({'id': row['id'], 'address': addr, 'lat': lat, 'lon': lon})
