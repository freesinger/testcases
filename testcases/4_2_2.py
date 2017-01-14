#!/usr/bin/python

"""
This dictionary is used to search the phone number and address.
"""

#A simple database
people = {
    
    'Dagou': {
        'phone': '1234',
        'addr': 'Foo drive'
    },

    'Ergou': {
        'phone': '4321',
        'addr': 'Sunset avenue'
    },

    'Tuotuo': {
        'phone': '6788',
        'addr': 'White palace'
    }
}

#Labels to tag the person
labels = {
    'phone': 'phone number',
    'addr': 'address'
}

#Get name
name = raw_input('Name: ')    

if name not in people:
    print 'No such person!'
    exit(0)

#Phone number or address?
while True:
    request = raw_input('Phone number (p) or address (a)?')
    
    if request == 'p':
        key = 'phone'
        break
    if request == 'a':
        key = 'addr'
        break                                 #More to convert...

#Print search result
if name in people:
    print "%s's %s is %s."%\
    (name, labels[key], people[name][key])
