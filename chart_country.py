import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

def plot_sales_country():

    # Conectar a la base de datos SQLite3
    conn = sqlite3.connect('DDBB/amazon.db')
    cursor = conn.cursor()

    # Consulta para obtener los años disponibles
    query_years = """
    SELECT DISTINCT Year
    FROM Qsales
    """
    cursor.execute(query_years)
    years = [str(row[0]) for row in cursor.fetchall()]


    # Consulta para obtener los datos de un año específico
    def get_data(year):
        query_data = f"""
        SELECT country, abs(import) as import, Type
        FROM Qsales
        WHERE Year = {year}
        """
        cursor.execute(query_data)
        return cursor.fetchall()


    # Función para actualizar el gráfico
    def update_graph(year):
        data = get_data(year)

        # Procesar los datos
        countries = []
        import_v = []
        import_c = []

        for row in data:
            country, import_value, type_value = row
            if country not in countries:
                countries.append(country)
                import_v.append(0)
                import_c.append(0)
            index = countries.index(country)
            if type_value == 'V':
                import_v[index] += import_value
            elif type_value == 'C':
                import_c[index] += import_value

        # Limpiar el gráfico anterior
        ax1.clear()

        # Crear el nuevo gráfico
        bars = ax1.bar(countries, import_v, color='b', label='Type V')
        line, = ax1.plot(countries, import_c, color='r', label='Type C')

        # Añadir título y leyenda
        ax1.set_xlabel('Countries')
        ax1.set_ylabel('Import', color='b')
        plt.title(f'Import by Country for Year {year}')
        ax1.legend(handles=[bars, line], labels=['Type V', 'Type C'])
        fig.tight_layout()
        canvas.draw()


    # Crear la ventana principal de tkinter
    root = tk.Tk()
    root.title("Import by Country")

    # Crear el gráfico inicial con el primer año disponible
    fig, ax1 = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()

    update_graph(years[0])

    # Crear el ComboBox para seleccionar el año
    combo = ttk.Combobox(root, values=years)
    combo.set(years[0])
    combo.pack()


    # Función para manejar el evento de selección de año
    def year_selected(event):
        update_graph(combo.get())


    combo.bind("<<ComboboxSelected>>", year_selected)

    # Iniciar el bucle principal de tkinter
    root.mainloop()

    # Cerrar la conexión
    conn.close()