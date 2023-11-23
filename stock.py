import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def fetch_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

def calculate_technical_indicators(stock_data):
    # Calculate daily returns
    stock_data['Daily_Return'] = stock_data['Adj Close'].pct_change()

    # Calculate cumulative returns
    stock_data['Cumulative_Return'] = (1 + stock_data['Daily_Return']).cumprod() - 1

    # Calculate moving average
    stock_data['50_MA'] = stock_data['Adj Close'].rolling(window=50).mean()

    # Calculate Relative Strength Index (RSI)
    delta = stock_data['Adj Close'].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    stock_data['RSI'] = rsi

    # Calculate Moving Average Convergence Divergence (MACD)
    short_window = 12
    long_window = 26

    short_ema = stock_data['Adj Close'].ewm(span=short_window, adjust=False).mean()
    long_ema = stock_data['Adj Close'].ewm(span=long_window, adjust=False).mean()

    stock_data['MACD'] = short_ema - long_ema
    stock_data['Signal_Line'] = stock_data['MACD'].ewm(span=9, adjust=False).mean()

    return stock_data

def visualize_stock_data(stock_data):
    plt.figure(figsize=(12, 6))

    # Plotting stock prices and moving average
    plt.subplot(2, 1, 1)
    plt.plot(stock_data['Adj Close'], label='Adjusted Close Price')
    plt.plot(stock_data['50_MA'], label='50-Day Moving Average', linestyle='--', color='orange')
    plt.title('Stock Prices and 50-Day Moving Average')
    plt.legend()

    # Plotting cumulative returns
    plt.subplot(2, 1, 2)
    plt.plot(stock_data['Cumulative_Return'], label='Cumulative Returns', color='green')
    plt.title('Cumulative Returns')
    plt.legend()

    # Show the plots
    plt.tight_layout()
    plt.show()

def visualize_technical_indicators(stock_data):
    plt.figure(figsize=(12, 8))

    # Plotting RSI
    plt.subplot(3, 1, 1)
    plt.plot(stock_data['RSI'], label='RSI', color='blue')
    plt.axhline(70, color='red', linestyle='--', label='Overbought (70)')
    plt.axhline(30, color='green', linestyle='--', label='Oversold (30)')
    plt.title('Relative Strength Index (RSI)')
    plt.legend()

    # Plotting MACD and Signal Line
    plt.subplot(3, 1, 2)
    plt.plot(stock_data['MACD'], label='MACD', color='purple')
    plt.plot(stock_data['Signal_Line'], label='Signal Line', linestyle='--', color='orange')
    plt.title('Moving Average Convergence Divergence (MACD)')
    plt.legend()

    # Plotting stock prices
    plt.subplot(3, 1, 3)
    plt.plot(stock_data['Adj Close'], label='Adjusted Close Price')
    plt.title('Stock Prices')
    plt.legend()

    # Show the plots
    plt.tight_layout()
    plt.show()

class StockAnalysisApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Stock Analysis Tool")

        # Create and set up widgets
        self.create_widgets()

    def create_widgets(self):
        # Label and Entry for stock symbol
        self.label_stock_symbol = ttk.Label(self.master, text="Stock Symbol:")
        self.label_stock_symbol.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        self.entry_stock_symbol = ttk.Entry(self.master)
        self.entry_stock_symbol.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        # Label and Entry for start date
        self.label_start_date = ttk.Label(self.master, text="Start Date (YYYY-MM-DD):")
        self.label_start_date.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        self.entry_start_date = ttk.Entry(self.master)
        self.entry_start_date.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

        # Label and Entry for end date
        self.label_end_date = ttk.Label(self.master, text="End Date (YYYY-MM-DD):")
        self.label_end_date.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

        self.entry_end_date = ttk.Entry(self.master)
        self.entry_end_date.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

        # Button to fetch and analyze data
        self.button_analyze = ttk.Button(self.master, text="Fetch and Analyze", command=self.fetch_and_analyze)
        self.button_analyze.grid(row=3, column=0, columnspan=2, pady=10)

        # Checkbox to choose analysis options
        self.check_var_rsi = tk.IntVar()
        self.check_var_macd = tk.IntVar()

        self.checkbutton_rsi = ttk.Checkbutton(self.master, text="Include RSI", variable=self.check_var_rsi)
        self.checkbutton_macd = ttk.Checkbutton(self.master, text="Include MACD", variable=self.check_var_macd)

        self.checkbutton_rsi.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
        self.checkbutton_macd.grid(row=4, column=1, padx=10, pady=5, sticky=tk.W)

        # Frame to display Matplotlib plots
        self.frame_plots = ttk.Frame(self.master)
        self.frame_plots.grid(row=5, column=0, columnspan=2, pady=10)

    def fetch_and_analyze(self):
        stock_symbol = self.entry_stock_symbol.get()
        start_date = self.entry_start_date.get()
        end_date = self.entry_end_date.get()

        # Fetch stock data
        stock_data = fetch_stock_data(stock_symbol, start_date, end_date)

        # Analyze stock data
        stock_data = calculate_technical_indicators(stock_data)

        # Visualize the results
        self.display_plots(stock_data)

        # Print stock data to console for verification
        print(stock_data)

    def display_plots(self, stock_data):
        # Clear any existing plots
        for widget in self.frame_plots.winfo_children():
            widget.destroy()

        # Choose which plots to display based on user selections
        if self.check_var_rsi.get():
            visualize_technical_indicators(stock_data)
        else:
            visualize_stock_data(stock_data)

        # Embed Matplotlib figure in Tkinter window
        canvas = FigureCanvasTkAgg(plt.gcf(), master=self.frame_plots)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def main():
    root = tk.Tk()
    app = StockAnalysisApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
