# Bradly Felix
from os import path
from urllib.request import urlretrieve
import re;

URL = 'https://s3.amazonaws.com/tcmg476/http_access_log'
logfile = 'accesslog.log'
total_requests = 0
past_year_requests = 0
unsuccessful_requests = 0
redirected_requests = 0
past_year = '/1995'
days = {}
weeks = {}
months = {}
filenames = {}

if path.exists('accesslog.log') == False:
    
    print("Parsing log file, please wait:")
    logfile, headers = urlretrieve(URL, logfile, lambda x,y,z: print('.', end='', flush=True) if x % 100 == 0 else False)

with open("accesslog.log") as fh:
    Lines = fh.readlines()
    for line in Lines:
        
        total_requests += 1
        
        if past_year in line:
            past_year_requests += 1
               
            if '403 -' in line or '404 -' in line:
                unsuccessful_requests += 1
            
            if '302 -' in line:
                redirected_requests += 1
        
        result = re.split('.+ \[(.+) .+\] "[A-Z]{3,5} (.+) HTTP/1.0" ([0-9]{3})', line)
        
        if len(result) == 5:
            date = result[1]
            file = result[2]
            
            date = date.split(':')
            if date[0] in days:
                days[date[0]] += 1
            else:
                days[date[0]] = 1
             
            date[0] = date[0].split('/')
            if date[0][1] + " " + date[0][2] in months:
                months[date[0][1] + " " + date[0][2]] += 1
            else:
                months[date[0][1] + " " + date[0][2]] = 1
            
            if file in filenames:
                filenames[file] += 1
            else:
                filenames[file] = 1
            
print("Question 1")
print("Requests per day: ")
for key, value in days.items():
    print(str(key) + ": " + str(value))

print("Question 2")
print("Number of requests per month: ")
for key, value in months.items():
    print(str(key) + ": " + str(value))

print("Questions 3 & 4")
print("Percentage of Unsuccessful requests: " + str(unsuccessful_requests) + " or " + str(round((unsuccessful_requests / total_requests) * 100, 2)) + "% of requests")
print("Percentage of Request redirected: " + str(redirected_requests) + " or " + str(round((redirected_requests / total_requests) * 100, 2)) + "% of requests")

print("Questions 5 & 6")
print("Most requested file: " + str(list(filenames.keys())[0]))
print("Least requested file: " + str(list(filenames.keys())[-1]))