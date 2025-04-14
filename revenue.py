import sqlite3
import tkinter as tk
from tkinter import ttk

def revenue_table():
    # Conectar a la base de datos SQLite3
    conn = sqlite3.connect('DDBB/amazon.db')
    cursor = conn.cursor()

    # Consulta para obtener los países y años disponibles
    query_countries_years = """
    SELECT DISTINCT country, Year
    FROM Qsales
    """
    cursor.execute(query_countries_years)
    data = cursor.fetchall()

    countries = sorted(set(row[0] for row in data))
    years = sorted(set(row[1] for row in data))

    # Consulta para obtener los datos de un país y año específicos
    def get_data(country, year):
        query_data = f"""
        SELECT Type, abs(import) as import
        FROM Qsales
        WHERE country = '{country}' AND Year = {year}
        """
        cursor.execute(query_data)
        return cursor.fetchall()

    # Crear la ventana principal de tkinter
    root = tk.Tk()
    root.title("Import Data Grid")

    # Crear el Treeview para mostrar la cuadrícula
    columns = ["Country"]
    columns.extend([f"{year}_V" for year in years])
    columns.extend([f"{year}_C" for year in years])
    columns.extend([f"{year}_BFO" for year in years])

    tree = ttk.Treeview(root, columns=columns, show='headings')

    # Configurar las columnas
    tree.heading("Country", text="Country")
    for year in years:
        tree.heading(f"{year}_V", text=f"{year} V")
    for year in years:
        tree.heading(f"{year}_C", text=f"{year} C")
    for year in years:
        tree.heading(f"{year}_BFO", text=f"{year} BFO")

    # Ajustar las columnas a la derecha
    for col in columns[1:]:
        tree.column(col, anchor=tk.E)

    # Añadir los datos al Treeview
    for country in countries:
        values = [country]
        for year in years:
            data = get_data(country, year)
            v_value = sum(row[1] for row in data if row[0] == 'V')
            values.append(f"€{v_value:.2f}")
        for year in years:
            data = get_data(country, year)
            c_value = sum(row[1] for row in data if row[0] == 'C')
            values.append(f"€{c_value:.2f}")
        for year in years:
            data = get_data(country, year)
            v_value = sum(row[1] for row in data if row[0] == 'V')
            c_value = sum(row[1] for row in data if row[0] == 'C')
            bfo_value = v_value - c_value
            values.append(f"€{bfo_value:.2f}")
        tree.insert("", "end", values=values)

    tree.pack(fill=tk.BOTH, expand=True)

    # Iniciar el bucle principal de tkinter
    root.mainloop()

    # Cerrar la conexión
    conn.close()
