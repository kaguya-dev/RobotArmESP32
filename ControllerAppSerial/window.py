import glob
import customtkinter as ctk
import serial
import threading
from serial.tools import list_ports
import time

# ----- Serial -----
ser = None

# ----- Appearance -----
ctk.set_appearance_mode("dark")  # Dark mode
ctk.set_default_color_theme("blue")  # You can try: green, dark-blue

# ----- App -----
app = ctk.CTk()
app.title("CHISA")
app.geometry("400x450")
# ----- Global Values -----
x = 0
y = 0
z = 0
mensagem = ""
liveMode = False


# ----- Functions -----
def listar_portas():
    portas = (
        glob.glob("/dev/ttyUSB*") + glob.glob("/dev/ttyACM*") + glob.glob("/dev/pts/*")
    )

    return sorted(portas)


def conectar():
    global ser
    porta = combo_portas.get()

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

    texto = f"{x}, {y}, {z}"
    label_message.configure(text=f"Mensagem: {texto}")


def enviar():
    if ser is None:
        return

    x = round(xscale.get())
    y = round(yscale.get())
    z = round(zscale.get())

    mensagem = f"{x}, {y}, {z}\n"
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

    mensagem = f"{x}, {y}, {z}"
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


# ----- Layout Frame -----
main_frame = ctk.CTkFrame(app)
main_frame.pack(side="right", padx=20, pady=20, fill="both", expand=True)
ports_frame = ctk.CTkFrame(app)
ports_frame.pack(side="left", padx=10, pady=5, fill="both", expand=False)


# ----- Sliders -----
def criar_slider(label_text):
    frame = ctk.CTkFrame(main_frame)
    frame.pack(pady=10, fill="x")

    label = ctk.CTkLabel(frame, text=label_text)
    label.pack(anchor="w")

    slider = ctk.CTkSlider(frame, from_=0, to=180, command=atualizar_mensagem_live)
    slider.pack(fill="x", pady=5)

    return slider


xscale = criar_slider("X Axis")
yscale = criar_slider("Y Axis")
zscale = criar_slider("Z Axis")

# ----- Buttons -----
sendButton = ctk.CTkButton(main_frame, text="Enviar", command=enviar)
sendButton.pack(pady=5, fill="x")
live_Button = ctk.CTkButton(
    main_frame, text="Live OFF", command=toggleLive, fg_color="gray"
)
live_Button.pack(pady=5, fill="x")

portButton = ctk.CTkButton(ports_frame, text="Conectar", command=conectar)
portButton.pack(pady=5, fill="x")
updtPortButton = ctk.CTkButton(ports_frame, text="Atualizar", command=atualizar_portas)
updtPortButton.pack(pady=5, fill="x")
# ----- Combo_Box -----
combo_portas = ctk.CTkComboBox(ports_frame, values=listar_portas())
combo_portas.pack(pady=3, fill="x")
# ----- Labels -----
label_message = ctk.CTkLabel(main_frame, text="Mensagem:")
label_message.pack(pady=5)

label_resposta = ctk.CTkLabel(main_frame, text="Resposta:")
label_resposta.pack(pady=5)

status_label = ctk.CTkLabel(ports_frame, text="Status: Desconectado", text_color="red")
status_label.pack(pady=3)

# ----- Start Serial Thread -----
ler_serial()

# ----- Run -----
app.mainloop()
