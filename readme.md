# E-Mail Box
_made by **Jamie**_

****
# Erklärung

Hallo Madeleine,

hier meine Version der E-Mail Box für euch.
Grundlegend kann man alles noch verändern, somit bitte einmal drüber schauen und bescheid sagen ob so alles passt.
Grafisch ist es natürlich nicht die krasseste Anwendung, aber dafür übersichtlich und verständlich.

****

Je nach Stärke der Hardware kann das Programm teilweiße bis zu 3 Sekunden brauchen bis es eine Aktion ausführt,
also nicht direkt erschrecken sondern kurz inne halten.
Bitte testet trotzdem einmal alles was ihr dann auch vorstellen müsst, dass Fehler ausgeschlossen werden können.

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
Datei unter ".../mbox/toolbar/close_window.tmp" löschen

****
# Technische Fragen

Sollten Fragen zur Funktionalität aufkommen, bitte bescheid sagen.
Ich habe versucht jede Zeile Code dahinter mit einem Kommentar zu erklären.
Code sollte oftmals zusätzlich kommentiert sein
