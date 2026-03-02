import tkinter as tk
from tkinter import ttk
import serial
import threading

ser = serial.Serial("/dev/ttyUSB0", 115200)


def enviar():
    x = round(xscale.get())
    y = round(yscale.get())
    z = round(zscale.get())
    mensagem = f"{x}, {y}, {z}\n"
    # label_message.config(text=mensagem)
    ser.write(mensagem.encode())


def ler_serial():
    while True:
        linha = ser.readline().decode().strip()
        label_resposta.config(text=linha)


def iniciar_thread():
    t = threading.Thread(target=ler_serial, daemon=True)
    t.start()


root = tk.Tk()

style = ttk.Style()
style.theme_use("clam")
xscale = ttk.Scale(root, from_=0, to=180, orient="horizontal")
xscale.pack(pady=10, fill="x", padx=10)

yscale = ttk.Scale(root, from_=0, to=180, orient="horizontal")
yscale.pack(pady=10, fill="x", padx=10)

zscale = ttk.Scale(root, from_=0, to=180, orient="horizontal")
zscale.pack(pady=10, fill="x", padx=10)

botao = ttk.Button(root, text="Enviar", command=enviar)
botao.pack(pady=10, fill="x", padx=20)

label_message = ttk.Label(root, text="Mensagem:")
label_message.pack(pady=10, fill="x", padx=20)
label_resposta = ttk.Label(root, text="Resposta:")
label_resposta.pack(pady=10, fill="x", padx=20)

iniciar_thread()
root.mainloop()
