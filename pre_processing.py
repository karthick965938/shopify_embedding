import json
from bs4 import BeautifulSoup
import pandas as pd

def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON in file: {file_path}")
        return None

def clean_html_tags(row):
    soup = BeautifulSoup(row["body_html"], "html.parser")
    text = soup.get_text()
    row["body_html"] = text
    return row

def get_img_src(row):
    all_images = []
    for image in row["images"]:
        all_images.append(image["src"])
    row["images_list"] = all_images
    return row

def create_expandend_description(row):
    if row["body_html"] == "" and row["tags"] == "":
        row["expanded_description"] = row["title"]
    elif row["body_html"] == "" and row["tags"] != "":
        row["expanded_description"] = "Title: " + row['title'] + " Tags: " + row['tags']
    elif row["body_html"] != "" and row["tags"] == "":
        row["expanded_description"] = "Title: " + row['title'] + " Description: " +row["body_html"]
    else:
        row["expanded_description"] = "Title: " + row['title'] + " Description: " +row["body_html"] + " Tags: " + row['tags']
    return row

def df_preprocessing(df):
    df = df[df["status"] == "active"]
    df.fillna("", inplace=True)
    df = df.apply(lambda row: get_img_src(row), axis=1)
    df = df.apply(lambda row: create_expandend_description(row), axis=1)
    df = df.apply(lambda row: clean_html_tags(row), axis=1)
    df = df.rename(columns={"body_html": "description"})
    df = df[["id", "title", "handle", "description", "expanded_description", "images_list"]]
    return df

file_path = 'data.json'
json_data = read_json_file(file_path)
all_products = json_data['products']
product_df = pd.DataFrame(all_products)
cleaned_df = df_preprocessing(product_df)

cleaned_df.to_csv("products.csv", index=False)
cleaned_products_json = cleaned_df.to_json(orient="records")
with open("products.json", "w") as f:
    f.write(cleaned_products_json)