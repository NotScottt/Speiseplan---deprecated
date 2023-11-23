from tkinter import messagebox
from bs4 import BeautifulSoup
from pathlib import Path
from sys import exit
import configparser
import functions
import requests
import datetime
import wget
import os

URL = "https://www.essecke-erfurt.de/mittagsverpflegung/essecke-melexis/"
HTML_DOC = requests.get(URL)

current_date = datetime.datetime.now()
year, week_num, day_of_week = current_date.isocalendar()
username = os.getlogin()

# Logfile Path
static_path = f"C:/Users/{username}"
second_logfile_path = functions.readLogfilePath()
logfile_path = f"{static_path}{second_logfile_path}/log.txt"

# Download Path
second_path = functions.readDownloadPath()
path = f"{static_path}{second_path}"


######################################################################################################

if len(str(current_date.hour)) == 2 and len(str(current_date.minute)) == 2:
        log_time = f"{current_date.hour}:{current_date.minute}"
    
elif len(str(current_date.hour)) == 1 and len(str(current_date.minute)) == 2:
        log_time = f"0{current_date.hour}:{current_date.minute}"

elif len(str(current_date.hour)) == 2 and len(str(current_date.minute)) == 1:
        log_time = f"{current_date.hour}:0{current_date.minute}"
    
elif len(str(current_date.hour)) == 1 and len(str(current_date.minute)) == 1:
        log_time = f"0{current_date.hour}:0{current_date.minute}"


if len(str(current_date.day)) == 1 and len(str(current_date.month)) == 1:
        log_date = f"0{current_date.day}.0{current_date.month}.{current_date.year}, {log_time}"

elif len(str(current_date.day)) == 1 and len(str(current_date.month)) == 2:
        log_date = f"0{current_date.day}.{current_date.month}.{current_date.year}, {log_time}"

elif len(str(current_date.day)) == 2 and len(str(current_date.month)) == 1:
        log_date = f"{current_date.day}.0{current_date.month}.{current_date.year}, {log_time}"  

elif len(str(current_date.day)) == 2 and len(str(current_date.month)) == 2:
        log_date = f"{current_date.day}.{current_date.month}.{current_date.year}, {log_time}"


######################################################################################################



def get_current_speiseplan(html):
    try:
        soup = BeautifulSoup(html.content, "lxml")
        
        div = soup.find("div", class_= "rightDownload")
        date = div.select_one("strong").text

        if len(str(week_num)) == 1:
            current_speiseplan_date = f"Speiseplan 0{week_num}.23.pdf"
        else:
            current_speiseplan_date = f"Speiseplan {week_num}.23.pdf"
        
        for current_speiseplan_list in soup.find_all("a", href=True,string=current_speiseplan_date):
            ultimate_link_final = current_speiseplan_list["href"]
        
        url = ultimate_link_final

        # Logfile
        username = os.getlogin() 
        static_path = f"C:/Users/{username}"
        second_logfile_path = functions.readLogfilePath()
            
        logfile_path = f"{static_path}{second_logfile_path}/log.txt"

        # Download
        second_path = functions.readDownloadPath()
        path = f"{static_path}{second_path}"
        
        if not os.path.exists(path):
            os.makedirs(path)
            messagebox.showinfo("Info", f"Ein neuer Ordner wurde unter {path} erstellt.")
            
            if not os.path.exists(logfile_path):
                with open(logfile_path, "w")as file:
                    functions.mahlzeitInDoc(file)
                    functions.writeFileNew(file, log_date, week_num, path)
                
                with open(logfile_path, "a")as file:
                    functions.writeNewPath(file, log_date, path)
            
            else:
                with open(logfile_path, "a")as file:
                    functions.writeNewPath(file, log_date, path)

        if len(str(week_num)) == 1:
            file_already_in = f"{path}/Speiseplan+0{week_num}.23.pdf"
        else:
            file_already_in = f"{path}/Speiseplan+{week_num}.23.pdf"
            
        
        is_in = os.path.isfile(file_already_in)

        if is_in == True:
            messagebox.showerror('Fehler', f'Der aktuelle Speiseplan ist bereits vorhanden unter {path}')
            if not os.path.exists(logfile_path):
                with open(logfile_path, "w")as file:
                    functions.mahlzeitInDoc(file)
                    functions.writeFileNew(file, log_date, week_num, path)
                
                with open(logfile_path, "a")as file:
                    functions.writeErrorDup(file, log_date, path)
            
            else:
                with open(logfile_path, "a")as file:
                    functions.writeErrorDup(file, log_date, path)
        else:
            messagebox.showinfo("Info", "Mahlzeit! Der aktuelle Speiseplan liegt jetzt im Ordner.")
            wget.download(url,out = path)

            if not os.path.exists(logfile_path):
                with open(logfile_path, "w")as file:
                    functions.mahlzeitInDoc(file)
                    functions.writeFileNew(file, log_date, week_num, path)
            else:
                with open(logfile_path, "a")as file:
                    functions.writeCurrentFile(file, log_date, week_num, path)

    except (UnboundLocalError, FileNotFoundError):
        username = os.getlogin() 
        static_path = f"C:/Users/{username}"
        second_logfile_path = functions.readLogfilePath()
        logfile_path = f"{static_path}{second_logfile_path}/log.txt"
        second_path = functions.readDownloadPath()
        path = f"{static_path}{second_path}"


        messagebox.showerror("Fehler", "Der gesuchte Speiseplan wurde nicht gefunden. Bitte versuche es später noch ein mal!")
        if not os.path.exists(logfile_path):
            with open(logfile_path, "w")as file:
                functions.mahlzeitInDoc(file)
                functions.writeFileNew(file, log_date, week_num, path)
                functions.writeErrorNotFound(file, log_date, path)
        else:
            with open(logfile_path, "a")as file:
                functions.writeErrorNotFound(file, log_date, path)

######################################################################################################


current_year = str(current_date.year)
current_year_two_digit = current_year[2:4]


if len(str(week_num)) == 2:
    current_speiseplan = f"Speiseplan+{week_num}.{current_year_two_digit}.pdf"
else:
    current_speiseplan = f"Speiseplan+0{week_num}.{current_year_two_digit}.pdf"

download_path = functions.readDownloadPath()
file_to_path = f"{static_path}{download_path}/{current_speiseplan}"

if not os.path.exists(file_to_path):
    messagebox.showinfo("Info","Der Speiseplan wurde noch nicht heruntergeladen. Kleinen Moment.")
    get_current_speiseplan(HTML_DOC)

    if not os.path.exists(logfile_path):
            with open(logfile_path, "w")as file:
                functions.mahlzeitInDoc(file)
                functions.writeFileNew(file, log_date, week_num, path)
    os.system(file_to_path)
    print("exit")
else:
    os.system(file_to_path)
    print("exit")