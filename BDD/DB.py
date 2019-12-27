#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 18:34:06 2019

@author: coco
"""

import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE users
             (name text, userid integer, useridtelegram integer, moneybalance real, mealbalance real, communityid integer, 
             isadmin bool)''')



c.execute('''CREATE TABLE meals
             (whocooks integer, communityid integer,what text, when text, howmany integer, howmuch real, deadline text, 
             isdone integer, participants text, canceled integer)''')


# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()