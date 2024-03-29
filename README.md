

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

```

* Ubuntu        20.04 LTS   
* Ubuntu        22.04 LTS   
* Mint           5.15.0-47-generic
* raspberry Pi  Raspian GNU/Linux 11 (bullseye) 32 Bit, 64 Bit nicht getestet
* Mac           tw. getestet
* Windows       10 
* Windows       11
```

Anregungen und gefundene Fehler bitte im github als Issue melden.

Weitere Infos:

HAMNET: https://wiki.oevsv.at/wiki/Kategorie:Digitaler_Backbone

MESHCOM: https://wiki.oevsv.at/wiki/Kategorie:MeshCom

<br>



# HamMessenger installieren 

<b>Alle gebrauchsfertigen Installer und Programme findest du im github unter Releases, rechts neben dem Sourcecode.<br>
Dazu auf den Text "Releases" klicken</b>
<br>

```
Windows: Es existiert eine Setup-Programm.
Linux:   Die Dateinen werden mit tar entpackt. Der Aufruf erfolgt dann mit ./HamMessenger
MAC:     Wie unter "Installation vom Source Code" beschrieben.
```
<br>
Nach der Installation müssen beim ersten Start im Tab Setup zumindest das Rufzeichen, Name, QTH, Broadcast IP und Hamnet IP eingegeben werden.
<br><br>

## WINDOWS

Download und install `SetupHamMeseenger2-W.x.x.x.exe` aus dem Bereich Releases.

Es müssen keine weiteren Dateien installiert werden.

<br>

## Linux (Ubuntu, Mint, Raspberry):

Download `HamMeseenger2-L.x.x.x.tar.gz` von Releases

```bash
tar -xvzf HamMessenger2-L.x.x.x.tar.gz
cd HamMessenger2-L.x.x.x
```

starten mit:

`./HamMessenger2`

Es müssen keine Pakete mit pip oder apt installiert werden.

<br>

## Mac
Die installation erfolgt derzeit wie unter "Installation from Source" beschrieben.<br><br>
todo - Wer kann da know how-beisteuern?<br>
<br>


# Installation vom Source Code

<br>
Sollte der Installer für das entsprechende Betriebssytem nicht funktionieren, <br>
kann die Installation vom Sourcecode probiert werden.
<br><br>

## Windows 
```bash

apt-get install git
git clone https://github.com/oe5rnl/HamMessenger2.git

pip install python
pip install pyqt5
pip install qdarkstyle
pip install pysondb
pip install simpleaudio

```
<br>
Die folgenden Dateien werden normalerweise vom Installer angelegt.<br>
In Fall der manuellen Installation müssen aus sie aus dem Verzeichnis HamMessenger2

in das Verzeihnis `APPDATE\Roaming\HamMessenger2` des Users kopiert werden:
<br>
xxx ist der versendete Windows User.

```bash

mkdir C:\Users\xxx\AppData\Roaming\HamMessenger2
mkdir C:\Users\xxx\AppData\Roaming\HamMessenger2\res
copy res\* C:\Users\xxxx\AppData\Roaming\HamMessenger2\res
copy groups.ini C:\Users\xxxAppData\Roaming\HamMessenger2
```
<br>
Weitere benötigte Dateien werden automatisch vom Basisverzeichnis der Applikation geladen.<br>
<br>

## Linux (Ubuntu, Mint, Raspberry pi)

```bash

git clone https://github.com/oe5rnl/HamMessenger2.git

sudo apt-get update
sudo apt-get -y install build-essential
sudo apt-get -y install python3 python3-pip git
sudo apt-get -y install python3-dev libasound2-dev

sudo apt-get -y install python3-pyqt5
sudo apt-get -y install qtcreator pyqt5-dev-tools

pip3 install pyqt5
pip3 install qdarkstyle
pip3 install pysondb
pip3 install simpleaudio

```
Asuführen mit:
```
cd HamMessenger2
python3 ./HamMessenger2.py
```
<br>

## Mac

Sollte identisch zu Linux sein.

todo - Wer kann da know-how beisteuern?<br>
<br><br>


# Erzeugen der Installer Programme

## Windows

Zuerst Installation des Programms wie oben unter Windows beschrieben.<br>
<br>
Das Erzeugen des Installers erfolgt in drei Schritten:<br>


Kopieren von Dateien in das Verzeichnis dist

```bash

    cd HamMessenger2
    cp main.ui dist/
    cp newgroup.ui dist/
    cp groups.ini dist/
    mkdir prod
```
<br>
Erzeugen eines Packages mit pyinstaller

```bash

    pip install pyinstaller
    pyinstaller --onefile HamMessenger2.py
```
<br>
Erzeugen des Setupprogrammes mit NSIS Menu<br>

```
    Start NSIS Menu
    Edit Version Info
    Compile NSI scripts: HamMessenger2.nsi
    Ergebnis steht im Verzeichnis builder
    Mit dem Programm "HM NIS Edit" kann die nsi date bearbeitet werden.<br>
```


## Linux (Ubuntu, Mint, Ubuntu)

Installation wie oben unter Linux beschrieben, dann<br>

```bash
pip3 install pyinstaller

```
ev. pyinstaller in den PATH einfügen.<bR>

```bash
./make_runtime x.x.x 
```
erzeugt ein tar.gz File in der Form HamMessenger2-L.x.x.x.tar.gz<br>
<br>
zb.: `./make_runtime 0.1.57c`<br>

Das Ergebnis tar.gz liegt im prod Verzeischnis.<br>

<br>
Am Ziel PC:<br>

```bash

tar xvf HamMessenger2-U.x.x.x.tar.gz

cd HamMessenger2
./HamMessenger2
```

<br>

## Info


Sollte die Anleitung Fehler enthalten - bitte ein issue im github anlegen.

