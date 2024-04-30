import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import CENTER
from datetime import datetime
import pickle
import yfinance as yf
import numpy as np
import pandas as pd

def predict_price(df, entry_date, entry_open, entry_high, entry_low, entry_close, entry_adj_close, entry_volume, label_result):
    try:
        # Get input values from entry fields
        open_price = float(entry_open.get())
        high_price = float(entry_high.get())
        low_price = float(entry_low.get())
        close_price = float(entry_close.get())
        adj_close = float(entry_adj_close.get())
        volume = float(entry_volume.get())

        # Calculate the index value corresponding to the date
        date_str = entry_date.get()
        date_format = "%Y-%m-%d"
        date_obj = datetime.strptime(date_str, date_format)
        index_value = (date_obj - df['Date'].min()).days

        # Create feature array for prediction
        features = np.array([[index_value, open_price, high_price, low_price, close_price, adj_close, volume]])

        # Predict the normalized closing price using the model
        predicted_normalized_price = model.predict(features)[0]

        # Convert normalized price back to actual price
        actual_predicted_price = predicted_normalized_price * (df['Close'].max() - df['Close'].min()) + df['Close'].min()

        # Display the predicted actual price
        label_result.config(text=f'Predicted Price: {actual_predicted_price:.2f} USD')
    except ValueError as ve:
        messagebox.showerror("Input Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def validate_login(entry_username, entry_password, login_window):
    username = entry_username.get()
    password = entry_password.get()

    # Check if the username and password are correct
    if username == "admin" and password == "password":
        messagebox.showinfo("Login Successful", "Welcome, admin!")
        login_window.destroy()
        show_prediction_page()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def show_prediction_page():
    prediction_window = tk.Tk()
    prediction_window.title("Stock Price Prediction")
    prediction_window.attributes('-fullscreen', True)

    prediction_frame = tk.Frame(prediction_window)

    # Create header
    header_label = tk.Label(prediction_frame, text="Stock Price Prediction", font=("Helvetica", 24))
    header_label.pack(pady=20)

    # Create entry fields for user input
    label_date = tk.Label(prediction_frame, text="Date (YYYY-MM-DD):")
    label_date.pack()
    entry_date = tk.Entry(prediction_frame)
    entry_date.pack()

    label_open = tk.Label(prediction_frame, text="Open Price:")
    label_open.pack()
    entry_open = tk.Entry(prediction_frame)
    entry_open.pack()

    label_high = tk.Label(prediction_frame, text="High Price:")
    label_high.pack()
    entry_high = tk.Entry(prediction_frame)
    entry_high.pack()

    label_low = tk.Label(prediction_frame, text="Low Price:")
    label_low.pack()
    entry_low = tk.Entry(prediction_frame)
    entry_low.pack()

    label_close = tk.Label(prediction_frame, text="Close Price:")
    label_close.pack()
    entry_close = tk.Entry(prediction_frame)
    entry_close.pack()

    label_adj_close = tk.Label(prediction_frame, text="Adj Close Price:")
    label_adj_close.pack()
    entry_adj_close = tk.Entry(prediction_frame)
    entry_adj_close.pack()

    label_volume = tk.Label(prediction_frame, text="Volume:")
    label_volume.pack()
    entry_volume = tk.Entry(prediction_frame)
    entry_volume.pack()

    # Create button to trigger prediction
    button_predict = tk.Button(prediction_frame, text="Predict", command=lambda: predict_price(df, entry_date, entry_open, entry_high, entry_low, entry_close, entry_adj_close, entry_volume, label_result))
    button_predict.pack(pady=10)

    # Create label to display prediction result
    label_result = tk.Label(prediction_frame, text="")
    label_result.pack()

    # Create note
    note_label = tk.Label(prediction_frame, text="Note: Please enter the details below and click 'Predict'.", font=("Helvetica", 10), fg="gray")
    note_label.pack()

    # Create exit button
    exit_button = tk.Button(prediction_frame, text="Exit", command=lambda: exit_app(prediction_window))
    exit_button.pack(pady=10)

    prediction_frame.pack()

def exit_app(window):
    result = messagebox.askquestion("Exit", "Are you sure you want to exit?")
    if result == "yes":
        window.destroy()

# Load the trained model from the .pkl file
with open('linear_regression_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Fetching data from Yahoo Finance
data = yf.download("AAPL", start="2022-01-01", end="2022-12-31")
df = data.reset_index()

# Create the main Tkinter window for login
login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("300x150")

# Create entry fields for username and password
label_username = ttk.Label(login_window, text="Username:")
label_username.pack()
entry_username = ttk.Entry(login_window)
entry_username.pack()

label_password = ttk.Label(login_window, text="Password:")
label_password.pack()
entry_password = ttk.Entry(login_window, show="*")
entry_password.pack()

# Create login button
login_button = ttk.Button(login_window, text="Login", command=lambda: validate_login(entry_username, entry_password, login_window))
login_button.pack()

# Run the Tkinter event loop for the login window
login_window.mainloop()
