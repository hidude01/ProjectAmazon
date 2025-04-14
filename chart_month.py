import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

def plot_sales_month():

    # Conectar a la base de datos SQLite3
    conn = sqlite3.connect('DDBB/amazon.db')
    cursor = conn.cursor()

    # Consulta para obtener los países disponibles
    query_countries = """
    SELECT DISTINCT country
    FROM Qsales
    """
    cursor.execute(query_countries)
    countries = [row[0] for row in cursor.fetchall()]

    # Consulta para obtener los datos de un país específico
    def get_data(country):
        query_data = f"""
        SELECT month, abs(import) as import, Year, Type
        FROM Qsales
        WHERE country = '{country}'
        """
        cursor.execute(query_data)
        return cursor.fetchall()

    # Función para actualizar el gráfico
    def update_graph(country):
        data = get_data(country)

        # Procesar los datos
        months = [str(i).zfill(2) for i in range(1, 13)]
        imports_v_by_year = {}
        imports_c_by_year = {}

        for row in data:
            month, import_value, year, type_value = row
            if type_value == 'V':
                if year not in imports_v_by_year:
                    imports_v_by_year[year] = [0] * 12  # Inicializar lista de 12 meses con ceros
                imports_v_by_year[year][int(month) - 1] += import_value
            elif type_value == 'C':
                if year not in imports_c_by_year:
                    imports_c_by_year[year] = [0] * 12  # Inicializar lista de 12 meses con ceros
                imports_c_by_year[year][int(month) - 1] += import_value

        # Limpiar el gráfico anterior
        ax1.clear()

        # Crear el nuevo gráfico
        width = 0.2  # Ancho de las barras

        for i, (year, imports) in enumerate(imports_v_by_year.items()):
            ax1.bar([int(month) + i * width for month in months], imports, width=width, alpha=0.5, label=f'Type V Year {year}')

        for year, imports in imports_c_by_year.items():
            ax1.plot([int(month) for month in months], imports, label=f'Type C Year {year}')

        # Añadir título y leyenda
        ax1.set_xlabel('Months')
        ax1.set_ylabel('Import', color='b')
        plt.title(f'Import by Month for Country {country}')
        ax1.legend()
        fig.tight_layout()
        canvas.draw()

    # Crear la ventana principal de tkinter
    root = tk.Tk()
    root.title("Import by Month")

    # Crear el gráfico inicial con el primer país disponible
    fig, ax1 = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()

    update_graph(countries[0])

    # Crear el ComboBox para seleccionar el país
    combo = ttk.Combobox(root, values=countries)
    combo.set(countries[0])
    combo.pack()

    # Función para manejar el evento de selección de país
    def country_selected(event):
        update_graph(combo.get())

    combo.bind("<<ComboboxSelected>>", country_selected)

    # Iniciar el bucle principal de tkinter
    root.mainloop()

    # Cerrar la conexión
    conn.close()