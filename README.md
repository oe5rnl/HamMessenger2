

<br>

# HAMGO Messenger2 Client


Der HAMGO Messenger Client lauft unter Windows, Linux und MAC.<br><br>
<b>Diese Version ersetzt die alte PyGObject/Gtk3 Linux Version aus dem Jahr 2018!!!</b><br>

Der MultiPlatform-Client wurde von Reinhold OE5RNL und Manfed OE5NVL erstellt. <br>
Er basiert auf dem Windows .NET Client von OE1KBC sowie dem HAMGO Protokoll von Alex OE1VQS und Kurt OE1KBC.<br><br>
Das Programm ist in Python geschrieben. Als GUI Framework wurde PyQt5 verwendet.<br>
<br>

Für Windiows gibt  es natürlich immer noch den .NET Client von OE1KBC.<br>
Er kann über den Link http://news.ampr.at/?page_id=462 aus dem HAMNET geladen werden.<br>

<br>
Getestet wurde das Programm auf folgende Betriebssystemen:<br>
<br>

* Ubuntu        20.04 LTS   
* raspberry Pi  Raspian GNU/Linux 11 (bullseye)
* Mac           -Test noch offen
* Windows       10 
* Windows       11

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
Download und install SetupHamMeseenger2-W.x.x.x.exe von Releases

Es müssen keine Pakete mit pip werden.

<br>

## Linux (Ubuntu):

Download SetupHamMeseenger2-L.x.x.x.tar.gz von Releases

tar -xvzf HamMessenger2-L.x.x.x.tar.gz

cd HamMessenger2-L.x.x.x

starten mit:

./HamMessenger2

Es müssen keine Pakete mit pip oder apt installiert werden.

<br>

## Linux Raspberry Pi
<br>
Download SetupHamMeseenger2-Pi.x.x.x.tar.gz von Releases

tar -xvzf HamMessenger2-Pi.x.x.x.tar.gz

cd HamMessenger2-Pi.x.x.x

starten mit:

./HamMessenger2

Es müssen keine Pakete mit pip oder apt installiert werden.


<br>
<br>

## Mac
todo - Wer kann da know how-beisteuern?<br><br>
Die installation erfolgt derzeit wie unter "Installation from Source" beschrieben.
<br>

# Installation vom Source Code

<br>
Sollte der Installer für das entsprechnde Betriebssytem nicht funktionieren, <br>
kann die Installation vom Sourcecode probiert werden.
<br><br>

## Windows 

git clone https://github.com/oe5rnl/hm2.git<br>
<br>
*<br>
pip install python3<br>
pip install pyqt5<br>
pip install qdarkstyle<br>
pip install pysondb<br>
pip install simpleaudio<br>
<br><br>
Die folgenden Dateien werden normalerweise vom Installer angelegt.<br>
In Fall der manuellen Installation müssen aus sie aus dem Verzeichnis HamMessenger2 <br>
in das Verzeihnis APPDATE\Roaming\HamMessenger2 des Users kopiert werden:<br>
<br>
mkdir C:\Users\reinh\AppData\Roaming\HamMessenger2\res<br>
copy res* C:\Users\reinh\AppData\Roaming\HamMessenger2\res<br>
copy groups.ini C:\Users\reinh\AppData\Roaming\HamMessenger2<br>
<br>
Weitere benötigte Dateien werden direkt vom Basisverzeichnis der Applikation geladen.<br>
<br>

## Linux 

git clone https://github.com/oe5rnl/hm2.git<br>
<br>
install python3 <br>
pip install pyqt5<br>
pip install pytqt5-tools<br>
pip install dark qdarkstyle<br>
pip install pysondb<br>
pip install simpleaudio<br>

cd HamManager2
./HamManager2

<br>

## Mac
todo - Wer kann da know how-beisteuern?<br><br>
<br>
git clone https://github.com/oe5rnl/hm2.git<br>
<br>
install python3 <br>
pip install pyqt5<br>
pip install pytqt5-tools<br>
pip install dark qdarkstyle<br>
pip install pysondb<br>
pip install simpleaudio<br>

change workdirecrory zu HamManager2
starte HamManager2

<br>

# Erzeugen der Installer Programme

## Windows

prerequisite:
* git installieren
* install python3 <br>
* pip install pyqt5<br>
* pip install dark qdarkstyle<br>
* pip install pysondb<br>
* pip install simpleaudio<br>
<br>
* pip install pyinstaller
* Download und install NSIS-Menu from https://nsis.sourceforge.io/Download
* den NSIS Editor/assistent from http://hmne.sourceforge.net/

<br>
Das Erzeugen des Installers erfolgt in drei Schritten:<br>

Kopieren von Dateien in das Verzeichnis dist<br><br>
    cd HamMessenger2
    cp main.ui dist/<br>
    cp newgroup.ui dist/<br>
    cp groups.ini dist/<br>
    mkdir prod<br>
<br>
Erzeugen eines Packages mit pyinstaller<br>
    pyinstaller --onefile HamMessenger2.py<br>
<br>
Erzeugen des Setupprogrammes mit NSIS Menu<br>
    Start NSIS Menu<br>
    Edit Version Info<br>
    Compile NSI scripts: HamMessenger2.nsi<br>
    Ergebnis steht im Verzeichnis builder
    Mit HM NIS Edit kann die nsi date bearbeitet werden.<br>



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
mkdir prod<br>
pyinstaller --onefile HamMessenger2.py<br>

Bei Änderungen an den Files main.ui und goup.ui
diese von Hammessenger2 nach dist kopieren.    

rm -r HamMessenger2-L.x.x.x && cp -r dist HamMessenger2-L.x.x.x
tar -czvf prod/HamMessenger2-L.x.x.x.tar.gz HamMessenger2-L.x.x.x
    
am Ziel PC:

tar xvf HamMessenger2-U.x.x.x.tar.gz


# raspberry PI

git clone https://github.com/oe5rnl/HamMessenger2.git<br>
<br>
pip install python3 # sollte schon installiert sein<br>
pip install dark qdarkstyle<br>
pip install pysondb<br>
pip install simpleaudio<br>
pip install pyinstaller<br>
<br>

sudo apt-get install python3-pyqt5<br>
sudo apt-get install pyqt5-dev-tools<br>
#install pyqt5-tools ???
#sudo apt-get install libqt5multimedia5-plugins qml-module-qtmultimedia<br>

Erzeugen eines Packages mit pyinstaller<br>

cd HamMessenger2<br>
mkdir prod<br>
pyinstaller --onefile HamMessenger2.py<br>

Bei Änderungen an den Files main.ui und goup.ui
diese von Hammessenger2 nach dist kopieren.    

rm -r HamMessenger2-Pi.x.x.x && cp -r dist HamMessenger2-Pi.x.x.x
tar -czvf prod/HamMessenger2-Pi.x.x.x.tar.gz HamMessenger2-Pi.x.x.x
    
am Ziel PC:

tar xvf HamMessenger2-U.x.x.x.tar.gz



<br>
# Info
Sollte die Anleitung Fehler enthalten - bitte um Info in de issues am github!.

