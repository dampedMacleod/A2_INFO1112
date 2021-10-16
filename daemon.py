#!/bin/python

import signal
import os
import sys

#Use this variable for your loop
daemon_quit = False

#Do not modify or remove this handler
def quit_gracefully(signum, frame):
    global daemon_quit
    daemon_quit = True

db_path = ""

def Count(delim,string):
    results = []
    count =0
    for x in string:
        if x == delim:  results.append(count)
        count +=1
    return results

def ReplaceDelim(start,end, ls,delim):
    for x in range(start,end):
        if ls[x] == delim:  ls[x] = '"'
    return ls

def Split(delim,target):
    ls=Count('"',target)
    if len(ls) % 2 != 0:
        print("Invalid quotations number of quotations")
    else:
        results= list(target)
        delim_exceptions= []
        for x in range(len(ls)//2):  
            results = ReplaceDelim(ls[2*x],ls[1+2*x],results,delim)

        for x in ls:  results[x] = ""

        string = ""

        for x in results: string+=x

        temp = string.split(delim)

        final_ls = [i.replace('"',delim) for i in temp]

        return final_ls

def IsValidDay(date):
    months_days = {"01": 31, "03": 31,"04": 30,"05": 31,"06": 30,"07": 31,"08": 31,"09": 30,"10": 31,"11": 30,"12": 31}
    if date[1] == "02":
        if int(date[2]) % 4 ==0:
            if 0 < int(date[0]) <= 29:  return True
            else: return False
        else:
            if 0 < int(date[0]) <= 28:  return True
            else: return False
    else:
        if date[1] in months_days:
            if 0 < int(date[0]) <= months_days[date[1]]:return True
            else: return False
        else: return False
        

def isDate(date):
    ls = date.split("-")
    d_struc = [2,2,4]
    if len(ls) !=3: return False
    else:
        for x in range(len(ls)):
            if ls[x].isdigit():
                if len(ls[x]) != d_struc[x]:  return False
            else: return False
        return IsValidDay(ls)

def WriteToFile(lines, path):
    f = open(path, "w")
    string = ""
    for l in lines:
        string += l
    f.write(string)
    f.close()

def Remove(args, path):
    f = open(path, "r")
    lines = f.readlines()
    print(args)
    f.close()
    dates = []
    n_dates = []
    for x in lines:
        if args[0] in x and args[1] in x:
            continue
        else: dates.append(x)
    WriteToFile(dates, path)



def Add(args, path):
    f = open(path,"a")
   
    for x in range(len(args)):
        f.write(args[x])
        if x != len(args)-1:f.write(",")
        else: f.write("\n")
    f.close()

def CreateDB(path):
    open(path, "a").close()

    t = open("/tmp/calendar_link","w")
    t.write(path)

    t.close()
    return path

def updDB(args,path):
    f = open(path, "r")
    lines = f.readlines()
    f.close()
    n_dates = []

    for x in range(len(lines)):
        if args[1] in lines[x] and args[0] in lines[x]:
            temp = lines[x].split(",")
            temp[1] = temp[1].replace(args[1], args[2])
            if len(temp) ==3 and len(args) ==4: temp[2] = f"{args[3]}\n"
            string = ""
            for i in range(len(temp)):
                string += temp[i]
                if i != len(temp) -1: string += ","
            n_dates.append(string)

        else: n_dates.append(lines[x])

    WriteToFile(n_dates, path)
    pass

def run():
    #Do not modify or remove this function call
    signal.signal(signal.SIGINT, quit_gracefully)

    # Call your own functions from within 
    # the run() funcion

    path = "/tmp/cald_pipe"

    if not os.path.exists(path):  os.mkfifo(path)
    else:
        os.unlink(path)
        os.mkfifo(path)

    
    if len(sys.argv) ==2:
        db_path = CreateDB(sys.argv[1])
    else:
        db_path = CreateDB(os.getcwd() + "/cald_db.csv")

    while not daemon_quit:
        p = open(path,"r")
        line = p.read().replace("\n","")
        temp = line.split(" ")
        if len(temp) >=3:
            if temp[0].lower() == "add":
                if len(temp) == 3 or len(temp) ==4:
                    if isDate(temp[1]):
                        Add(temp[1:], db_path)
                    else: print("invalid Date")
                
                else: print("Invalid args in add")

            elif temp[0].lower() == "del":
                if len(temp) == 3:
                    if isDate(temp[1]):
                        Remove(temp[1:],db_path)
                    else: print("Invalid date")
                else: print("Invalid delete args")

            elif temp[0].lower() == "upd":
                if len(temp) == 4 or len(temp) == 5:
                    updDB(temp[1:],db_path)
                    pass
            else:
                print("Invalid command")
        else: print("Invalid args")
    pass
if __name__ == '__main__':
    run()
