import sqlite3
from flask import Flask, render_template
from flask_paginate import Pagination, get_page_args

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

def get_users(page, total=100, per_page=20):
    offset = total - ((page - 1) * per_page) + 1
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    query = '''SELECT *
                FROM tasks
                WHERE taskID < ?
                ORDER BY taskID DESC
                LIMIT ?;'''
    cur.execute(query, (offset, per_page))
    users = cur.fetchall()
    cur.close()
    con.close()
    return users

@app.route('/')
def index():
    total = 100
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    page, per_page, offset = get_page_args(page_parameter='page', # I don't use this offset value at all
                                           per_page_parameter='per_page')
    per_page = 20
    tasks = cur.execute('SELECT * FROM tasks').fetchone()[0]
    cur.close()
    con.close()
    tasks = get_users(page=page, total=total, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total)
    return render_template('index.html',
                            tasks=tasks,
                            page=page,
                            per_page=per_page,
                            pagination=pagination)
