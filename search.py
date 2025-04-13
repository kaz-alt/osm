import psycopg2
from config import DB_CONFIG

def find_nearby_pharmacies(lat, lon, radius_m=1000):
    conn = psycopg2.connect(**DB_CONFIG)
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
        LIMIT 20;
    """

    cur.execute(query, (lon, lat, lon, lat, radius_m))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results
