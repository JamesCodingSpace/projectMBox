import sqlite3
from datetime import datetime
import os
import random
import sqlite3
from datetime import datetime

def insert_dummy_emails(table_name):
    emails = []
    with open("mbox/login/premade_emails.txt", 'r') as file:
        for line in file:
            parts = line.strip().split(', ')
            subject = parts[0].split(': ')[1]
            content = parts[1].split(': ')[1]
            content = parts[1].split(': ')[1].replace('{{newline}}', '\n')
            emails.append((subject, content))
    conn = sqlite3.connect('mbox/emails.db')
    c = conn.cursor()
    for email in emails:
        rndm_eid = random.randint(1,1000000000000)
        sent_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute(f"INSERT INTO {table_name} (eid, sender, subject, content, sent_date) VALUES (?, ?, ?, ?, ?)",
                  (rndm_eid, "System", email[0], email[1], sent_date))
    conn.commit()
    conn.close()

