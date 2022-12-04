import pandas as pd
data = pd.read_csv("clean_data.csv")

def search(in_str, data):
    in_str = in_str.lower()
    df_id = list(data[(data['identifier'].str.contains(in_str, case=False)) | (data['title'].str.contains(in_str, case=False)) | (data['description'].str.contains(in_str, case=False))].identifier)
    return df_id

print(search("big data", data))