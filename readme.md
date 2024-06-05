# E-Mail Box
von Madeleine Reuther und Tom Vogel

****
# Erklärung

Guten Tag,
dies ist unsere kleine E-Mail Box.
Zum ausführen bitte "main.py" starten und vorher PyQT5 installieren.

****

Je nach Stärke der Hardware kann das Programm teilweiße bis zu 2 Sekunden brauchen bis es eine Aktion ausführt,
also nicht direkt erschrecken, sondern kurz inne halten.
Manche Funktionen sind noch leicht Fehleranfäliig.

****

Zur Erstellung wurde VS Code verwendet und folgende libarys müssen zusätzlich installiert werden:
- pip install PyQt5

****
# Funktionen

Stand jetzt gibt es folgende Funktionen:

- Login Terminal + Regestrierung verschiedener Benutzer
- Anzeige Email Betreff/Sender/Datum/Inhalt + Sortierbar nach Sender/Datum/Betreff
- Senden, Antworten, Weiterleiten von Emails
- Löschen, Aktualisieren von Emails
- Gelöschte Emails anschauen + recovern
- Verändern von Account Information (Password, E-Mail, Name)
- Account Löschen
- Logout/shutdown
- Credits
- Login Log


****
# Bakannte Probleme

- Change Account Info hatte Probleme sich richtig zu schließen
=> kann passieren dass es einen close loop gibt beim starten der Anwendung
FALLS JA
Die Datei unter ".../mbox/toolbar/close_window.tmp" löschen

