from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import customtkinter
from math import floor

import serial 
import threading
import time 

#val = 40
a = 1
start_progbar = 0
warning = 0
data_sensor = 0
ser = serial.Serial(port='COM3', baudrate=115200, timeout=0)

if not ser.isOpen():
    ser.open()


def start():
    global progressbar
    global text_var
    # canvas.delete("all") 
    # progressbar = ttk.Progressbar(canvas,orient = VERTICAL, value=30,length = 400, mode = 'determinate')
    # progressbar.place(x=200, y = 175, width = 50)
    # canvas.create_text(500, 50,text="Application pour mesurer le taux de sécheresse des sols", font=("Helvetica", 18), justify="center" )
    echelle()
    progressbar = customtkinter.CTkProgressBar(master=fenetre, orientation=VERTICAL, width = 50, height=360, corner_radius=5, border_width=5, progress_color="steel blue")
    progressbar.place(x = 300, y=300, anchor = CENTER)
    progressbar.set(0.40668)
    label.destroy()
    customtkinter.CTkLabel(master=fenetre,
                               textvariable=text_var,
                               width=700,
                               height=80,
                               fg_color=("steel blue"),
                               corner_radius=8,
                               font=("Helvetica", 24)).place(relx=0.5, rely=0.1, anchor=CENTER)

    
def taux_humidite():
    #global val
    global data_sensor
    val = data_sensor*100/100000

    if(val<=20):
        color_fg = "red"

    else: 
        color_fg = "steel blue"

    customtkinter.CTkLabel(master=fenetre,
                        text="Taux d'humidité",
                        width=200,
                        height=70,
                        fg_color=("steel blue"),
                        corner_radius=8,
                        font=("Helvetica", 20)).place(relx=0.7, rely=0.3, anchor=CENTER)
    
    customtkinter.CTkLabel(master=fenetre,
                        text=f"{val}%",
                        width=200,
                        height=70,
                        fg_color=(color_fg),
                        corner_radius=8,
                        font=("Helvetica", 20)).place(relx=0.7, rely=0.5, anchor=CENTER)






def variation():
    global val
    global a
    global canvas
    global warning 
    current_val = val/100

    if(val==100):
        a=-1
    if(val==0):
        a=1
    if(val<=20):
        progressbar.set(current_val)
        progressbar.configure(progress_color = "red")
        #label1.place(relx=0.7, rely=0.7, anchor=CENTER)
        if(warning==0):
            
            warning = 1
    else: 
        #label1.destroy()
        progressbar.set(current_val)
        progressbar.configure(progress_color = "steel blue")
        warning = 0

    taux_humidite()
    # graph_humidite(val)
    val += a*10 
    print(val)
    
def echelle():   
    for i in range(6):
        #canvas.create_text(170, 175 + i*80, text = f"{100 - i*20}% --", tag="echelle", font=("Hel2vetica", 12))
        customtkinter.CTkLabel(master=fenetre,
                    text = f"{100 - i*20}% --",
                    width=10,
                    height=5,
                    fg_color=("transparent"),
                    corner_radius=8,
                    font=("Helvetica", 15)).place(x=230, y=125 + i*70, anchor=CENTER)


def read():
    global data_sensor
    global progressbar
    #while True:
    data=ser.readline()
    if data: 
    #data_sensor=data.decode('utf8')
        data_s=data.decode('utf8')
        to_convert = data_s.replace('\n', '')
        to_convert = data_s.replace('\0', '')

        try:
            # Convertir la chaîne en entier
            data_sensor = int(to_convert)
        except ValueError:
            # Gérer le cas où la chaîne n'est pas un entier valide
            print("Erreur: Impossible de convertir en entier :", to_convert)
    variation_auto()
        
    # data_frequence=data_sensor.split(';')

    # if data_sensor=='':
    #     final_data = 0
    # else:
    #     final_data = int(data_frequence)  
    # if(to_convert != ""): 
    #     print(f"{to_convert} + {int(to_convert)}")
    

def variation_auto():
   # global val
    global data_sensor
    global canvas
    #global warning 
    current_val = data_sensor/100000
    print(f"{current_val} + {data_sensor}")
    if(current_val<=0.2):
        progressbar.set(current_val)
        progressbar.configure(progress_color = "red")
        #label1.place(relx=0.7, rely=0.7, anchor=CENTER)
    else: 
        #label1.destroy()
        progressbar.set(current_val)
        progressbar.configure(progress_color = "steel blue")

    taux_humidite()

def start_reading():
    read()
    fenetre.after(100, start_reading)

customtkinter.set_appearance_mode("dark")
fenetre = customtkinter.CTk()
fenetre.geometry("1000x600")

# canvas = Canvas(fenetre, width=1000, height=600, background='black')
# canvas.pack()
# txt = fenetre.create_text(500,300, text="Application pour mesurer le taux de sécheresse des sols", font=("Helvetica", 24), justify="center")
text_var = StringVar(value="Application pour mesurer le taux de sécheresse des sols")

label = customtkinter.CTkLabel(master=fenetre,
                               textvariable=text_var,
                               width=700,
                               height=50,
                               fg_color=("steel blue"),
                               corner_radius=8)
label.place(relx=0.5, rely=0.5, anchor=CENTER)
b1 = customtkinter.CTkButton(fenetre, text="Commencer", command = start)
b1.place(relx = 0.3, rely = 0.9, anchor = CENTER)
b2 = customtkinter.CTkButton(fenetre,text="variation auto", command = start_reading)
b2.place(relx = 0.7, rely = 0.9, anchor = CENTER)
# label1 = customtkinter.CTkLabel(master=fenetre,
#                                 text="Taux de sécheresse élevé",
#                                 width=200,
#                                 height=150,
#                                 fg_color=("yellow"),
#                                 corner_radius=0,
#                                 font=("Helvetica", 30))




fenetre.mainloop()



