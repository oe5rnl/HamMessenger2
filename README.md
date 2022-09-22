

<br>

# HAMGO Messenger2 Client


Der HAMGO Messenger Client lauft unter Windows, Linux und MAC.<br><br>
<b>Diese Version ersetzt die alte PyGObject/Gtk3 Linux Version aus dem Jahr 2018!!!</b><br>

Der MultiPlatform-Client wurde von Reinhold OE5RNL und Manfed OE5NVL erstellt. <br>
Das Programm ist in Python geschrieben. Als GUI Framework wurde PyQt5 verwendet.<br><br>
Er basiert auf dem Windows .NET Client von OE1KBC sowie dem HAMGO Protokoll von Alex OE1VQS und Kurt OE1KBC.<br>
<br>

Für Windows gibt es natürlich immer noch den .NET Client von OE1KBC.<br>
Er kann über den Link http://news.ampr.at/?page_id=462 aus dem HAMNET geladen werden.<br>

<br>
Getestet wurde das neue Programm auf folgenden Betriebssystemen:<br>
<br>

* Ubuntu        20.04 LTS   
* Ubuntu        22.04 LTS   
* Mint           5.15.0-47-generic
* raspberry Pi  Raspian GNU/Linux 11 (bullseye) 32 Bit, 64 Bit nicht getestet
* Mac           Test noch offen
* Windows       10 
* Windows       11

Anregungen und gefundene Fehler bitte im github als Issue melden.

Weitere Infos:

HAMNET: https://wiki.oevsv.at/wiki/Kategorie:Digitaler_Backbone

MESHCOM: https://wiki.oevsv.at/wiki/Kategorie:MeshCom

<br>

# HamMessenger installieren 

<br>
<b>Alle gebrauchsfertigen Installationsprogramme findest du im github unter Releases<br>
Rechts neben dem Sourcecode.</b><br>
Nach der Installation müssen beim ersten Start im Tab Setup zumindest das Rufzeichen, Name, QTH, Broadcast IP und Hamnet IP eingegeben werden.
<br><br>

## WINDOWS

<br>
Download und install SetupHamMeseenger2-W.x.x.x.exe von Releases

Es müssen keine Pakete mit pip werden.

<br>

## Linux (Ubuntu, Mint, Raspberry):

Download HamMeseenger2-L.x.x.x.tar.gz von Releases

tar -xvzf HamMessenger2-L.x.x.x.tar.gz

cd HamMessenger2-L.x.x.x

starten mit:

./HamMessenger2

Es müssen keine Pakete mit pip oder apt installiert werden.

<br>


## Mac
todo - Wer kann da know how-beisteuern?<br><br>
Die installation erfolgt derzeit wie unter "Installation from Source" beschrieben.
<br>


# Installation vom Source Code

<br>
Sollte der Installer für das entsprechende Betriebssytem nicht funktionieren, <br>
kann die Installation vom Sourcecode probiert werden.
<br><br>

## Windows 
apt-get install git
git clone https://github.com/oe5rnl/HamMessenger2.git<br>
<br>
pip install python<br>
pip install pyqt5<br>
pip install qdarkstyle<br>
pip install pysondb<br>
pip install simpleaudio<br>
<br><br>
Die folgenden Dateien werden normalerweise vom Installer angelegt.<br>
In Fall der manuellen Installation müssen aus sie aus dem Verzeichnis HamMessenger2 <br>
in das Verzeihnis APPDATE\Roaming\HamMessenger2 des Users kopiert werden:<br>
<br>
mkdir C:\Users\reinh\AppData\Roaming\HamMessenger2<br>
mkdir C:\Users\reinh\AppData\Roaming\HamMessenger2\res<br>
copy res* C:\Users\reinh\AppData\Roaming\HamMessenger2\res<br>
copy groups.ini C:\Users\reinh\AppData\Roaming\HamMessenger2<br>
<br>
Weitere benötigte Dateien werden direkt vom Basisverzeichnis der Applikation geladen.<br>
<br>

## Linux (Ubuntu, Mint, Raspberry pi)

git clone https://github.com/oe5rnl/HamMessenger2.git<br>
<br>
sudo apt-get -y install build-essential<br>
sudo apt-get -y install python3 python3-pip git<br>
sudo apt-get -y install python3-dev libasound2-dev<br>
<br>
sudo apt-get -y install python3-pyqt5<br>
sudo apt-get -y install qtcreator pyqt5-dev-tools<br>
<br>
pip3 install pyqt5<br>
pip3 install qdarkstyle<br>
pip3 install pysondb<br>
pip3 install simpleaudio<br>


cd HamManager2<br>
python3 ./HamManager2.py

<br>

## Mac

Sollte identisch zu Linux sein.

todo - Wer kann da know-how beisteuern?<br>
<br>

<br>


# Erzeugen der Installer Programme

## Windows

Installation wie oben unter Windows beschrieben.<br>
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
    pip install pyinstaller<br><br>
    pyinstaller --onefile HamMessenger2.py<br>
<br>
Erzeugen des Setupprogrammes mit NSIS Menu<br>
    Start NSIS Menu<br>
    Edit Version Info<br>
    Compile NSI scripts: HamMessenger2.nsi<br>
    Ergebnis steht im Verzeichnis builder
    Mit dem Programm "HM NIS Edit" kann die nsi date bearbeitet werden.<br>



## Linux (Ubuntu, Mint, Ubuntu)

Installation wie oben unter Linux beschrieben, dann<br>

pip3 install pyinstaller<br>
ev. pyinstaller in den PATH einfügen.<bR>

./make_runtime x.x.x erzeugt ein tar.gz File in der Form HamMessenger2-L.x.x.x.tar.gz<br>

<br>
zb.: ./make_runtime 0.1.57c<br>

Das Ergebnis tar.gz liegt im prod Verzeischnis.<br>

<br>
Am Ziel PC:<br>

tar xvf HamMessenger2-U.x.x.x.tar.gz

cd HamMessenger2<br>
./HamMessenger2


<br>

## Info


Sollte die Anleitung Fehler enthalten - bitte um Info in de issues am github!.

