def pid_search(program):
    with open("mbox/settings/pids.txt", 'r') as file:
        for line in file:
            if line.strip().startswith(f'P: {program},'):
                id_string = line.strip().split(", ")[1]
                pid_int = int(id_string.split(": ")[1])
                return pid_int
    return None

def pid_new_id(program, new_id):
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

def get_user():
    with open("mbox/settings/settings.txt", 'r') as file:
        for line in file:
            parts = line.strip().split(": ")
            if parts[0] == "Benutzername":
                return parts[1]
    return None