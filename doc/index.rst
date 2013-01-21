.. Teamhub documentation master file, created by
   sphinx-quickstart on Mon Nov 26 11:42:15 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Teamhub Dokumentation
=====================

Willkommen in der Teamhub-Dokumentation!

Teamhub ist ein einfaches Aufgabenmanagementsystem für
kleine Teams. Es wurde als Django-App entwickelt und
benötigt deshalb eine laufende Django-Installation.

Fragen, Anregungen und anderes Feedback nehmen wir gerne
auf unserem `Github-Repository`_ entgegen.

.. _Github-Repository: https://github.com/neonsamurai/swp2-teamhub

Inhalt
======

.. toctree::
   :maxdepth: 2
   :numbered:


Installation
============

Die empfohlene Betriebsumgebung ist ein Unix-basiertes Betriebssystem.
Für die folgende Anleitung wird ein Ubuntu/Debian angenommen. Es werden
aber auch Links zu den jeweilig benötigten Abhängigkeiten geliefert, so
dass die Installation ggf. auch manuell erfolgen kann. Teamhub ist eine
Anwendung für das Django-Webframework. Demnach müssen vor der Installation
folgende Abhängigkeiten erfüllt sein:

- Python 2.7.x
- Python-pip

Es wird weiterhin emfohlen, für den Testbetrieb und Entwickllung, eine
virtuelle Pythonumgebung zu erstellen, um eine ggf. vorhandene systemweite
Pythoninstallation nicht zu beeinträchtigen. Hierfür wird virtualenv empfohlen.

Schritt-für-Schritt-Anleitung
-----------------------------

# Installieren Sie Python 2.7.x
## Installation per ``sudo apt-get install python2.7``
## Link: www.python.org
# Installieren Sie pip:
## Installation per ``sudo apt-get install python-pip``
## Link: http://www.pip-installer.org/en/latest/installing.html#using-the-installer
# Installieren Sie virtualenv mit pip: ``sudo pip install virtualenv``
# Erstellen Sie ein Verzeichnis, in dem die Anwendung leben soll
## z.B.: ``mkdir teamhub``
# Beziehen Sie den Quellcode
## Repository clonen: ``git clone git@github.com:neonsamurai/swp2-teamhub.git``
## Alternativ kopieren sie das Verzeichnis “teamhub” aus dem gelieferten ZIP-Archiv an eine geeignete Stelle
# Im Verzeichnis des Repositorys eine virtuelle Pythonumgebung erstellen: ``virtualenv venv``
# Die virtuelle Umgebung aktivieren:
## ``venv/Scripts/activate.bat`` (Windows cmd.exe)
## ``venv/Scripts/activate.ps1`` (Windows PowerShell)
## ``. venv/bin/activate`` (Linux)
# Installieren Sie die Abhängigkeiten mit: pip install -r requirements.txt

Inbetriebnahme
--------------
Bevor Sie die Anwendung das erste mal starten können, müssen Sie noch die Datenbank
vorbereiten, sowie anschließend den Entwicklungsserver starten.

Zurücksetzen der Datenbank
..........................

# ``rm db/sqlite.db``
# ``touch db/sqlite.db``
# ``python manage.py syncdb``

Sie werden gefragt, ob Sie einen Superuser erstellen möchten. Bitte tun sie dies und
beantworten die Fragen entsprechend. Notieren Sie sich ggf. die Zugangsdaten für
ihren Superuser.

Starten Sie den Entwicklungsserver mit ``python manage.py runserver``

Die Anwendung ist jetzt auf http://localhost:8000 verfügbar.




Index und Tabellen
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

