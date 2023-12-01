from tkinter import messagebox
from bs4 import BeautifulSoup
from tkinter.ttk import *
from tkinter import *
import webbrowser
import requests
from datetime import datetime, timedelta
import os
import tempfile

URL = "https://www.essecke-erfurt.de/mittagsverpflegung/essecke-melexis/"
HTML_DOC = requests.get(URL)

current_date = datetime.now()
year, week_num, day_of_week = current_date.isocalendar()
username = os.getlogin()


def open_main_root():
    main_root = Tk()
    main_root.geometry("250x50")
    main_root.resizable(False, False)
    main_root.title("Speiseplan")


    button_width = 17

    melexis_btn = Button(main_root, text="Melexis", command=open_melexis_plan)
    melexis_btn.configure(width=button_width)
    melexis_btn.place(relx=0.27, rely=0.5, anchor="center")


    guka_btn = Button(main_root, text="Gulaschkanone", command=open_guka_plan)
    guka_btn.configure(width=button_width)
    guka_btn.place(relx=0.73, rely=0.5, anchor="center")

    main_root.mainloop()


def open_guka_plan():
    today = datetime.now()
    year = today.year
    kw = today.isocalendar().week
    needed_month = today - timedelta(days = today.weekday())

    guka_url = f"https://gulaschkanone-erfurt.de/wp-content/uploads/{year}/{needed_month.month}/Sued-Ost-KW-{kw}.pdf"
    webbrowser.open(guka_url, new=0, autoraise=True)



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
        return url
    except (UnboundLocalError, FileNotFoundError):
        messagebox.showerror("Fehler", "Der aktuelle Speiseplan wurde nicht gefunden. Bitte versuchen Sie es später erneut!")


def open_melexis_plan():
    url = get_current_speiseplan(HTML_DOC)
    response = requests.get(url)

    temp_dict = tempfile.TemporaryDirectory()
    base_path = temp_dict.name
    tmp_pdf_file_path = base_path + "\pdf_tmp.pdf" 

    with open(tmp_pdf_file_path, "wb") as tmpPDF:
        tmpPDF.write(response.content)

    os.system(tmp_pdf_file_path)
    temp_dict.cleanup()

open_main_root()