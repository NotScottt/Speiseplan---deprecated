from tkinter import messagebox
from bs4 import BeautifulSoup
from tkinter.ttk import *
from tkinter import *
import webbrowser
import tempfile
import requests
from infi.systray import SysTrayIcon
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import os


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

today = datetime.now()
year = today.year
kw = today.isocalendar().week
needed_month = today - timedelta(days = today.weekday())

if len(str(needed_month.month)) == 1:
    month = f"0{needed_month.month}"
else:
    month = needed_month.month

if len(str(kw)) == 1:
    kw = f"0{kw}"


date_minus_one = datetime.today() - relativedelta(month=1)
if len(str(date_minus_one.month)) == 1:
    month_minus_one = f"0{date_minus_one.month}"
else:
    month_minus_one = date_minus_one.month


def open_guka_plan(systray):
    guka_url = f"https://gulaschkanone-erfurt.de/wp-content/uploads/{year}/{month}/Sued-Ost-KW-{kw}.pdf"
    webbrowser.open(guka_url, new=0, autoraise=True)


def get_sportklinik(systray):
    # https://sportklinik-erfurt.de/wp-content/uploads/2024/01/Kw06.pdf

    sportklinik_url = f"https://sportklinik-erfurt.de/wp-content/uploads/{year}/{month}/Kw{kw}.pdf"

    response = requests.get(sportklinik_url)
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.title.string

    
    
    if "Seite wurde nicht gefunden" in title:
        final_url = f"https://sportklinik-erfurt.de/wp-content/uploads/{year}/{month_minus_one}/Kw{kw}.pdf"
    else:
        final_url = sportklinik_url

    # sportklinik_url = f"https://gulaschkanone-erfurt.de/wp-content/uploads/{year}/{month}/Sued-Ost-KW-{kw}.pdf"
    webbrowser.open(final_url, new=0, autoraise=True)


def get_current_speiseplan(html):
    try:
        soup = BeautifulSoup(html.content, "lxml")

        if len(str(week_num)) == 1:
            current_speiseplan_date = f"Speiseplan 0{week_num}.{str(year)[2:]}.pdf"
        else:
            current_speiseplan_date = f"Speiseplan {week_num}.{str(year)[2:]}.pdf"

      
        for current_speiseplan_list in soup.find_all("a", href=True,string=current_speiseplan_date):
            ultimate_link_final = current_speiseplan_list["href"]

        return ultimate_link_final
    except (UnboundLocalError, FileNotFoundError):
        messagebox.showerror("Fehler", "Der aktuelle Speiseplan wurde nicht gefunden. Bitte versuchen Sie es später erneut!")


def open_melexis_plan(systray):
    url = get_current_speiseplan(HTML_DOC)
    response = requests.get(url)

    if response.status_code == 200:
        temp_dict = tempfile.TemporaryDirectory()
        base_path = temp_dict.name
        tmp_pdf_file_path = base_path + "\pdf_tmp.pdf" 

        with open(tmp_pdf_file_path, "wb") as tmpPDF:
            tmpPDF.write(response.content)

        os.system(tmp_pdf_file_path)
        temp_dict.cleanup()

    else:
        messagebox.showerror("Fehler", f"Der Aktuelle Speiseplan konnte nicht gefunden werden.\n\nGrund:\nStatuscode {response.status_code}, {response.reason}")
    

menu_options = (("Melexis", None, open_melexis_plan), ("Gulaschkanone", None, open_guka_plan), ("Sportklinik", None, get_sportklinik))
systray = SysTrayIcon("Besteck.ico", "Speisepläne", menu_options)

systray.start()