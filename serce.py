import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt


# Database Functions
def create_table():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS patients
                 (login TEXT, password TEXT, pump_name TEXT, F REAL, P REAL, n REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS patient_data
                 (login TEXT, hgb REAL, hct REAL, fhb REAL, ldh REAL, gluco REAL, inr REAL, crp REAL,
                 temperature REAL, body_weight REAL, sdp REAL, ddp REAL, map REAL)''')
    conn.commit()
    conn.close()


def register_user():
    login = login_entry.get()
    password = password_entry.get()
    pump_name = pump_name_entry.get()
    F = F_entry.get()
    P = P_entry.get()
    n = n_entry.get()

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO patients VALUES (?, ?, ?, ?, ?, ?)", (login, password, pump_name, F, P, n))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Registration successful!")


def login_user():
    login = login_entry.get()
    password = password_entry.get()

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM patients WHERE login=? AND password=?", (login, password))
    user = c.fetchone()
    conn.close()

    if user:
        login_window.withdraw()
        main_window()
    else:
        messagebox.showerror("Error", "Invalid login or password")


# GUI Functions
def main_window():
    def save_data():
        # Get patient inputs
        hgb = hgb_entry.get()
        hct = hct_entry.get()
        fhb = fhb_entry.get()
        ldh = ldh_entry.get()
        gluco = gluco_entry.get()
        inr = inr_entry.get()
        crp = crp_entry.get()

        temperature = temperature_entry.get()
        body_weight = body_weight_entry.get()
        sdp = sdp_entry.get()
        ddp = ddp_entry.get()
        map_ = map_entry.get()

        # Save data to database
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO patient_data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (login_entry.get(), hgb, hct, fhb, ldh, gluco, inr, crp, temperature, body_weight, sdp, ddp, map_))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Data saved successfully!")

    def visualize_data():
        # Retrieve patient data from database
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM patient_data WHERE login=?", (login_entry.get(),))
        data = c.fetchall()
        conn.close()

        # Prepare data for plotting
        x_values = []
        y_values = []
        for row in data:
            x_values.append(row[8])  # Temperature
            y_values.append(row[11])  # MAP

        # Plotting
        plt.plot(x_values, y_values)
        plt.xlabel('Temperature (°C)')
        plt.ylabel('Mean Arterial Pressure (mmHg)')
        plt.title('Patient Data Visualization')
        plt.show()

    main_window = tk.Toplevel()
    main_window.title("Patient Data")
    main_window.geometry("400x400")

    hgb_label = tk.Label(main_window, text="HGB (hemoglobin):")
    hgb_label.pack()
    hgb_entry = tk.Entry(main_window)
    hgb_entry.pack()

    hct_label = tk.Label(main_window, text="HCT (hematocrit):")
    hct_label.pack()
    hct_entry = tk.Entry(main_window)
    hct_entry.pack()

    fhb_label = tk.Label(main_window, text="fHB (hemoglobin fraction):")
    fhb_label.pack()
    fhb_entry = tk.Entry(main_window)
    fhb_entry.pack()

    ldh_label = tk.Label(main_window, text="LDH (lactate dehydrogenase):")
    ldh_label.pack()
    ldh_entry = tk.Entry(main_window)
    ldh_entry.pack()

    gluco_label = tk.Label(main_window, text="GLUCO (glucose):")
    gluco_label.pack()
    gluco_entry = tk.Entry(main_window)
    gluco_entry.pack()

    inr_label = tk.Label(main_window, text="INR (international rate):")
    inr_label.pack()
    inr_entry = tk.Entry(main_window)
    inr_entry.pack()

    crp_label = tk.Label(main_window, text="CRP (C-reactive protein):")
    crp_label.pack()
    crp_entry = tk.Entry(main_window)
    crp_entry.pack()

    temperature_label = tk.Label(main_window, text="Temperature:")
    temperature_label.pack()
    temperature_entry = tk.Entry(main_window)
    temperature_entry.pack()

    body_weight_label = tk.Label(main_window, text="Body Weight:")
    body_weight_label.pack()
    body_weight_entry = tk.Entry(main_window)
    body_weight_entry.pack()

    sdp_label = tk.Label(main_window, text="SDP (Systolic Blood Pressure):")
    sdp_label.pack()
    sdp_entry = tk.Entry(main_window)
    sdp_entry.pack()

    ddp_label = tk.Label(main_window, text="DDP (diastolic blood pressure):")
    ddp_label.pack()
    ddp_entry = tk.Entry(main_window)
    ddp_entry.pack()

    map_label = tk.Label(main_window, text="MAP (mean arterial pressure):")
    map_label.pack()
    map_entry = tk.Entry(main_window)
    map_entry.pack()

    save_button = tk.Button(main_window, text="Save", command=save_data)
    save_button.pack()

    visualize_button = tk.Button(main_window, text="Visualize", command=visualize_data)
    visualize_button.pack()


# Login Window
login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("300x150")

login_label = tk.Label(login_window, text="Login:")
login_label.pack()
login_entry = tk.Entry(login_window)
login_entry.pack()

password_label = tk.Label(login_window, text="Password:")
password_label.pack()
password_entry = tk.Entry(login_window, show="*")
password_entry.pack()

pump_name_label = tk.Label(login_window, text="Pump Name:")
pump_name_label.pack()
pump_name_entry = tk.Entry(login_window)
pump_name_entry.pack()

F_label = tk.Label(login_window, text="F (driving force):")
F_label.pack()
F_entry = tk.Entry(login_window)
F_entry.pack()

P_label = tk.Label(login_window, text="P (blood pressure):")
P_label.pack()
P_entry = tk.Entry(login_window)
P_entry.pack()

n_label = tk.Label(login_window, text="n (flow rate):")
n_label.pack()
n_entry = tk.Entry(login_window)
n_entry.pack()

login_button = tk.Button(login_window, text="Login", command=login_user)
login_button.pack()

register_button = tk.Button(login_window, text="Register", command=register_user)
register_button.pack()

create_table()

login_window.mainloop()
