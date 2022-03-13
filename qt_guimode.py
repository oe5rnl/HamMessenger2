
#---------------------------------------------------------------------------------------------------------------
#  filename: qt_guimode.py
#  date: 2022-01-24
#  date: 2018-07-23
#  function:
# 
#  author:      oe5rnl@oevsv.at, oe5nvl@oevsv.at
#  description: HAMNET Messenger client für Linux, Mac und Windows
#               based on OE1KBs Windows .NET Client
#  license:     GNU_GENERAL_PUBLIC_LICENSE_V3

# https://pypi.org/project/pyqt-darktheme/
# https://www.youtube.com/watch?v=SQBQ_y_9gzA



from PyQt5.QtCore import QObject

import qdarkstyle  # noqa: E402

from qdarkstyle.colorsystem import Blue, Gray
from qdarkstyle.palette import Palette


class DarkPalette(Palette):
    """Dark palette variables."""

    # Identifier
    ID = 'dark'

    # Color
    COLOR_BACKGROUND_1 = Gray.B10
    COLOR_BACKGROUND_2 = Gray.B20
    COLOR_BACKGROUND_3 = Gray.B30
    COLOR_BACKGROUND_4 = Gray.B40
    COLOR_BACKGROUND_5 = Gray.B50
    COLOR_BACKGROUND_6 = Gray.B60

    COLOR_TEXT_1 = Gray.B130
    COLOR_TEXT_2 = Gray.B110
    COLOR_TEXT_3 = Gray.B90
    COLOR_TEXT_4 = Gray.B80

    COLOR_ACCENT_1 = Blue.B20
    COLOR_ACCENT_2 = Blue.B40
    COLOR_ACCENT_3 = Blue.B50
    COLOR_ACCENT_4 = Blue.B70
    COLOR_ACCENT_5 = Blue.B80

    OPACITY_TOOLTIP = 230


class LightPalette(Palette):
    """Theme variables."""

    ID = 'light'

    # Color
    COLOR_BACKGROUND_1 = Gray.B140
    COLOR_BACKGROUND_2 = Gray.B130
    COLOR_BACKGROUND_3 = Gray.B120
    COLOR_BACKGROUND_4 = Gray.B110
    COLOR_BACKGROUND_5 = Gray.B100
    COLOR_BACKGROUND_6 = Gray.B90

    COLOR_TEXT_1 = Gray.B10
    COLOR_TEXT_2 = Gray.B20
    COLOR_TEXT_3 = Gray.B50
    COLOR_TEXT_4 = Gray.B70

    COLOR_ACCENT_1 = Blue.B130
    COLOR_ACCENT_2 = Blue.B100
    COLOR_ACCENT_3 = Blue.B90
    COLOR_ACCENT_4 = Blue.B80
    COLOR_ACCENT_5 = Blue.B70

    OPACITY_TOOLTIP = 230


class GuiMode(QObject):

    def __init__(self,app,config):
        super().__init__()
        self.app = app
        self.config = config
        self.mode = self.config.guimode
        if  self.mode == 'dark':
            self.setDark()
        else:
            self.setLight()

    def setGuiMode(self, mode):
        if  mode == 'dark':
            self.mode = 'dark'
            self.setDark()
        else:
            self.mode='light'
            self.setLight()

    #self.app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))

    def setDark(self):
        self.app.setStyleSheet(qdarkstyle.load_stylesheet(palette=DarkPalette))

    def setLight(self):
        self.app.setStyleSheet(qdarkstyle.load_stylesheet(palette=LightPalette))

    def getMode(self):
        return self.mode