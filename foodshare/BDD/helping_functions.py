#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 22:54:40 2019

@author: coco
"""


def create_user(conn, user):
    """
    Create a new user into the projects table
    :param conn:
    :param user:
    :return: user id
    """
    sql = """ INSERT INTO users (name, userid,
    useridtelegram, moneybalance, mealbalance, communityid, isadmin)
              VALUES(?,?,?,?,?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, user)
    return cur.lastrowid


def create_meal(conn, meal):
    """
    Create a new meal into the projects table
    :param conn:
    :param meal:
    :return: meal id
    """
    sql = """ INSERT INTO meals (whocooks, communityid, /
    what, when, howmany, howmuch, deadline, /
             isdone, participants, canceled)
              VALUES(?,?,?,?,?,?,?,?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, meal)
    return cur.lastrowid


def select_users_by_mealpoints(conn, communityid):
    """
    Select users by order of mealpoints 
    :param conn:
    :param communityid:
    :return: rows of users in the selected community 
    ordered by mealpoints"""
    sql = """SELECT * FROM users WHERE communityid=? ORDER BY mealbalance"""
    cur = conn.cursor()
    cur.execute(sql, (communityid,))
    rows = cur.fetchall()
    return rows
