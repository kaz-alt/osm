import os
import pandas as pd

# マージ対象のフォルダパスを指定
folder_path = '/Users/katoukazuya/git/research/kokudo'
output_file = 'japan_address_geo.csv'

# フォルダ内のすべてのCSVファイルを取得
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# CSVファイルを順番に読み込んでマージ
merged_data = pd.DataFrame()
for file in csv_files:
    file_path = os.path.join(folder_path, file)
    data = pd.read_csv(file_path, encoding="cp932")
    merged_data = pd.concat([merged_data, data], ignore_index=True)
    print(f"マージ完了: {file}")

# マージしたデータを新しいCSVファイルに保存
merged_data.to_csv(output_file, index=False)

print(f'Merged {len(csv_files)} CSV files into {output_file}')