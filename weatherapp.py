import tkinter as tk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap

#create function to get weather infomation from api
def get_weather(city):
    API_key = "d670f9bbbd64db680ba5be8b982816b3"
    url =f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    res = requests.get(url)

    if res.status_code == 404:
        messagebox.showerror("ERROR", "City not found!!")
        return None
    #respone JSON get weather information
    weather = res.json()
    icon_id = weather['weather'][0]['icon']
    temperature = weather['main']['temp'] - 273.15
    description = weather['weather'][0]['description']
    city = weather['name']
    country = weather['sys']['country']

    #get icon url and return all weather information
    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
    return (icon_url, temperature, description, city, country)

#create fuction to search weather a city
def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return
    # if city is found unpack the weather information
    icon_url, temperature, description, city, country = result
    location_lb.configure(text=f"{city},{country}")

    #get weather icon from url and update
    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_lb.configure(image=icon)
    icon_lb.image = icon

    #update temperature and description label
    temp_lb.configure(text=f"Temperature: {temperature:.2f}°C")
    description_lb.configure(text=f"Description: {description}")

root = ttkbootstrap.Window(themename="morph")
root.title("Weather App by bwxTH")
root.geometry("400x400")

city_entry = ttkbootstrap.Entry(root, font="Helvetica, 18")
city_entry.pack(pady=10)

search_btn = ttkbootstrap.Button(root, text="Search", command=search, bootstyle="warning")
search_btn.pack(pady=10)

location_lb = tk.Label(root, font="Helvetica, 25")
location_lb.pack(pady=20)

icon_lb = tk.Label(root)
icon_lb.pack()

temp_lb = tk.Label(root, font="Helvetica, 25")
temp_lb.pack()

description_lb = tk.Label(root, font="Helvetica, 25")
description_lb.pack()

root.mainloop()
