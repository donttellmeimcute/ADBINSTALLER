import tkinter as tk
from tkinter import filedialog
import subprocess
import os

def select_files():
    files = filedialog.askopenfilenames(filetypes=[("APK Files", "*.apk")])
    file_list.delete(0, tk.END)
    for file in files:
        file_list.insert(tk.END, file)

def install_files():
    for i in range(file_list.size()):
        file_path = file_list.get(i)
        subprocess.run(["adb", "install", file_path])

def enable_wireless_debugging():
    ip_address = ip_entry.get()
    code = code_entry.get()
    port = port_entry.get()
    
    # Establecer el puerto como una variable de entorno
    os.environ['ANDROID_ADB_SERVER_PORT'] = port
    
    subprocess.run(["adb", "tcpip", port])
    subprocess.run(["adb", "connect", f"{ip_address}:{port}"])

def disable_wireless_debugging():
    subprocess.run(["adb", "usb"])  # Cambiar a USB
    subprocess.run(["adb", "kill-server"])  # Detener el servidor ADB

def on_closing():
    disable_wireless_debugging()
    root.destroy()

root = tk.Tk()
root.title("Instalador de APKs")

file_frame = tk.Frame(root)
file_frame.pack(pady=10)

file_list = tk.Listbox(file_frame, width=50)
file_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(file_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

file_list.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=file_list.yview)

select_button = tk.Button(root, text="Seleccionar archivos", command=select_files)
select_button.pack(pady=5)

install_button = tk.Button(root, text="Instalar archivos", command=install_files)
install_button.pack(pady=5)

wireless_debug_frame = tk.LabelFrame(root, text="Depuración inalámbrica")
wireless_debug_frame.pack(pady=10)

ip_label = tk.Label(wireless_debug_frame, text="Dirección IP:")
ip_label.grid(row=0, column=0, padx=5, pady=5)

ip_entry = tk.Entry(wireless_debug_frame)
ip_entry.grid(row=0, column=1, padx=5, pady=5)

code_label = tk.Label(wireless_debug_frame, text="Código:")
code_label.grid(row=1, column=0, padx=5, pady=5)

code_entry = tk.Entry(wireless_debug_frame)
code_entry.grid(row=1, column=1, padx=5, pady=5)

port_label = tk.Label(wireless_debug_frame, text="Puerto:")
port_label.grid(row=2, column=0, padx=5, pady=5)

port_entry = tk.Entry(wireless_debug_frame)
port_entry.grid(row=2, column=1, padx=5, pady=5)

enable_button = tk.Button(wireless_debug_frame, text="Habilitar", command=enable_wireless_debugging)
enable_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

exit_button = tk.Button(root, text="Salir", command=on_closing)
exit_button.pack(pady=10)

root.protocol("WM_DELETE_WINDOW", on_closing)  # Llamar a on_closing() cuando se cierre la ventana

root.mainloop()
