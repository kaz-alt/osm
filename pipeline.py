import csv
from multiprocessing import Pool
from search import find_nearby_pharmacies
from config import GEO_OUTPUT, RESULT_OUTPUT

def process_row(row):
    id_, lat, lon = row['id'], float(row['lat']), float(row['lon'])
    pharmacies = find_nearby_pharmacies(lat, lon)
    return [(id_, name or '', p_lat, p_lon, int(dist)) for name, p_lat, p_lon, dist in pharmacies]

def run_pipeline(processes=8):
    with open(GEO_OUTPUT, encoding='utf-8') as fin, open(RESULT_OUTPUT, 'w', newline='', encoding='utf-8') as fout:
        reader = csv.DictReader(fin)
        writer = csv.writer(fout)
        writer.writerow(['address_id', 'pharmacy_name', 'lat', 'lon', 'distance_m'])

        with Pool(processes=processes) as pool:
            for result_batch in pool.imap(process_row, reader, chunksize=100):
                for result in result_batch:
                    writer.writerow(result)
