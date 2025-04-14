
import pandas as pd
import sqlite3

from tkinter.filedialog import askopenfilename
from tkinter import messagebox

def read_cost():


    file_path = askopenfilename(title="Select Excel file: Cost", filetypes=[("Excel File", "*.xlsx *.xls")])
    excel_file = pd.ExcelFile(file_path)
    results = []
    year: str
    month: str


    sheet_names = excel_file.sheet_names

    for sheet in sheet_names:
        if "EUR" in sheet:
            data = pd.read_excel(file_path, sheet_name=sheet)
            stop_word = r"Total"

            cols = list(data.columns)
            first_row = data.columns[0]
            prefix = first_row.split(' - ')[0]
            prefix = prefix.split(' ')[0]
            month_year = ' '.join(first_row.split(' ')[-2:])
            month = month_year.split('/')[1]
            year = month_year.split('/')[2].split(')')[0]
            data['Country'] = prefix
            data['Month'] = month
            data['Year'] = year
            index: int
            for index, row in data.iterrows():
                if index >= 2:
                    if stop_word in row.values or data['Country'].iloc[index] == stop_word.upper():
                        #results.append(
                           # (data['Year'].iloc[0], data['Month'].iloc[0], data['Country'].iloc[0], *row.values[:-3], 'C'))

                        break
                    else:
                        results.append(
                            (data['Year'].iloc[0], data['Month'].iloc[0], data['Country'].iloc[0], *row.values[:-3], 'C'))


    try:
        conn = sqlite3.connect('DDBB\\amazon.db')
        cursor = conn.cursor()

        #delete all data if exists

        delete_query = f"DELETE FROM sales WHERE Year = :year AND Month = :month and Type='C';"
        cursor.execute(delete_query,{"year": year, "month": month})


        #insert new data from results
        df_result = pd.DataFrame(results,
                                 columns=['Year', 'Month', 'Country', 'description', 'import', 'iva', 'Total', 'Type'])
        df_result.to_sql("sales", conn, if_exists="append",index=False)
        conn.close()

        messagebox.showinfo(title="Upload Data", message="Cost Data Loaded")

    except Exception as e:
        print(f"An error occurred: {e}")
