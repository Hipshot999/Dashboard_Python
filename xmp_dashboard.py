# -*- coding: UTF-8 -*-


# py_md5_xmp

# Scriptet tar en given xmp-fil och beräknar md5-summan för dess datafil.
#
# md5 summa i Adobe LR xmp-fil:
# PelleTags:PelleTag1_md5sum="935c0eb6242e80c95001368b9d53b421"
#
# Exiftool xmp-fil:
# <PelleTags:PelleTag1_md5sum>572737b08d11666255afb41b2c0443cb</PelleTags:PelleTag1_md5sum>

# cur.execute('''CREATE TABLE dashboard (id INTEGER PRIMARY KEY, main_path TEXT, last_run TEXT, tot_xmp INTEGER, ok_xmp INTEGER,nok_xmp INTEGER, missing_raw INTEGER)''')
# cur.execute("INSERT INTO dashboard (main_path, last_run, tot_xmp, ok_xmp, nok_xmp, missing_raw) VALUES(?,?,?,?,?,?)", ['H:\Pelle Temp', 0, 0, 0, 0, 0])
# cur.execute("UPDATE dashboard SET last_run = ? WHERE id = 1", ['2018-11-07'])
#
# cur.execute('''CREATE TABLE md5_results (id INTEGER PRIMARY KEY, file_path TEXT NOT NULL, file_name TEXT NOT NULL, md5_file TEXT, md5_calc TEXT, ok_nok TEXT, date TEXT)''')
# cur.execute("INSERT INTO md5_results (file_path, file_name, md5_file, md5_calc, ok_nok, date) VALUES(?,?,?,?,?,?)", ['C:\Pelle\Dropbox\Hack - xmp dashboard', 'testfil.xmp', '0', '0', '0', '2018-11-07'])
#


# ToDo's:
# - Fanken vilken röra det blev när jkjag försökte OOPsa allt. Nu är helt icke-intuitivt med ett mellan tinng mellan procedur och OOPs...
# - Multithreading? Starta flera threads om min folder ligger på olika diskar? Man ser ju att PCU lasten är runt 10%
# medans disklasten liger på 40-90%. Gör threadandet lite intelligent så den inte startar med mapar som ligger på samma disk.
# - Gör den def _main == osv. Verkar OOPsigt och bra.
# - Gör lite fler try-except, definitivt alla sql execute.
# - Någon form av utskrift så man kan följa mellanresultat. I ett nytt fönster?
# Kanske ngt liknande det jag har till verify xmp-hacket.
# Allt syns ju IDLE?

# Skippade:
# - En Cancel Run-knapp. - Fick det inte att lira, måste läsa på mer.


# v0.1 191106
# - Nu funkar läsa in xmp-filer och jämföra med beräknad md5 för motsvarande fil.
# v0.2 191107
# - sqlite fungerar ok
# - Räknar antalet närvarande xmp-filer i varje main folder.
# - Finns nu en tabell man använder.
# v0.3 191107
# - Själva dashboarden visas nu
# v0.4 191107
# - Göra event som fyller på databasen
# v0.5 1911115
# - Funkar nu med dynamisk generering av drop down boxarna. Man lagrar värdena i ett dict. Blev riktigt snyggt
# v0.6 191111
# - Funkar nu för New Run (och Do Nothing), Den raderar existerande värden i tabellen och fyller på med nya
# v0.7 191111
# - New run med delete allt gammalt i db verkar funka nu
# v0.8 191114
# - Cancel Run-fönster. Måste alltså ha två fönster. Nog strukturera om allt...
# - Implementerade en Cancel Run-knapp, men fick det inte att lira. Stegar till 0.9 och tar bort den.
# v0.9 191114
# - Lade till så att man får en utskrift var 1000 fil man hanterar. Det borde snabb upp lite.
# - Började titta på PyQt, verkar mycket stabilare än Tkinter. Får se om jag får ordning på det.
# - Fixade ett fel där lower case av t.ex. mp4 inte togs med eftersom listan med filändelser är versaler. Lade
# till upper() i jämförelsen.
# v0.10 191118
# - Fixat, var en räknare som inte stegade på rätt ställe. Nu finns det ett fel om det inte finns en raw-fil, då blir det ett index out of bounds. Detta händer när det är
# en DNG-fil, tex. DNG finns inte med bland filändelserna. Fixade det men nu blir det en irriterande utskrift för varje
# fil den hittar som inte finns i RAW-listan. En xmp kan ju ha en jpg bredvid sig t.ex. som inte skall generera ngn utskrift.
# - Fixat, lade till en separat räknare. Jag lade ju till att den skriver ut var xxx fil att hur många den processat. Irriterande skriver den det för de första
# 100 filerna. Min div/mod verkar inte funka som jag tänkte mig.
# - Lade till en break så när den räknat md5 för en fil så hoppar den ut loopen. Tidigare fortsatte den att stega igenom hela mappen även om den hiottat rätt fil.
# - Ta time() vid start av vartje mapp, och vi slkutet och spara. Skriv sedan ut en liten summering.
# - Vid varje start skriver jag ut mappnamnet. Kan man skriva ut antalet filer också? JAg räknar ju dem innan. Samma via Approxxx fuiler av yy?
# - Lade till en ny parameter vital_stats som om satt skriver ut det viktigaste.
# - Lite andra småfix.
# v0.11 191118
# - Optimerade lite för läsbarhet i loopen med filjämförelser.
# - Lade till lite mer text i starten och förlupen tid i sekunder för varje limited_printouts intervall.
# - Nu funkar det ganska bra, så stegar.
# v0.12 191118
# - Vilken röra. Tog bort tkinter och några av klasserna jag gjort, nog bättre att gå tillbaka till mer procedural kod.
# - Jag räknar antalet fall där jag har en xmp-fil utan tillhörande RAW,men jag visar det inte ngnstans.
# - En liten räknare som visar hur många dagar sen det var man körde mappen?
# - PyQt
# - Ange sekunder mellantider funkar bra, man kunde ge delta tid också.
# - Threading, man måste ha någon intelligens så man lägger ut dem på olika hårddiskar, och begränsar antalet trådar till antalet hårddiskar.
# v0.12 branch THREAD 191118
# - Threading verkar faktiskt funka. Men jisses vad rörig koden är nu!
# v0.13 branch THREAD 191119
# - Initiala tester visar att den inte klarar av att separera diskarna, så den startar två mappar på samma disk.
# Måste alltså starta threadsen manuellt, och vänta på att de blir klara.
# v0.14 191120
# - Det funkar nu! Den tittar på listan över mappar som skall köras, och fördelar sedan threadsen över
# hårddiskarna så att det aldrig körs två threads samtidigt på samma disk.
# - Detta blir nu huvudbranchen, tar bort THREAD.
# - Skulle behöva snygga till det, nu är det riktigt grötigt.
# - Den där Cancel-knappen är nog bra att ge sig på tillsammans med PtQt.
# - Delta sekunder för utskriften efter x antal filer. Men den måste vara thread-specifik, dvs varje thread har sin egen räknare.
# - Jag fyller inte i missing raw kolumnen i dashboard.
# - Test av GitHub, denna skall vara för W12.
# v0.15 191127
# - Gjorde om så att istället för att ha en version för varje dator så gjorde jag en config-fil, connect_sqlite_db.py, som jag
# anropar. I den finns rätt sträng för att connecta till rätt databas.
# v1.0 191127
# Andra försöket i git, tar bort ver-hantering i namnet, och passar på att stega till 1.0
# 191127
# - I Gityran så slarvade jag bort filerna med följande fix:
# -- Lade till att den visar antalet filer med missing RAW.
# --- Uppdaterade db på LM och W12, behövs ju på ACTUAL och W10 också,
# dvs ta fram sql:en och testa.
# --- GUIt behöver fixas, själva Dashboarden saknar klumnen missing RAW. 
# - Allt ovan nu fixat, behöver lägga till SQL för att uppdatera db på W10&ACTUAL
# 191129
# - Lade till antal dagar sedan senaste körningen.
# - Lade till delta seconds sedan varje limited_printouts.
# 191209
# - Git test

import os
from os.path import join
from operator import itemgetter, attrgetter
from tkinter import *
import fnmatch
import sys
import math
import threading
import subprocess
import fileinput
import datetime
import time
import hashlib
import sqlite3
from tkinter import ttk # Denna innehåller comboboxen - drop down.

# generate_md5_Checksum_def är en funktion som ligger i en separat fil,
from generate_md5_Checksum_def import md5Checksum
from connect_sqlite_db import connect_sqlite_db


def index_containing_substring(the_list, substring):  # returns the md5 sum, zero if no md5.
    for i, s in enumerate(the_list):
        if substring in s:
            md5 = s[s.find(substring)+28:s.find(substring)+60]
            return md5

    return 0


def folderThread(main_folder):
    global dashboard
    global main_folders
    global combo
    global combo_var
    global verbose
    global cur

    print("Thread started at " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print('Printout levels: ' + str(vital_stats) + ' ' + str(verbose) + ' ', flush=True)
    print('Thread identity: ' + str(threading.get_ident()))

    if vital_stats: print('Thread identity: ' + str(threading.get_ident()) + " Starting with " + main_folder + " and " + combo_var[main_folder] + " containing " + str(xmp_tracker[main_folders.index(main_folder)][1]) + " xmp files.")

    md5_OK              = 0
    md5_NOK             = 0
    md5_not_found       = 0
    md5_missing_raw     = 0
    xmp_file_counter    = 0
    results             = []
    time1               = time.time()

    try:                        # Clear db here from all rows with path
        sql = "DELETE FROM md5_results WHERE file_path LIKE '" + main_folder + "%'"
        cur.execute(sql)
        if verbose: print("Thread identity: " + str(threading.get_ident()) + " Executed sql: " + sql)
        if verbose: print("Thread identity: " + str(threading.get_ident()) + " First sql segment: Rows returned from execute  = " + str(cur.rowcount), flush=True)
        conn.commit()
    except sqlite3.Error as error:
        if print_errors: print("Thread identity: " + str(threading.get_ident()) + " Failed to delete record from sqlite table", error, flush=True)


    try:   # Update dashboard since I've removed all files for folder main_folder.
        cur.execute("UPDATE dashboard SET last_run = ?, tot_xmp = ?, ok_xmp = ?, nok_xmp = ?, missing_raw = ? WHERE main_path = '" + main_folder + "'",
                    (todays_date, 0, 0, 0, 0))
        if verbose: print(" Thread identity: " + str(threading.get_ident()) + "First sql segment: Rows returned from execute UPDATE dashboard = " + str(cur.rowcount), flush=True)
        conn.commit()
    except sqlite3.Error as error:
        if print_errors: print(" Thread identity: " + str(threading.get_ident()) + "Failed to UPDATE dashboard from sqlite table", error, flush=True)

    time2 = time.time()
    for subdir, dirs, files in os.walk(main_folder):
        for file in files:
            found_raw = 0
            try:
                if file.endswith('xmp'):
                    xmp_file_counter +=1
                    if verbose: print ('Found file: ' + file, flush=True)
                    f = open(subdir+'\\'+ file,"r")
                    list_file = list(f)
                    md5_index_tmp = index_containing_substring(list_file, '<PelleTags:PelleTag1_md5sum>')
                    if md5_index_tmp == 0:
                        md5_index = [0, index_containing_substring(list_file, 'PelleTags:PelleTag1_md5sum=')]
                    else:   
                        md5_index = [md5_index_tmp,0]

                    if verbose: print(md5_index)

                    if any(md5_index):    # xmp-filen innehåller en md5-summa.
                        res = [idx for idx, val in enumerate(md5_index) if val != 0] # Ger vilken typ av xmp encoding det är.
                        md5_xmp = md5_index[res[0]]
                        for raw_file in os.listdir(subdir):    # Find the corresponding RAW-file to generate md5 sum.
                            if file[:-3] in raw_file[:-3]: # Här slicar jag bort ändelserna för att se om de har samma namn.
                                if raw_file[-3:].upper() in raw_extensions:
                                    found_raw = 1
                                    md5_calculated = md5Checksum(subdir + '\\' + raw_file)
                                    if verbose: print ('Calculated md5 for file ' + raw_file)
                                    if verbose: print (md5_calculated)
                                    if md5_calculated == md5_xmp:
                                        results.append((subdir, file, md5_xmp, md5_calculated, 'OK', todays_date))
                                        md5_OK +=1
                                        if verbose: print("md5 stämmer " + " subdir " + subdir + " file " + file)
                                    else:
                                        results.append((subdir, file, md5_xmp, md5_calculated, 'NOK', todays_date))
                                        md5_NOK +=1
                                        if print_errors: print("md5 fail: " + subdir + "\\"  +  str(raw_file))
                                        
                                    break

                        if not found_raw:  # Efter break exekveras denna. Tror jag...
                            if print_errors: print("xmp without matching raw: " + subdir + "\\"  +  str(raw_file))
                            results.append((subdir, file, 'No valid raw file found', '-', 'NOK', todays_date))
                            md5_missing_raw +=1

                    else: # index_containing_substring returns zero, PelleTags not present in xmp-file
                        if print_errors: print("Error, no md5 sum in file " + subdir + "\\" + file)
                        md5_not_found += 1
                        results.append((subdir, file, 'No md5 in xmp', md5_calculated, 'NOK', todays_date))

                    f.close()

                    if xmp_file_counter % limited_printouts == 0:
                        if vital_stats: print("Thread identity: " + str(threading.get_ident()) + ", " + str(xmp_file_counter) + " xmp-files processed in "
                                + str(round(time.time()-time1)) + " seconds, delta time " + str(round(time.time()-time2)) + " seconds, local time " +
                                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                        time2 = time.time()
                        

            except:
                if print_errors:
                    print ('Unexpected fail for file: ' + file)
                    print (sys.exc_info())
                f.close()

    try:
        cur.executemany("INSERT INTO md5_results ('file_path', 'file_name', 'md5_file', 'md5_calc', 'ok_nok', 'date') VALUES (?,?,?,?,?,?)", results)
        if vital_stats: print("Thread identity: " + str(threading.get_ident()) + " Second sql segment: Rows returned from execute INSERT INTO md5_resutls = "
                              + str(cur.rowcount))
    except sqlite3.Error as error:
        if print_errors: print("Thread identity: " + str(threading.get_ident()) + " Failed to INSERT INTO md5_results sqlite table", error)

    try:
        cur.execute("UPDATE dashboard SET last_run = ?, tot_xmp = ?, ok_xmp = ?, nok_xmp = ?, missing_raw = ?, missing_xmp = ? WHERE main_path = '" + main_folder + "'",
                (todays_date, md5_OK+md5_NOK, md5_OK, md5_NOK,md5_missing_raw,md5_not_found))
        if vital_stats: print("Thread identity: " + str(threading.get_ident()) + " Second sql segment: Rows returned from execute UPDATE dashboard = " + str(cur.rowcount))
    except sqlite3.Error as error:
        if print_errors: print("Thread identity: " + str(threading.get_ident()) + " Failed to UPDATE dashboard from sqlite table", error)

    if vital_stats: print("Thread identity: " + str(threading.get_ident()) + " Run results for path: " + main_folder + " md5_OK=" + str(md5_OK) + " md5_NOK=" +
                str(md5_NOK) + " md5__not_found=" + str(md5_not_found) + " md5_missing_raw=" + str(md5_missing_raw) + ", in " + str(round(time.time()-time1)) +
                " seconds, finished at " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ".")


def runrunrun():
    global combo
    global combo_var
    global master

    for key, value in combo.items():
        combo_var[key] = combo[key].get() #combo values gets destroyed when closing GUI, therefore copy values.

    master.destroy()  # Close GUI and continue after mainloop

def quitquit():
    conn.close()
    exit() 

def xmp_count():
    # Check how many xmp files there are in each main folder.
    global main_folders
    global xmp_tracker
    global verbose
    global xmp_tracker

    xmp_file_count  = 0

    for main_folder in main_folders:
        for subdir, dirs, files in os.walk(main_folder):
            for file in files:
                if file[-3:] == 'xmp':
                    xmp_file_count += 1
        xmp_tracker.append([main_folder,xmp_file_count])
        if vital_stats: print(main_folder + " has " + str(xmp_file_count) + " xmp files")
        xmp_file_count = 0

def build_dashboard():
    # Build dashboard
    # Creating main tkinter window/toplevel
    global dashboard
    global main_folders
    global combo
    global combo_var
    global xmp_tracker
    global verbose

    global master

    date_format = "%Y-%m-%d"
    todays_date = datetime.date.today().strftime(date_format)


    max_width = max(len(x) for x in main_folders)  # needed to size the cell with path
    # this will create a label widget 
    col_1 = Label(master, relief=RIDGE,  text  = "Folder path", width = max_width) 
    col_2 = Label(master, relief=RIDGE,  text  = "Last run", width = 12)
    col_3 = Label(master, relief=RIDGE,  text  = "Days since last run", width = 18)
    col_4 = Label(master, relief=RIDGE,  text  = "Tot last count xmp") 
    col_5 = Label(master, relief=RIDGE,  text  = "Tot db xmp") 
    col_6 = Label(master, relief=RIDGE,  text  = "OK xmp") 
    col_7 = Label(master, relief=RIDGE,  text  = "NOK xmp") 
    col_8 = Label(master, relief=RIDGE,  text  = "Missing RAW") 
    col_9 = Label(master, relief=RIDGE,  text  = "Missing xmp") 
    col_10 = Label(master, relief=RIDGE,  text  = "Start/Restart") 

    # grid method to arrange labels in respective 
    # rows and columns as specified 
    col_1.grid(row = 0, column = 0, sticky = W, pady = 2) 
    col_2.grid(row = 0, column = 1, sticky = W, pady = 2) 
    col_3.grid(row = 0, column = 2, sticky = W, pady = 2) 
    col_4.grid(row = 0, column = 3, sticky = W, pady = 2) 
    col_5.grid(row = 0, column = 4, sticky = W, pady = 2)
    col_6.grid(row = 0, column = 5, sticky = W, pady = 2) 
    col_7.grid(row = 0, column = 6, sticky = W, pady = 2) 
    col_8.grid(row = 0, column = 7, sticky = W, pady = 2)
    col_9.grid(row = 0, column = 8, sticky = W, pady = 2)
    col_10.grid(row = 0, column = 9, sticky = W, pady = 2)

    for ii, each_row in enumerate(dashboard):
    #    print(each_row)
    #    print(ii)
        col_1 = Label(master, text = each_row[1]) 
        col_2 = Label(master, text = each_row[2])
        col_3 = Label(master, text = (datetime.datetime.strptime(todays_date, date_format)- datetime.datetime.strptime(each_row[2], date_format)).days)
        col_4 = Label(master, text = xmp_tracker[ii][1])
        col_5 = Label(master, text = each_row[3]) 
        col_6 = Label(master, text = each_row[4])
        col_7 = Label(master, text = each_row[5]) 
        col_8 = Label(master, text = each_row[6])   
        col_9 = Label(master, text = each_row[7])   

        col_1.grid(row = ii+1, column = 0, sticky = W, pady = 5, padx = 5) 
        col_2.grid(row = ii+1, column = 1, sticky = W, pady = 5, padx = 5) 
        col_3.grid(row = ii+1, column = 2, sticky = W, pady = 5, padx = 5)
        col_4.grid(row = ii+1, column = 3, sticky = W, pady = 5, padx = 5) 
        col_5.grid(row = ii+1, column = 4, sticky = W, pady = 5, padx = 5) 
        col_6.grid(row = ii+1, column = 5, sticky = W, pady = 5, padx = 5)
        col_7.grid(row = ii+1, column = 6, sticky = W, pady = 5, padx = 5)
        col_8.grid(row = ii+1, column = 7, sticky = W, pady = 5, padx = 5)
        col_9.grid(row = ii+1, column = 8, sticky = W, pady = 5, padx = 5)
    
    
    valores=("Do nothing", "Restart", "New run")

    # key_name[1] innehåller path som blir key i dict, och värdet blir det man valt i drop down.
    for index, key_name in enumerate(dashboard):
        combo[key_name[1]] = ttk.Combobox(master, values=valores)
        combo[key_name[1]].set("Do nothing ")
        combo[key_name[1]].grid(row = 1+index, column = 9, sticky = W, pady = 6, padx = 5)

    # button widget
    b1 = Button(master, text = "Cancel", width = 9, command=quitquit) 
    b2 = Button(master, text = "Go", width = 9, command=runrunrun) 
    # arranging button widgets 
    b1.grid(row = ii+2, column = 9, sticky = W) 
    b2.grid(row = ii+2, column = 9, sticky = E) 

    # infinite loop which can be terminated  
    # by keyboard or mouse interrupt 
    mainloop() 


def get_list_of_folders(main_folders_2):
    tmp = []
    tmp.append(main_folders_2[0])
    for ii in range(len(main_folders_2)):
        if main_folders_2[ii] not in tmp and main_folders_2[ii][0] not in [item[0] for item in tmp]:
            tmp.append(main_folders_2[ii])

    return tmp



def run_thru_folders():
    global dashboard
    global main_folders
    global combo
    global combo_var
    global verbose
    global vital_stats
    global cur

    
    new_run_folders  = []
    current_run_list = []
    l3               = []


    for main_folder in main_folders:
        if combo_var[main_folder] == "New run":
            new_run_folders.append(main_folder)
        else:
            if vital_stats: print("For folder " +  main_folder + ": " + combo_var[main_folder])

    if vital_stats: print('new_run_folders: ')
    if vital_stats: print(new_run_folders)

    while new_run_folders:
        current_run_list = get_list_of_folders(new_run_folders)
        if vital_stats: print('current_run_list: ')
        if vital_stats: print(current_run_list)

        if l3 is not None:
            l3 = [x for x in new_run_folders if x not in current_run_list]
            new_run_folders = l3

        iii = 0
        thread_list = []
        for current_folder in current_run_list:
            thread_list.append(threading.Thread(target=folderThread, args=(current_folder,)))
 
            # Starting threads 
            thread_list[iii].start()
            print('Startat thread number ' + str(iii))
            print("Base identity: " + str(thread_list[iii]) + " ")
            time.sleep(3) # Think this is needed to give time to db transactions at the start of a run.
            iii += 1
  
        for xxx in range(iii):
            thread_list[xxx].join()


verbose             = 1
vital_stats         = 1
limited_printouts   = 1000
print_errors        = 1
md5_index           = []
xmp_tracker         = []
combo               = {}
combo_var           = {}
todays_date         = str(datetime.date.today())
raw_extensions      = ['CR2','NEF','3FR','ARW','SRF','SR2','CRW','IIQ','EIP','DCR','K25','KDC','ERF','MEF','MOS','MRW','NRW',
                       'ORF','PEF','RAF','RAW','RW2','RWL','RWZ','X3F','MOV','MP4','AVI','WMV','M4V','MPG','3GP','3G2']

#conn = sqlite3.connect('C:\Pelle\Dashboard_Python\dashboard_md5.sql3', check_same_thread=False)  # LeanMean
#conn = sqlite3.connect('G:\PelleHack\Python_Dashboard\dashboard_md5.sql3', check_same_thread=False) # W12

conn = connect_sqlite_db()
cur = conn.cursor()
cur.execute("SELECT * FROM dashboard")
dashboard = cur.fetchall()
#print(dashboard)
main_folders = [dashboard[i][1] for i in range(len(dashboard))]  # Extract the paths to its own list.
print(main_folders)

xmp_count()

master = Tk()

build_dashboard()
run_thru_folders()

conn.commit()
conn.close()
    
