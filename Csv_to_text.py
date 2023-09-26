import pandas as pd
import os
import csv
import shutil

def csv_totxt():
    # Load the CSV file into a DataFrame
    csv_file = "youtube_comments.csv"  # Replace with your CSV file path
    column_name = "Comment"              # Replace with the column containing text data

    # Specify the encoding as 'latin1'
    df = pd.read_csv(csv_file, encoding='latin1')
    sel=df.head(1000)


    # Create a directory to store the text files
    if  os.path.exists("t"):
        shutil.rmtree("t")
        
    os.makedirs("t")
    # Iterate through the rows and create individual text files
    for index, row in sel.iterrows():
        text_data = row[column_name]
        
        # Create a unique filename for the text file (e.g., text_1.txt, text_2.txt)
        filename = f"text_{index + 1}.txt"
        
        # Write the text data to the text file
        with open(os.path.join("t", filename), "w+", encoding="utf-8") as file:
            file.write(text_data)
