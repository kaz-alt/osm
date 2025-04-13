from geocoder import geocode_addresses
from pipeline import run_pipeline
from visualize import generate_map
from config import ADDRESS_INPUT, GEO_OUTPUT, RESULT_OUTPUT

if __name__ == '__main__':
    print("Step 1: ジオコーディング中...")
    geocode_addresses(ADDRESS_INPUT, GEO_OUTPUT)

    print("Step 2: 周辺薬局の検索開始（並列処理）...")
    run_pipeline(processes=8)

    print("Step 3: 地図描画中（代表薬局のみ）...")
    generate_map(RESULT_OUTPUT, output_html='pharmacy_map.html', max_points=5000)

    print("✅ 全処理が完了しました！")
