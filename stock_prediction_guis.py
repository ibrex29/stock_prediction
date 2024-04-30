import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
import pickle
import yfinance as yf
import numpy as np
import pandas as pd

# Load the trained model from the .pkl file
with open('linear_regression_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Function to predict normalized closing price
def predict_price(df):
    try:
        # Get input values from entry fields
        date_str = entry_date.get()
        open_price = float(entry_open.get())
        high_price = float(entry_high.get())
        low_price = float(entry_low.get())
        close_price = float(entry_close.get())
        adj_close = float(entry_adj_close.get())
        volume = float(entry_volume.get())

        # Validate date format
        date_format = "%Y-%m-%d"
        try:
            datetime.strptime(date_str, date_format)
        except ValueError:
            raise ValueError("Incorrect date format. Please use YYYY-MM-DD.")

        # Calculate the index value corresponding to the date
        date_obj = datetime.strptime(date_str, date_format)
        index_value = (date_obj - df['Date'].min()).days

        # Create feature array for prediction
        features = np.array([[open_price, high_price, low_price, close_price, adj_close, volume]])

        # Predict the normalized closing price using the model
        predicted_normalized_price = model.predict(features)[0]

        # Display the predicted normalized price
        label_result.config(text=f'Predicted Normalized Price: {predicted_normalized_price:.4f}')
    except ValueError as ve:
        messagebox.showerror("Input Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Fetching data from Yahoo Finance
data = yf.download("AAPL", start="2022-01-01", end="2022-12-31")
df = data.reset_index()

# Convert 'Date' column to numeric values representing days since the earliest date
df['Date_numeric'] = (df['Date'] - df['Date'].min()).dt.days

# Create the main Tkinter window
window = tk.Tk()
window.title("Stock Price Prediction")
window.geometry("400x400")

# Create entry fields for user input
label_date = tk.Label(window, text="Date (YYYY-MM-DD):")
label_date.pack()
entry_date = tk.Entry(window)
entry_date.pack()

label_open = tk.Label(window, text="Open Price:")
label_open.pack()
entry_open = tk.Entry(window)
entry_open.pack()

label_high = tk.Label(window, text="High Price:")
label_high.pack()
entry_high = tk.Entry(window)
entry_high.pack()

label_low = tk.Label(window, text="Low Price:")
label_low.pack()
entry_low = tk.Entry(window)
entry_low.pack()

label_close = tk.Label(window, text="Close Price:")
label_close.pack()
entry_close = tk.Entry(window)
entry_close.pack()

label_adj_close = tk.Label(window, text="Adj Close Price:")
label_adj_close.pack()
entry_adj_close = tk.Entry(window)
entry_adj_close.pack()

label_volume = tk.Label(window, text="Volume:")
label_volume.pack()
entry_volume = tk.Entry(window)
entry_volume.pack()

# Create button to trigger prediction
button_predict = tk.Button(window, text="Predict", command=lambda: predict_price(df), height=4)
button_predict.pack()

# Create label to display prediction result
label_result = tk.Label(window, text="")
label_result.pack()

# Add comments to guide users
comment_label = tk.Label(window, text="Please enter the details below and click 'Predict'.")
comment_label.pack()

# Run the Tkinter event loop
window.mainloop()
