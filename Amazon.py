import tkinter as tk
from tkinter import ttk
from cost import read_cost
from sales import read_sales
from chart_month import plot_sales_month
from chart_country import plot_sales_country
from revenue import revenue_table

def generate_chart(option):
    if option == "Month":
        plot_sales_month()
    elif option == "Country":
        plot_sales_country()
    elif option == "Revenue":
        revenue_table()

app = tk.Tk()
app.title("Amazon Sales")

# Set Window size and back Color
app.geometry("400x300")
app.configure(bg="#f0f0f0")

# Frame Where I added the buttons and the dropdown
frame = tk.Frame(app, bg="#f0f0f0")
frame.pack(pady=20)

# Cost Button
cost_button = tk.Button(frame, text="Load Cost File", command=read_cost, bg="#4CAF50", fg="white", font=("Arial", 12))
cost_button.grid(row=0, column=0, padx=10, pady=10)

# Sales Button
sales_button = tk.Button(frame, text="Load Sales File", command=read_sales, bg="#4CAF50", fg="white", font=("Arial", 12))
sales_button.grid(row=0, column=1, padx=10, pady=10)

# graphical output dropdown menu
options = ["Month", "Country", "Revenue"]
selected_option = tk.StringVar()
dropdown = ttk.Combobox(frame, textvariable=selected_option, values=options, font=("Arial", 12))
dropdown.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Button to create the graphics or the grid depending on dropdown menu
generate_button = tk.Button(frame, text="Create Graphic/Table", command=lambda: generate_chart(selected_option.get()), bg="#008CBA", fg="white", font=("Arial", 12))
generate_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

app.mainloop()
