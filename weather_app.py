import tkinter as tk
import requests

# Create the main window
root = tk.Tk()
root.title("Weather Forecast App - Final Project")
root.geometry("500x300")
root.config(bg="#f0f0f0")  # Set background color

# Create a frame for the input area
input_frame = tk.Frame(root, bg="#f0f0f0")
input_frame.pack() 

# Create and place widgets
city_label = tk.Label(input_frame, text="Location:", bg="#f0f0f0", font=("Arial", 12))
city_label.pack(side=tk.LEFT, pady=20, padx=20, anchor="e")

city_entry = tk.Entry(input_frame, width=20, font=("Arial", 12))
city_entry.pack(side=tk.LEFT, padx=5)

search_button = tk.Button(input_frame, text="Search", command=lambda: search_weather(), 
                          bg="#007BFF", fg="black", font=("Arial", 12))
search_button.pack(side=tk.LEFT, padx=5)

result_label = tk.Label(root, text="", justify=tk.LEFT, bg="#f0f0f0", font=("Arial", 14, "bold"))
result_label.pack(pady=(20, 10), padx=20)  # Add top padding and bottom padding

# Define the search action
def search_weather():
    city = city_entry.get().split(',')[0].strip()  # Take only the city name
    api_key = "e5b87468cb09cb842d8a4cbb9848a544"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad responses
        
        data = response.json()
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        pressure = data['main']['pressure']
        precipitation = data['clouds']['all'] 
        
        result_label.config(text=(
            f"Weather in {city}:\n\n"
            f"Temperature: {temperature:.1f}°C\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed:.1f} m/s\n"
            f"Pressure: {pressure} hPa\n"
            f"Precipitation: {precipitation}%"  
        ))
    except requests.exceptions.RequestException as e:
        result_label.config(text=f"Error fetching weather data: {e}")

# Start the GUI event loop
root.mainloop()
