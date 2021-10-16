import os
import sys
import datetime

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

def WriteToPipe(ls):
    p= open("/tmp/cald_pipe","w")

    string=""
    for x in range(len(ls)):
        """
        if x < 2: string += ls[x]
        else: string += f'"{ls[x]}"'
        """
        string += ls[x]
        string += " " if x < len(ls) -1 else ""
    p.write(string)
    p.close()

def isInsideBoth(ls,word, index):
    for x in ls:
        temp = Split(",", word)
        if x == temp[index]:  return True
    return False


def PrintResults(ls):
    for x in ls:
        temp = Split(",", x)
        for y in range(len(temp)):
            if y != 2:
                print(temp[y].replace("\n",""),end=" : ")
            else:
                print(temp[y].replace("\n",""),end="")
        print()

def Date(path, dates):
    db=open(path,"r")
    lines = db.readlines()
    db.close()
    results = []
    for x in lines:
        if isInsideBoth(dates, x, 0):  results.append(x)

    PrintResults(results)

def Name(path, names):
    db=open(path,"r")
    lines = db.readlines()
    db.close()
    results = []
    for x in lines:
        if isInsideBoth(names,x, 1):  results.append(x)

    PrintResults(results)

def Interval(path,dates):
    db=open(path,"r")
    lines = db.readlines()
    db.close()

    results = []
    
    tmp1 = dates[0].split("-")
    tmp2 = dates[1].split("-")

    d_min = datetime.date(int(tmp1[2]),int(tmp1[1]),int(tmp1[0]))
    d_max = datetime.date(int(tmp2[2]),int(tmp2[1]),int(tmp2[0]))

    for x in lines:
        record = Split(",", x)
        tmp = record[0].split("-")
        d = datetime.date(int(tmp[2]),int(tmp[1]),int(tmp[0]))

        if d_min <= d <= d_max:  results.append(x)

    PrintResults(results)
    

def CheckDates(dates):
    for x in dates:
        if not isDate(x):  return False
    return True

def FindEvent(db_path,query): 
    db=open(db_path,"r")
    lines = db.readlines()
    db.close()

    results = []    

    for x in lines:
	    if query[0] in x and query[1] in x: results.append(x)

    return results
	 
def PrintStdErr(ls):
    for x in ls: print(x,file=sys.stderr)

def run():
    c_link ="/tmp/calendar_link" 
    if os.path.exists(c_link): 
        #check if file is empty?
        t = open(c_link, "r")
        db_path = t.readline()
        t.close()

        err = []
        db=open(db_path,"r")
        if len(sys.argv) >= 2:
            if sys.argv[1].lower() == "get":
                if len(sys.argv) >=3:
                    if sys.argv[2].lower() == "date":
                        if len(sys.argv) == 3:
                            err.append("Unable to parse date")
                        else:
                            if not CheckDates(sys.argv[3:]): err.append("Unable to parse date")

                            else:  Date(db_path,sys.argv[3:])

                    elif sys.argv[2].lower() == "interval":
                        if len(sys.argv) ==5:
                            if not CheckDates(sys.argv[3:]): err.append("Unable to parse date")
                            else:
                                tmp1 = sys.argv[3].split("-")
                                tmp2 = sys.argv[4].split("-")
                                if datetime.date(int(tmp2[2]),int(tmp2[1]),int(tmp2[0])) <=  datetime.date(int(tmp1[2]),int(tmp1[1]),int(tmp1[0])): 
                                    err.append("Unable to process Start date is after End date")
                                if len(err) == 0 : Interval(db_path, sys.argv[3:])
                    elif sys.argv[2].lower() == "name":
                        if len(sys.argv) == 3:
                            err.append("Please Specify an argument")
                        else:
                            Name(db_path, sys.argv[3:])

                    else: err.append("Multiple errors occur")
                else: err.append("Multiple errors occur")
            elif sys.argv[1].lower() == "add":
                if len(sys.argv) == 3: 
                    err.append("Missing event name")
                if not isDate(sys.argv[2]): err.append("Unable to parse date")

                if len(sys.argv) == 4 or len(sys.argv) ==5:
                    if sys.argv[3] == "": err.append("Missing event name")
                    if not isDate(sys.argv[2]): err.append("Unable to parse date")

                    if len(err) == 0:
                        WriteToPipe(sys.argv[1:])

                else:err.append("Multiple Errors occur")
            elif sys.argv[1].lower() == "upd":

                if len(sys.argv) < 4: err.append("Not enough events given")

                if len(sys.argv) == 5 or len(sys.argv) ==6:
                    if not isDate(sys.argv[2]): err.append("Unable to parse date")

                    if len(FindEvent(db_path, sys.argv[3])) == 0: err.append("Unable to update event doesn't exist")
                    if len(err) ==0: WriteToPipe(sys.argv[1:])
                else: err.append("Multiple errors occur")
            elif sys.argv[1].lower() == "del":
                if len(sys.argv) ==4:
                    if not isDate(sys.argv[2]): err.append("Unable to parse date")

                    if sys.argv[3] == "": err.append("Missing event name")

                    if len(err) == 0:  WriteToPipe(sys.argv[1:])
                else: err.append("Missing event name")
        else:  err.append("Multiple errors occur")
#            else: err.append("Multiple errors occur")
        if len(err) >0: PrintStdErr(err)
        db.close()

    else:
        print("Database doesn't exists")
        pass

if __name__ == '__main__':
    run()

