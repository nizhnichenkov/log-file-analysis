# @author   Svetoslav Nizhnichenkov
# @email    svetoslav.nizhnichenkov@ucdconnect.ie
# @ID       17712081
'''
    Program to analyse access log files.

    What it does:
        1. Given a log file - outputs the number of unique IP addresses
        2. Lists the top N IP addresses ( the ones with the most requests )
        3. Given an IP - displays the number of visits for that IP
        4. Given an IP - gives a number representing all the requests made by that IP
        5. Given a date - outputs all the IPs and the visits they've made for that date
'''


import sys
import getopt
from collections import OrderedDict
from operator import itemgetter
import re


def uniqueIPAddresses(fileName):
    '''
    Count the number of unique IP addresses in a file
    '''
    f = open(fileName, "r")
    lst = []

    ip_regex = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

    # add all IP addresses to a list
    for line in f:
        if re.search(ip_regex, line):
            lst.append(line)

    uniqueIP = []

    # split the line, only save the IP address
    for i in lst:
        y = i.split()
        uniqueIP.append(y[0])

    # remove all duplicates from uniqueIP
    uniqueIP_set = set(uniqueIP)

    # convert the set back to a list
    uniqueIP = list(uniqueIP_set)

    uniqueIPtotal = 0
    for i in uniqueIP:
        uniqueIPtotal += 1

    f.close()

    print(uniqueIPtotal)


def topNipAddresses(fileName, number):
    '''
    List top N IP addresses according to number of requests
    '''

    f = open(fileName, "r")
    lst = []

    ip_regex = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

    # add all IP addresses to a list
    for line in f:
        if re.search(ip_regex, line):
            lst.append(line)

    # # add all IP addresses to a list
    # for line in f:
    #     lst.append(line)

    totalIP = []

    # split the line, only save the IP address
    for i in lst:
        y = i.split()
        totalIP.append(y[0])

    # sort all IP addresses
    totalIP.sort()

    # create an empty dictionary
    freq = {}

    # sort items by frequency of requests
    for item in totalIP:
        if item in freq:
            freq[item] += 1
        else:
            freq[item] = 1

    # sort dictionary of frequencies
    # in descending order according to value ( frequency )
    sortedFreq = OrderedDict(
        sorted(freq.items(), key=itemgetter(1), reverse=True))

    # delete all the occurrences of '::1'
    # since it's not listed as an answer
    # in the assignment requirements
    for key in sortedFreq:
        if key in '::1':
            del sortedFreq[key]

    # run a for loop to dispaly the first N IP addresses
    # with the highest frequency of requests
    nmbr = int(number)
    counter = 0
    print('{:15}    {:}'.format('IP', 'Requests'))
    for key, value in sortedFreq.items():
        if counter == nmbr:
            break
        print('{:15}    {:}'.format(key, value))
        counter += 1

    f.close()


def listAllRequests(fileName, ip):
    '''
    Lists all the requests made by an IP address
    given as argument by the user
    '''

    # open file for reading
    f = open(fileName, "r")

    # list all the requests made by an ip address
    for line in f:
        # split line, as we only need to compare IP addresses
        # we do not want to compare just a part of it ( substring )
        y = line.split()
        if ip == y[0]:
            print(line)

    # close file
    f.close()


def numOfVisits(fileName, IP):
    '''
    Outputs the number of visits given an IP
    '''
    f = open(fileName, "r")

    lst = []
    visits = 0

    # add all lines containing the IP address
    # in lst
    for line in f:
        y = line.split()
        if IP == y[0]:
            lst.append(line)

    for i in range(0, len(lst)-1):

        # if the IP address has only made one request
        # that would be 1 visit
        if len(lst) == 1:
            visits += 1
            break

        # save only date index in variables x and y
        # y saves the (i+1)th date index
        x = lst[i].split()[3].split('/')[0]
        y = lst[i+1].split()[3].split('/')[0]

        x = x.split('[')
        y = y.split('[')

        # if requests have been made on a different date
        # increment visits
        if int(x[1]) != int(y[1]):
            visits += 1

        # if requests have been made on the same date
        # check if the month is the same, if it is,
        # check if time between requests is > 1 hour,
        # if month is not the same, increment visits
        if int(x[1]) == int(y[1]):
            month = lst[i].split()[3].split('/')[1]
            month2 = lst[i+1].split()[3].split('/')[1]

            month = month.split('[')
            month2 = month2.split('[')

            # if months are different
            # increment visits
            if month[0] != month2[0]:
                visits += 1

            # if months are the same
            # check hour difference
            if month[0] == month2[0]:

                hours = float(lst[i].split()[3].split(':')[1]) * 60
                minutes = float(lst[i].split()[3].split(':')[2])
                seconds = float(lst[i].split()[3].split(':')[3]) * (1/60)
                res = hours + minutes + seconds

                hours2 = float(lst[i+1].split()[3].split(':')[1]) * 60
                minutes2 = float(lst[i+1].split()[3].split(':')[2])
                seconds2 = float(lst[i+1].split()[3].split(':')[3]) * (1/60)
                res2 = hours2 + minutes2 + seconds2

                result = abs(res - res2)

                # if hour difference is greater than 1 hour
                # increment visits
                if result > 60.0:
                    visits += 1

    # we're not taking into account the very last request when
    # we're running the for loop, which means we're losing 1 visit
    # so we must update the visits variable
    if len(lst) == 0:
        visits = 0

    elif len(lst) != 0:
        visits += 1

    # output # of visits
    print(visits)
    f.close()


def numOfVisitsOnDate(fileName, date):
    '''
    List number of visits of all the requests on a specific date
    '''
    f = open(fileName, "r")

    lst = []

    ip_regex = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

    # check every request against the date given as command line argument
    # if both dates match, save the current line in a list
    for line in f:
        x = line.split()[3].split('[')[1].split(':')[0].split('/')
        y = x[0] + x[1] + x[2]

        if date == y:
            if re.search(ip_regex, line):
                lst.append(line)

    # sort the list
    lst.sort()

    # make a list with unique IP addresses
    unique_ip = []
    for i in lst:
        x = i.split()
        unique_ip.append(x[0])

    uniqueIPSet = set(unique_ip)
    unique_ip = list(uniqueIPSet)

    # a list to hold the visits for each IP
    visitFreq = []

    # check each ip in unique_ip against all the data in lst[]
    # and calculate the number of visits for each IP address
    # save visits in 'visitFreq'
    for ip in unique_ip:
        temp = []
        visits = 0

        # add all the lines where the current IP address occurs
        # in a temporary list
        for line in lst:
            x = line.split()
            if x[0] == ip:
                temp.append(line)

        # count the number of visits for the current IP
        for i in range(0, len(temp)-1):
            hours = float(temp[i].split()[3].split(':')[1]) * 60
            minutes = float(temp[i].split()[3].split(':')[2])
            seconds = float(temp[i].split()[3].split(':')[3]) * (1/60)
            res = hours + minutes + seconds

            hours2 = float(temp[i+1].split()[3].split(':')[1]) * 60
            minutes2 = float(temp[i+1].split()[3].split(':')[2])
            seconds2 = float(temp[i+1].split()[3].split(':')[3]) * (1/60)
            res2 = hours2 + minutes2 + seconds2

            result = abs(res - res2)

            # if hour difference is greater than 1 hour
            # increment visits
            if result > 60.0:
                visits += 1

        # taking into account the very last request,
        # as a new request is never made, it counts
        # as a visit
        if len(temp) != 0:
            visits += 1

        # save number of visits for current IP
        visitFreq.append(visits)

    # make a dictionary and combine both lists
    dictFreq = dict(zip(unique_ip, visitFreq))

    # sort 'dictFreq' in descending order according to value
    sortedFreq = OrderedDict(
        sorted(dictFreq.items(), key=itemgetter(1), reverse=True))

    # format output
    print('{:15}    {:}'.format('IP', 'Visits'))
    for key, value in sortedFreq.items():
        # print(str(key) + " : " + str(value))
        print('{:15}    {:}'.format(str(key), str(value)))

    f.close()


'''
    ~~~~~~~~~~~~~~~ MAIN ~~~~~~~~~~~~~~~~~~~~
'''
argv = sys.argv[1:]

# variable to hold log file's name
logFile = ""

# use getopt and implement error handling
try:
    opts, args = getopt.getopt(argv, "l:nt:L:v:d:")
except getopt.GetoptError as err:
    print(err)

# save log file name
for opt, arg in opts:
    if opt in ['-l']:
        logFile = arg


# run throught the arguments passed by the user
# and call the appropriate function
for opt, arg in opts:
    if opt in ['-n']:
        uniqueIPAddresses(logFile)
    elif opt in ['-t']:
        number = arg
        topNipAddresses(logFile, number)
    elif opt in ['-L']:
        ip = arg
        listAllRequests(logFile, ip)
    elif opt in ['-v']:
        ip = arg
        numOfVisits(logFile, ip)
    elif opt in ['-d']:
        date = arg
        numOfVisitsOnDate(logFile, date)
