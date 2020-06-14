from flask import Flask, g
import sqlite3

def connect_db():
    sql = sqlite3.connect(r'db_memberApi')
    sql.row_factory = sqlite3.Row
    #conn = sql.cursor()
    return sql

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db