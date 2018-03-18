from tkinter import *
import tkinter as tk
import matplotlib.pyplot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
#matplotlib.use('TkAgg')

import Adafruit_DHT

from PIL import ImageTk, Image
from datetime import datetime

class Generate_plot():
	"""Generates and updates temperature and humidity graph."""
	def __init__(self):
		# Create plot of temp and humidity data.
		self.f = Figure(figsize=(5, 4), dpi=100)
		self.a = self.f.add_subplot(111)
	
		self.a.plot(indoor_temp_hist)
		self.a.plot(indoor_hum_hist)
		self.a.set_title("Temperature and humidity last 24h")
		self.a.set_xlabel("Time")
		self.a.set_ylabel("Degrees C / % Relative Humidity")
		self.a.legend(["Indoor temperature", "Indoor humidity"], loc="upper left")

		self.canvas = FigureCanvasTkAgg(self.f, master=page_3)
		self.canvas.show()
		#canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		
	def clear_plot(self):
		"""Clears graph."""
		self.a.clear()
		self.canvas.draw()
		
	def update_plot(self):
		"""Updates graph with current data."""
		self.a.plot(indoor_temp_hist)
		self.a.plot(indoor_hum_hist)
		self.a.set_title("Temperature and humidity last 24h")
		self.a.set_xlabel("Time")
		self.a.set_ylabel("Degrees C / % Relative Humidity")
		self.a.legend(["Indoor temperature", "Indoor humidity"], loc="upper left")
		self.canvas.draw()

def exit():
	"""Function for quitting."""
	root.quit()

def raise_frame(frame):
	"""Function for navigating to page."""
	frame.tkraise()
#	if frame=='page_3':
#		# Regenerates graph
#		plot.clear_plot()
#		plot.update_plot()

def clock():
	"""Gets current time for the display."""
	root.after(1000, clock)
	currenttime = datetime.now().strftime("%H:%M:%S")
	time.set(currenttime)

def get_temp():
	"""Gets current temperature and humidity from sensor."""
	root.after(temp_interval, get_temp)
	humidity, temperature = Adafruit_DHT.read_retry(22, 4)
	temp = "{0:0.1f}".format(temperature)
	indoor_temp_hist.append(temp)
	if len(indoor_temp_hist) > (86400/temp_interval):
		indoor_temp_hist.pop(0)
	temperature_in.set(temp + "°C")
	hum = "{0:0.1f}".format(humidity)
	# Make a sanity check on humidity to avoid crazy readings
	if float(hum) >= 0 and float(hum) <= 100:
		indoor_hum_hist.append(hum)
		if len(indoor_hum_hist) > (86400/temp_interval):
			indoor_hum_hist.pop(0)
		humidity_in.set(hum + "%RH")

def plot_page(frame):
	global plot
	"""Activates plot page (3) and regenerates plot."""
	frame.tkraise()
	plot.clear_plot()
	plot.update_plot()


# Definitions
menu_color = "#004060"
main_color = "#111111"
text_color = "#D0D0D0"
highlight_color = "#000000"
main_font = "Dejavu Sans"

indoor_temp_hist = []
indoor_hum_hist = []

temp_interval = 10000

# TKinter
root = tk.Tk()
root.geometry("1024x600")
root.resizable(0,0)
root.overrideredirect(True) # Overrides window manager
root.wm_attributes("-topmost", 1) # Makes window top
root.config(cursor="none") # Hides cursor

back = tk.Frame(master=root, bg=menu_color)
back.pack_propagate(0)
back.pack(fill=tk.BOTH, expand=False)

# Icons
temp_icon = ImageTk.PhotoImage(file="temp.png")
forecast_icon = ImageTk.PhotoImage(file="forecast.png")
history_icon = ImageTk.PhotoImage(file="history.png")
settings_icon = ImageTk.PhotoImage(file="settings.png")

# Main menu buttons
button_1 = Button(master=back, image=temp_icon, bg=menu_color, 
	highlightbackground=highlight_color, command=lambda:raise_frame(page_1), 
	width=250, height=80, padx=5, pady=3)
button_1.grid(row=0, column=0)

button_2 = Button(master=back, image=forecast_icon, bg=menu_color, 
	highlightbackground=highlight_color, command=lambda:raise_frame(page_2), 
	width=250, height=80, padx=5, pady=3)
button_2.grid(row=0, column=1)

button_3 = Button(master=back, image=history_icon, bg=menu_color, 
	highlightbackground=highlight_color, command=lambda:plot_page(page_3), 
	width=250, height=80, padx=5, pady=3)
button_3.grid(row=0, column=2)

button_4 = Button(master=back, image=settings_icon, bg=menu_color, 
	highlightbackground=highlight_color, command=lambda:raise_frame(page_4), 
	width=250, height=80, padx=5, pady=3)
button_4.grid(row=0, column=3)

# Frame for pages
container = tk.Frame()
container.pack(side="top", fill="both", expand=True)

# Individual pages
page_1 = tk.Frame(bg=main_color)
page_1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

page_2 = tk.Frame(bg=main_color)
page_2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

page_3 = tk.Frame(bg=main_color)
page_3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

page_4 = tk.Frame(bg=main_color)
page_4.place(in_=container, x=0, y=0, relwidth=1, relheight=1)


# Background image
#image = ImageTk.PhotoImage(file="background.jpg")
#background = Label(page_1, image=image)
#background.place(x=0, y=0, relwidth=1, relheight=1)

"""Page 1 contents"""
# Clock
time = StringVar()
time.set("--:--:--")
clockLabel = Label(master=page_1, fg=text_color, bg=main_color, 
	textvariable=time, font=(main_font, 40))
clockLabel.place(x=385, y=60)

# Indoor/outdoor static labels
indoor = StringVar()
indoor.set("Indoor")

indoorLabel = Label(master=page_1, fg=text_color, bg=main_color, 
	textvariable=indoor, font=(main_font, 30))
indoorLabel.place(x=100, y=350)

outdoor = StringVar()
outdoor.set("Outdoor")

outdoorLabel = Label(master=page_1, fg=text_color, bg=main_color, 
	textvariable=outdoor, font=(main_font, 30))
outdoorLabel.place(x=600, y=350)

# Indoor temperature label
temperature_in = StringVar()
temperature_in.set('---' + "°C")

temperature_inLabel = Label(master=page_1, fg=text_color, bg=main_color, 
	textvariable=temperature_in, font=(main_font, 80))
temperature_inLabel.place(x=100, y=150)

# Indoor humidity label
humidity_in = StringVar()
humidity_in.set('---' + "%RH")

humidity_inLabel = Label(master=page_1, fg=text_color, bg=main_color, 
	textvariable=humidity_in, font=(main_font, 48))
humidity_inLabel.place(x=100, y=250)

# Outdoor temperature label
temperature_out = StringVar()
temperature_out.set("---" + "°C")

temperature_outLabel = Label(master=page_1, fg=text_color, bg=main_color, 
	textvariable=temperature_out, font=(main_font, 80))
temperature_outLabel.place(x=600, y=150)

# Page 2 contents
page_2text = StringVar()
page_2text.set("Weather Forecast")
page_2textLabel = Label(master=page_2, fg=text_color, bg=main_color, 
	textvariable=page_2text, font=(main_font, 30, "bold"))
page_2textLabel.place(x=20, y=20)

# Page 3 contents


# Page 4 contents 
page_4text = StringVar()
page_4text.set("Settings")
page_4textLabel = Label(master=page_4, fg=text_color, bg=main_color, 
	textvariable=page_4text, font=(main_font, 30, "bold"))
page_4textLabel.place(x=20, y=20)

# Exit button
button_exit = Button(master=page_4, text="Exit", bg=menu_color, 
	highlightbackground=highlight_color, command=exit, width=10, height=3)
button_exit.place(x=880, y=420)


# Show first page on startup
raise_frame(page_1)
# Create graph
plot = Generate_plot()
# Read clock and sensors
root.after(1000, clock)
root.after(temp_interval, get_temp)
# Run main interface 
root.mainloop()
