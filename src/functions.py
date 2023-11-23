import configparser
from tkinter import messagebox, filedialog
from sys import exit
import os

def mahlzeitInDoc(x):
    x.write("  __  __         _      _            _  _    _ \n")
    x.write(" |  \/  |       | |    | |          (_)| |  | |\n")
    x.write(" | \  / |  __ _ | |__  | | ____ ___  _ | |_ | |\n")
    x.write(" | |\/| | / _` || '_ \ | ||_  // _ \| || __|| |\n")
    x.write(" | |  | || (_| || | | || | / /|  __/| || |_ |_|\n")
    x.write(" |_|  |_| \__,_||_| |_||_|/___|\___||_| \__|(_)\n")



def exit_application():
    msg_box = messagebox.askquestion('Init generieren', 'Möchtest du ein Init-File generieren lassen?', icon='warning')
    if msg_box == 'yes':
        f = filedialog.asksaveasfile(mode="w", title="Speichern", initialfile = "config" , defaultextension=".ini", initialdir="")
        path_to_config = f.name
        with open(f.name, "w") as file:
            file.write("[MODIFY]\n")
            file.write("download_path = /Desktop/Essensplan\n")
            file.write("logfile_path = /Desktop/Essensplan\n")
            file.write('\n\n# WICHTIG: Das erste "/" darf nicht gelöscht werden\n')
            file.write('#          Der Pfad darf nicht mit einem "/" enden')
            file.write('#          Achte außerdem darauf, dass der Pfad Existieren muss')

        messagebox.showinfo("Erfolgreich", f"Die config.ini wurde erstellt. Achte bitte darauf, dass die Datei im gleichen ordner wie Die Anwendung lieg.")
        exit()
    else:
        exit()

def writeFileNew(file, log_date, week_num, path):
    file.write(f"\n{log_date}: Neues Logfile wurde erstellt.")
    file.write(f"\n{log_date}: Speiseplan für KW {week_num} heruntergeladen und unter {path} gespeichert.")

def writeCurrentFile(file, log_date, week_num, path):
    file.write(f"\n{log_date}: Speiseplan für KW {week_num} heruntergeladen und unter {path} gespeichert.")

def writeErrorDup(file, log_date, path):
    file.write(f"\n{log_date}: Fehler erhalten! 'Der aktuelle Speiseplan ist bereits vorhanden unter {path}'")

def writeErrorNotFound(file, log_date, path):
    file.write(f"\n{log_date}: Fehler erhalten! 'Der gesuchte Speiseplan wurde nicht gefunden. Bitte versuche es später noch ein mal!'")

def writeNewPath(file, log_date, path):
    file.write(f"\n{log_date}: Neuer Pfad wurde unter {path} erstellt.")

def readDownloadPath():
    config = configparser.ConfigParser()
    # config.sections()
    try:
        config.read("config.ini")
        return config["MODIFY"]["download_path"]
    except (FileNotFoundError, KeyError):
        messagebox.showerror("Fehler", "Der Pfad in der config.ini wurde nicht gefunden")
        exit_application()

def readLogfilePath():
    config = configparser.ConfigParser()
    try:
        config.read("config.ini")
        return config["MODIFY"]["logfile_path"]
    except (KeyError, FileNotFoundError):
        messagebox.showerror("Fehler", "Es wurde keine config.ini gefunden. Stelle bitte sicher, dass diese im gleichen Ordner liegt!")
        exit_application()