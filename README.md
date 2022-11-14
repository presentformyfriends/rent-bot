# Rent Bot
Python script due date reminder to pay your rent. 

## :calendar: Usage

The rent amount is stored in a text file that the script reads from. 

Since my rent increases every August, the script reminds me of the rent increase if the next month will be August, and prompts me to enter the new increased rent amount. It then overwrites the rent amount in the text file with the new rent amount, and saves the change.

I use Task Scheduler to run the script on the 25th day of every month.

On the 25th of every month, the script opens a dialog box and asks if I have paid my rent yet.

If I answer Yes/y/, it tells me "Good job" and exits.

If I answer No/n (or if I close the dialog box), the script waits until the next day and asks me again. However, if it is the last day to pay my rent on time, then the script produces a dialog box with a warning that it is the last day to pay, and then exits.

## :snake: Dependencies

This script uses the following Python modules:  pyautogui, sys, os, re, time, datetime, relativedelta, decimal

This script was designed to be scheduled to run (I use Task Scheduler for this).
