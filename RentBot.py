#! python3

import pyautogui, sys, os, re, time
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from decimal import Decimal


def amtGet():
    rgx = re.compile(r"^[1-9][0-9]*(?:\.\d{,2})?$") # First digit must be between 1 and 9, followed by unlimited digits between 0 and 9, followed by a period, followed by any two digits
    try:
        amtTxtFile = open('rent_amount.txt', 'r')
        line = amtTxtFile.read()
        if rgx.match(line):
            amt = Decimal(line)
            return amt
        else:
            pyautogui.confirm('Rent amount not found', title='RentBot - Amount Missing')
            sys.exit()
    except FileNotFoundError:
        pyautogui.confirm("Text file 'rent_amount.txt' not found", title='RentBot - File Missing')
        sys.exit()

def daysDueGet():
    dt = datetime.now()
    lastDayToPay = ((dt.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)) # Replace Now's day with day 1 of that month. Add 32 days to go to next month, then replace that month's day with day 1. Minus one day = lastDayToPay (number of days until rent is due)
    daysDue = (lastDayToPay) - (datetime.now())
    daysDue = daysDue.days # Number of days until rent is due
    return daysDue
        
def rentAsk(amt, daysDue):
    nextMonthAlpha = (datetime.now() + relativedelta(months=1)).strftime('%B') # Define next month (alpha word string i.e. 'July')
    yes = ['yes','y']
    no = ['no','n']
    while True:
        choice = pyautogui.prompt('Your rent of $' + str(amt) + '\n\nfor the month of '+nextMonthAlpha+' is due in: \n\n' +str(daysDue)+ ' days\n\nHave you paid your rent yet?')
        if choice == None or choice.lower() in no:
            askTomorrow(daysDue)
        elif choice.lower() in yes:
            pyautogui.alert('Good job!', title='RentBot Completed')
            sys.exit()
        else:
            continue

def askTomorrow(daysDue):
    if daysDue != 1:
        pyautogui.alert('Ok, I will ask you again tomorrow.', title='RentBot Aborted')
        tomorrow = (datetime.now() + relativedelta(days=1))
        while datetime.now() < tomorrow:
            time.sleep(1)
            continue
    else:
        pyautogui.alert('Today is the last day to pay your rent. If you do not pay it today, it will be LATE!', title='LATE WARNING')
        sys.exit()

def rent_increase(amt, daysDue):
    while True:
        rgx = re.compile(r"^[1-9][0-9]*(?:\.\d{,2})?$") # First digit must be between 1 and 9, followed by unlimited digits between 0 and 9, followed by a period, followed by any two digits
        result = pyautogui.prompt('This rent amount will be different due to the\n\nAUGUST RENT INCREASE!\n\nPlease enter your new rent amount:')
        if result == None:
            askTomorrow(daysDue)
        elif rgx.match(result):
            newAmt = Decimal(result.strip())
            if newAmt > amt:
                break
            else:
                pyautogui.alert("New rent amount should (unfortunately) be greater than old rent amount", title='Invalid New Rent Amount')
                continue
        else:
            continue
    with open('rent_amount.txt', 'w') as out:
        out.write("%2.2f" % newAmt)
    pyautogui.alert('Thanks presentformyfriends! Your new rent amount of $'+str("%2.2f" % newAmt)+' has been saved.', title='New Rent Amount Saved')
    rentAsk(newAmt, daysDue)
    

username = os.getlogin()
os.chdir('C:\\Users\\'+username+'\\RentBot\\') # Set working directory
    
### MAIN ###
nextMonth = (datetime.now() + relativedelta(months=+1)).strftime('%m') # Define next month (two-digit string i.e. '05')
amt = amtGet()
daysDue = daysDueGet()
if nextMonth != '08':
    rentAsk(amt, daysDue)
else:
    rent_increase(amt, daysDue)
