import customtkinter as ctk
import serial
import threading

# ----- Serial -----
ser = serial.Serial("/dev/ttyUSB0", 115200)

# ----- Appearance -----
ctk.set_appearance_mode("dark")  # Dark mode
ctk.set_default_color_theme("blue")  # You can try: green, dark-blue

# ----- App -----
app = ctk.CTk()
app.title("CHISA")
app.geometry("400x450")


# ----- Functions -----
def enviar():
    x = round(xscale.get())
    y = round(yscale.get())
    z = round(zscale.get())

    mensagem = f"{x}, {y}, {z}\n"
    label_message.configure(text=f"Mensagem: {mensagem.strip()}")

    ser.write(mensagem.encode())


def atualizar_resposta(texto):
    label_resposta.configure(text=f"Resposta: {texto}")


def ler_serial():
    while True:
        linha = ser.readline().decode().strip()
        app.after(0, atualizar_resposta, linha)


def iniciar_thread():
    t = threading.Thread(target=ler_serial, daemon=True)
    t.start()


# ----- Layout Frame -----
main_frame = ctk.CTkFrame(app)
main_frame.pack(padx=20, pady=20, fill="both", expand=True)


# ----- Sliders -----
def criar_slider(label_text):
    frame = ctk.CTkFrame(main_frame)
    frame.pack(pady=10, fill="x")

    label = ctk.CTkLabel(frame, text=label_text)
    label.pack(anchor="w")

    slider = ctk.CTkSlider(frame, from_=0, to=180)
    slider.pack(fill="x", pady=5)

    return slider


xscale = criar_slider("X Axis")
yscale = criar_slider("Y Axis")
zscale = criar_slider("Z Axis")

# ----- Send Button -----
botao = ctk.CTkButton(main_frame, text="Enviar", command=enviar)
botao.pack(pady=20, fill="x")

# ----- Labels -----
label_message = ctk.CTkLabel(main_frame, text="Mensagem:")
label_message.pack(pady=5)

label_resposta = ctk.CTkLabel(main_frame, text="Resposta:")
label_resposta.pack(pady=5)

# ----- Start Serial Thread -----
iniciar_thread()

# ----- Run -----
app.mainloop()
