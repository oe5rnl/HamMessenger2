

<br>

# ANLEITUNG IN ARBEIT !!!

# HAMGO Messenger2 Client


Der HAMGO Messenger Client lauft unter Windows, Linux und MAC.<br><br>
<b>Diese Version ersetzt die alte PyGObject/Gtk3 Version aus dem Jahr 2018!!!</b><br>

Der MultiPlatform-Client wurde von Reinhold OE5RNL und Manfed OE5NVL erstellt. <br>
Er basiert auf dem Windows .NET Client von OE1KBC sowie dem HAMGO Protokoll von Alex OE1VQS und Kurt OE1KBC.<br><br>
Das Programm ist in Python geschrieben. Als GUI Framework wurde PyQt5 verwendet.<br>
<br>

Für Windiows gibt  es natürlich immer noch den .NET Client von OE1KBC.<br>
Er kann über den Link http://news.ampr.at/?page_id=462 aus dem HAMNET geladen werden.<br>

<br>
Getestet wurde das Programm auf folgende Betriebssystemen:<br>
<br>

* Ubuntu   20.04 LTS   
* raspberry Pi ???
* Mac      Test noch offen
* Windows  10 
* Windows  11

Anregungen und Fehler bitte im github als Issue einmelden.



Weitere Infos:

HAMNET: https://wiki.oevsv.at/wiki/Kategorie:Digitaler_Backbone

MESHCOM: https://wiki.oevsv.at/wiki/Kategorie:MeshCom

<br>

# HamMessenger Install 

<br>
<b>Alle Installationsprogramme findest du im github unter Releases.</b><br>
Nach der Installation müssen im Tab Setup zumindest das Rufzeichen, Name, QTH, Broadcast IP und Hamnet IP eingegeben werden.
<br><br>

## WINDOWS

<br>
Download und install SetupHamMeseenger2-U.x.x.x.exe von Releases

Es müssen keine Pakete mit pip werden.

<br>

## Linux (Ubuntu):

Download SetupHamMeseenger2-U.x.x.x.tar.gz von Releases

tar -xvzf HamMessenger2-x.x.x.tar.gz

cd HamMessenger2

starten mit:

./HamMessenger2

Es müssen keine Pakete mit pip oder apt installiert werden.

<br>

## Linux Raspberry Pi
<br>
Für den Raspberry Pi ist ein eigener installer erforderlich.

wo??????

Es müssen keine Pakete mit pip oder apt installiert werden.


<br>
<br>

## Mac
todo<br><br>
<br>

# Installation vom Source Code

<br>
Sollte der Installer für das entsprechnde Betriebssytem nicht funktionieren, <br>
kann die Installation vom Sourcecode probiert werden.
<br><br>

## Windows 

git clone https://github.com/oe5rnl/hm2.git<br>
<br>
pip install python3<br>
pip install pyqt5<br>
pip install dark qdarkstyle<br>
pip install pysondb<br>
pip install simpleaudio<br>
<br><br>
Die folgenden Dateien werden normalerweise vom Installer angelegt.<br>
In Fall der manuellen Installation müssen aus sie aus dem Verzeichnis hm2 <br>
in das Verzeihnis APPDATE\Roaming\HamMessenger2 des Users kopiert werden:<br>
<br>
mkdir C:\Users\reinh\AppData\Roaming\HamMessenger2\res<br>
copy res* C:\Users\reinh\AppData\Roaming\HamMessenger2\\res<br>
copy groups.ini C:\Users\reinh\AppData\Roaming\HamMessenger2<br>
<br>
Weitere benötigte Dateien werden direkt vom Basisverzeichnis der Applikation geladen.<br>
<br>


<br>

## Mac
todo - Wer kann da know how beisteuern.<br><br>
Die installation erfolgt wie unter "Installation from Source" beschrieben.
<br>
<br>

# Erzeugen der Installer Programme

## Windows

prerequisite:

* install python3 <br>
* pip install pyqt5<br>
* pip install dark qdarkstyle<br>
* pip install pysondb<br>
* pip install simpleaudio<br>
<br>
* pip install pyinstaller
* Download und install NSIS-Menu from https://nsis.sourceforge.io/Download
* den NSIS Editor/assistent from http://hmne.sourceforge.net/


Das Erzeugen des Installers erfolgt in drei Schritten:<br>

Kopieren von Dateien in das Verzeichnis dist<br><br>
    cp main.ui dist/<br>
    cp newgroup.ui dist/<br>
    cp groups.ini dist/<br>
<br>
Erzeugen eines Packages mit pyinstaller<br>
    pyinstaller --onefile hm2.py<br>
<br>
Erzeugen des Setupprogrammes mit NSIS Menu<br>
    Start NSIS Menu<br>
    Compile NSI scripts: HamMessenger2.nsi<br>
    HM NIS Edit<br>



## Linux (Ubuntu)

git clone https://github.com/oe5rnl/HamMessenger2.git

install python3 <br>
pip install pyqt5<br>
pip install pytqt5-tools<br>
pip install dark qdarkstyle<br>
pip install pysondb<br>
pip install simpleaudio<br>

Erzeugen eines Packages mit pyinstaller<br>

cd HamMessenger2<br>
pyinstaller --onefile HamMessenger2.py<br>

Bei Änderungen an den Files main.ui und goup.ui
diese von Hammessenger2 nach dist kopieren.    

cp -r dist HamMessenger2
tar -czvf HamMessenger2-U.x.x.x.tar.gz HamMessenger2
    
am Ziel PC:

tar xvf HamMessenger2-U.x.x.x.tar.gz


# raspberry PI

git clone https://github.com/oe5rnl/HamMessenger2.git<br>
<br>
pip install python3 # sollte schon installiert sein<br>
pip install dark qdarkstyle<br>
pip install pysondb<br>
pip install simpleaudio<br>
<br>

sudo apt-get install python3-pyqt5<br>
sudo apt-get install libqt5multimedia5-plugins qml-module-qtmultimedia<br>


sudo apt-get install python3-pyqt5

?? sudo apt-get install libqt5multimedia5-plugins qml-module-qtmultimedia



Erzeugen eines Packages mit pyinstaller<br>
    pyinstaller --onefile hm2.py<br>

files bereinigen und nach dist kopieren

tar cvf HamMessenger2-x.x.x.tar dist

am Ziel PC:

tar cvf HamMessenger2-x.x.x.tar



tar -xvzf may_arch.tar.gz



<br>
# Info
Sollte die Anleitung Fehler enthalten - bitte um Info in de issues am github!.


git rm --cached file1.txt
git commit -m "remove file1.txt"
And to push changes to remote repo

git push origin branch_name


git reset --soft HEAD^  

Raspberry :
pip install QDarkStyle
apt-get install pyqt5-dev
apt-get install pyqt5-dev-tools
apt-get install python3-pyqt5.qtmultimedia
pip install pysondb

pip install simpleaudio


# pip install pyqt5
# pip install dark qdarkstyle
# pip install pysondb
# pip install simpleaudio
#
# pyuic5 -x main.ui -o main-ui.py
#
# Raspberry PI 
#
# sudo apt-get install python3-pyqt5
# sudo apt-get install libqt5multimedia5-plugins qml-module-qtmultimedia