import sqlite3

def pid_search(program): # lässt ein Unterprogram nach der PID eines anderen suchen 
    with open("mbox/settings/pids.txt", 'r') as file:
        for line in file:
            if line.strip().startswith(f'P: {program},'):
                id_string = line.strip().split(", ")[1]
                pid_int = int(id_string.split(": ")[1])
                return pid_int
    return None

def pid_new_id(program, new_id): # Speichert die PID eines neuen Fensters
    entry_exists = False
    new_line = f'P: {program}, ID: {new_id}\n'

    with open("mbox/settings/pids.txt", 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if line.strip().startswith(f'P: {program},'):
            lines[i] = new_line
            entry_exists = True
            break

    if not entry_exists:
        lines.append(new_line)

    with open("mbox/settings/pids.txt", 'w') as file:
        file.writelines(lines)

def get_user(): # Abfrage, welcher User momentan angemeldet ist
    try:
        connection = sqlite3.connect("mbox/settings/settings.db")
        cursor = connection.cursor()

        cursor.execute("SELECT username FROM user")
        result = cursor.fetchone()

        if result:
            return result[0]
    finally:
        if connection:
            connection.close()