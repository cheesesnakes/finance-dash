# a script to correctly format data from a csv named acc_stat

import csv
import os
import re

# open the csv file

with open('acc_stat.csv', 'r') as file:
    # read the csv file
    
    reader = csv.reader(file)
    
    # create a new csv file to write the data
    
    with open('cleaned_acc_stat.csv', 'w') as new_file:
        
        # write the data to the new csv file
        
        writer = csv.writer(new_file)
        
        # write the header
        
        writer.writerow(['date', 'description', 'debit', 'credit', 'balance', 'account']) 
        
        # skip the header
        next(reader)
           
           # loop through the data
           
        for row in reader:
               
            # get the date
            
            date = row[0]
            
            # conver dd/mm/yy to yyyy-mm-dd
            
            if '/' in date:
                
                date = date.split('/')
                
                # if date[2] > 4 digits, drop extra digits
                
                if len(date[2]) > 4:
                    
                    date[2] = date[2][0:3]
                
                if len(date[2]) < 4:

                    # if date[2] < 4 digits, add 20 to the year
                    
                    date[2] = '20' + date[2]
            
                date = date[2].strip() + '-' + date[1].strip() + '-' + date[0].strip()
            
            elif ' ' in date:
                
                date = date.split(' ')
                
                # conver Jul to 07
                
                if date[1] == 'Jul':
                    date[1] = '07'
                elif date[1] == 'Jun':
                    date[1] = '06'
                    
                # add more conditions for other months if needed
                
                
                
                date = date[2] + '-' + date[1] + '-' + date[0]
            
            # else if the date is already in the correct format
            
            else:
                
                date = date.split('-')
                
                if len(date[2]) < 4:

                    # if date[2] < 4 digits, add 20 to the year
                    
                    date[2] = '20' + date[2]
                
                date = date[2] + '-' + date[1] + '-' + date[0]
                
            # remove blank spaces from the date
            
            date = date.strip()
            
            # format debit, credit and balance as numbers using regex to remove other characters except . and digits
            
            debit = re.sub(r'[^\d.]', '', row[2])
            
            credit = re.sub(r'[^\d.]', '', row[3])
            
            balance = re.sub(r'[^\d.]', '', row[4])
            
            # write the data to the new csv file
            
            writer.writerow([date, row[1], debit, credit, balance, row[5]])

                                        
    
    
    
    
