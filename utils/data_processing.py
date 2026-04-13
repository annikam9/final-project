import pandas as pd

defenders = pd.read_csv('utils/defenders_data.csv', sep=",", encoding='utf-8-sig', encoding_errors='replace')
oc21 = pd.read_csv('utils/oc_index2021.csv', sep=";", encoding='latin-1', on_bad_lines='skip')
oc23 = pd.read_csv('utils/oc_index2023.csv', sep=";", encoding='latin-1', on_bad_lines='skip')
oc25 = pd.read_csv('utils/oc_index2025.csv', sep=";", encoding='latin-1', on_bad_lines='skip')

oc21.columns = oc21.columns.str.strip().str.lower()
oc23.columns = oc23.columns.str.strip().str.lower()
oc25.columns = oc25.columns.str.strip().str.lower()

print(oc21.columns.tolist())  # sollte jetzt einzelne Spalten zeigen

oc_combined = oc21.merge(oc23, on="country", suffixes=('_2021', '_2023')).merge(oc25, on="country", suffixes=('', '_2025'))

print(oc_combined.shape)
print(oc_combined.head())