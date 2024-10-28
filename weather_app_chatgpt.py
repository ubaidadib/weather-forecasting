import tkinter as tk
from tkinter import messagebox, ttk
import requests
import os

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Forecast App")
        self.root.geometry("500x300")
        self.root.config(bg="#f0f0f0")  # Set background color

        self.api_key = os.getenv("e5b87468cb09cb842d8a4cbb9848a544", "e5b87468cb09cb842d8a4cbb9848a544")  # Replace with your actual API key
        self.create_widgets()
        self.units = "metric"  # Default units

    def create_widgets(self):
        """Creates and arranges the input and result widgets."""
        input_frame = tk.Frame(self.root, bg="#f0f0f0")
        input_frame.pack(pady=20)

        city_label = tk.Label(input_frame, text="Location:", bg="#f0f0f0", font=("Arial", 12))
        city_label.pack(side=tk.LEFT, padx=(20, 5))

        self.city_entry = tk.Entry(input_frame, width=20, font=("Arial", 12))
        self.city_entry.pack(side=tk.LEFT, padx=5)

        self.unit_var = tk.StringVar(value="metric")
        metric_radio = tk.Radiobutton(input_frame, text="Celsius", variable=self.unit_var, value="metric", bg="#f0f0f0")
        imperial_radio = tk.Radiobutton(input_frame, text="Fahrenheit", variable=self.unit_var, value="imperial", bg="#f0f0f0")
        metric_radio.pack(side=tk.LEFT)
        imperial_radio.pack(side=tk.LEFT)

        search_button = tk.Button(
            input_frame,
            text="Search",
            command=self.search_weather,
            bg="#007BFF",
            fg="black",
            font=("Arial", 12)
        )
        search_button.pack(side=tk.LEFT, padx=(5, 20))

        self.result_label = tk.Label(
            self.root,
            text="",
            justify=tk.LEFT,
            bg="#f0f0f0",
            font=("Arial", 14, "bold")
        )
        self.result_label.pack(pady=(10, 20), padx=20)

    def search_weather(self):
        """Fetches weather data for the entered city and updates the result label."""
        city = self.city_entry.get().split(',')[0].strip()  # Take only the city name
        if not city:
            messagebox.showwarning("Input Error", "Please enter a valid city name.")
            return

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units={self.unit_var.get()}"

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad responses
            
            data = response.json()
            self.update_result_label(data, city)
        except requests.exceptions.HTTPError as http_err:
            messagebox.showerror("HTTP Error", f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as req_err:
            messagebox.showerror("Request Error", f"Error fetching weather data: {req_err}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def update_result_label(self, data, city):
        """Updates the result label with weather information."""
        try:
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            pressure = data['main']['pressure']
            precipitation = data['clouds']['all']

            # Prepare the result text
            unit_symbol = "°C" if self.unit_var.get() == "metric" else "°F"
            self.result_label.config(text=(
                f"Weather in {city}:\n\n"
                f"Temperature: {temperature:.1f}{unit_symbol}\n"
                f"Humidity: {humidity}%\n"
                f"Wind Speed: {wind_speed:.1f} m/s\n"
                f"Pressure: {pressure} hPa\n"
                f"Precipitation: {precipitation}%"
            ))
        except KeyError:
            messagebox.showerror("Data Error", "Could not retrieve weather data. Please check the city name.")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
