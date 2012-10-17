# Team Hub

Es soll ein kleines Projektmanagementsystem erstellt werden. Im Kern soll es die Anwender befähigen, Aufgaben innerhalb eines Projektes zu planen, zu verfolgen und deren Ausgang zu bewerten.

Die Realisierung soll als Webanwendung erfolgen und dabei moderne Frontendtechnologien verwenden, die eine produktive Arbeitsumgebung schaffen.

Der Projekt/Teamleiter ( auch andere Benutzer?) sollte in der Lage sein Aufgaben anderen Teammitgliedern zuzuweisen. Die Anwender sollten außerdem ihren Fortschritt bei der Lösung einer Aufgabe bewerten können. Es sollten auch Informationen zum Fortschritt des gesamten Projekts angezeigt werden.

Das System sollte mehrere Ansichten bieten z.B. Übersicht aller Aufgaben, Übersicht aller Aufgaben nach Datum (in einem Kalender) sortiert, Übersicht aller Aufgaben nach Fortschritt usw. enthalten.

Das ist ein Test
# Erste Schritte

* Python muss vorhanden sein.
* pip installieren: http://www.pip-installer.org/en/latest/installing.html#using-the-installer
* virtualenv installieren: 'pip install virtualenv'
* Repository clonen: 'git clone git@github.com:neonsamurai/swp2-teamhub.git'
* Im Verzeichnis des Repository: 'virtualenv venv'
* 'venv/Scripts/activate.bat' (Windows cmd.exe) oder 'venv/Scripts/activate.ps1' (Windows PowerShell) oder '. venv/bin/activate' (Linux)
* 'pip install -r requirements.txt'

# Info, Tutorials usw.

* Git
** Git Book, ausführliche Doku: http://git-scm.com/book/de
** Git Tutorial: http://gitimmersion.com/
* Django
** Django-Projektseite: http://www.djangoproject.com
** Ausführliche Doku: https://docs.djangoproject.com/en/1.4/
** Tutorial: https://docs.djangoproject.com/en/1.4/intro/tutorial01/
* Twitter/Bootstrap
** Github: http://twitter.github.com/bootstrap/
** Doku: http://twitter.github.com/bootstrap/base-css.html

# Git Quick-Guide

## Repository von github holen
1. $> git clone git@github.com:neonsamurai/swp2-teamhub.git

## Repository updaten
1. $> git pull

## Neue Branch mit Namen <NEUE_BRANCH> erstellen
1. $> git push origin <<NEUE_BRANCH>>:refs/heads/<<NEUE_BRANCH>>
2. $> git fetch origin
3. $> git branch --track <NEUE_BRANCH> origin/<NEUE_BRANCH>
4. $> git checkout <NEUE_BRANCH>

## Branch wechseln
1. $> git checkout <BRANCH_NAME>

## Changes committen
Die lange Version (Hier kann man erstmal Dateien zum Commit hinzufügen, und die dann commiten. Gut wenn man seine Änderungen auf mehrere Commits aufteilen möchte):
1. $> git add <dateiname>
2. $> git commit -m "Commit Message"

Die kurze Version (Wenn man alle Änderungen in das Commit einfügen möchte):
1. $> git commit -am "Commit Message"

## Änderungen zu Github pushen
1. $> git push <BRANCH_NAME>

## Eine Branch in die eigene Branch "mergen"
ACHTUNG: Niemals direkt in die master-Branch mergen. Zum Mergen nach master bitte folgenden Absatz beachten!

Man muss sich in der Branch befinden, in die man etwas anderes hineinmergen will:

1. $> git pull
2. $> git merge <BRANCH_NAME>

## Eine Branch nach master mergen
ACHTUNG: Niemals direkt in master mergen!

1. $> git checkout <DIE_BRANCH_DIE_ICH_NACH_MASTER_MERGEN_WILL>
2. $> git pull
3. $> git merge origin/master
4. (ggf. Merge-Konflikte lösen)
5. $> git checkout master
6. $> git merge <DIE_BRANCH_DIE_ICH_NACH_MASTER_MERGEN_WILL>
7. $> git push
test2 R. Mousarov
