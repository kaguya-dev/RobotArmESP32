import glob
import customtkinter as ctk
import serial
import sys
from serial.tools import list_ports
import time

# ----- Serial -----
ser = None

# ----- Appearance -----
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ----- App -----
app = ctk.CTk(fg_color="#28282b")
app.title("CHISA")
app.geometry("900x500")

# ----- Global Values -----
x = 0
y = 0
z = 0
w = x
mensagem = ""

ascii_art_path = "design/ascii-art.txt"
with open(ascii_art_path, "r") as file:
    ascii_art = file.read()
liveMode = False


# ----- Functions -----
def listar_portas():
    portas = []

    # Real USB devices (cross-platform safe)
    for p in list_ports.comports():
        if p.vid is not None:
            portas.append(p.device)

    # Add simulation ports (Linux only)
    if sys.platform.startswith("linux"):
        simuladas = glob.glob("/dev/pts/[0-9]*")
        portas.extend(simuladas)

    return sorted(portas)


def conectar():
    global ser
    porta = combo_portas.get().split(" - ")[0]

    try:
        ser = serial.Serial(porta, 115200, timeout=1)
        status_label.configure(text="Status: Conectado", text_color="green")
    except Exception as e:
        status_label.configure(text="Status: Erro", text_color="red")
        print(e)


def atualizar_portas():
    combo_portas.configure(values=listar_portas())


def atualizar_mensagem_live(valor=None):
    x = round(xscale.get())
    y = round(yscale.get())
    z = round(zscale.get())
    w = round(wscale.get())

    texto = f"{x}, {y}, {z}, {w}"
    label_message.configure(text=f"Mensagem: {texto}")


def enviar():
    if ser is None:
        return

    x = round(xscale.get())
    y = round(yscale.get())
    z = round(zscale.get())
    w = round(wscale.get())

    mensagem = f"{x}, {y}, {z}, {w}\n"
    ser.write(mensagem.encode())


def toggleLive():
    global liveMode
    liveMode = not liveMode

    if liveMode:
        live_Button.configure(text="Live ON", fg_color="green")
    else:
        live_Button.configure(text="Live OFF", fg_color="gray")


def setValues():
    x = round(xscale.get())
    y = round(yscale.get())
    z = round(zscale.get())
    w = round(wscale.get())
    mensagem = f"{x}, {y}, {z}, {w}"
    return mensagem


def atualizar_mensagem(texto):
    label_message.configure(text=f"Mensagem: {texto}")


def atualizar_resposta(texto):
    label_resposta.configure(text=f"Resposta: {texto}")


def ler_serial():
    if ser is not None and ser.inWaiting():
        linha = ser.readline().decode().strip()
    if liveMode:
        app.after(50, atualizar_resposta, linha)


app.grid_columnconfigure(1, weight=2)
app.grid_columnconfigure(2, weight=4)

app.grid_rowconfigure(0, weight=2)
# ----- Layout Frame -----
main_frame = ctk.CTkFrame(app, fg_color="#242124")
main_frame.grid(row=0, column=2, padx=20, pady=20, sticky="nsew")

ports_frame = ctk.CTkFrame(app, fg_color="#242124")
ports_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")


# art_frame = ctk.CTkFrame(app)
# art_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")


# ----- Sliders -----
def criar_slider(label_text):
    frame = ctk.CTkFrame(main_frame, width=90)
    frame.pack(pady=10, fill="x")

    label = ctk.CTkLabel(frame, text=label_text)
    label.pack(anchor="w")

    slider = ctk.CTkSlider(frame, from_=0, to=180, command=atualizar_mensagem_live)
    slider.pack(fill="x", pady=5, padx=20)

    return slider


xscale = criar_slider("X Axis")
yscale = criar_slider("Y Axis")
zscale = criar_slider("Z Axis")
wscale = criar_slider("W Axis")

sendButton = ctk.CTkButton(main_frame, text="Enviar", command=enviar)
sendButton.pack(pady=5, fill="x")
live_Button = ctk.CTkButton(
    main_frame, text="Live OFF", command=toggleLive, fg_color="gray"
)
live_Button.pack(pady=5, fill="x")

title_label = ctk.CTkLabel(
    ports_frame, text="CHISA V1.0", text_color="#adbce6", font=("DejaVu Sans Mono", 30)
)
title_label.pack(pady=5, padx=1)

portButton = ctk.CTkButton(ports_frame, text="Conectar", command=conectar)
portButton.pack(pady=5, fill="x")
updtPortButton = ctk.CTkButton(ports_frame, text="Atualizar", command=atualizar_portas)
updtPortButton.pack(pady=5, fill="x")

combo_portas = ctk.CTkComboBox(ports_frame, values=listar_portas())
combo_portas.pack(pady=3, fill="x")

label_message = ctk.CTkLabel(main_frame, text="Mensagem:")
label_message.pack(pady=5)

label_resposta = ctk.CTkLabel(main_frame, text="Resposta:")
label_resposta.pack(pady=5)


status_label = ctk.CTkLabel(ports_frame, text="Status: Desconectado", text_color="red")
status_label.pack(pady=3)

# ----- TextBoxes -----
# ascii_box = ctk.CTkTextbox(art_frame, font=("DejaVu Sans Mono", 4))
# ascii_box.insert(0.0, ascii_art)
# ascii_box.configure(state="disabled", wrap="none")
# ascii_box.pack(fill="both", expand=True)

# ----- Start Serial Thread -----
ler_serial()

# ----- Run -----
app.mainloop()
