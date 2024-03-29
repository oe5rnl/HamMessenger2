; Script generated by the HM NIS Edit Script Wizard.

; HM NIS Edit Wizard helper defines
!define PRODUCT_NAME "HamMessenger2"
!define PRODUCT_VERSION "W-0.5.7a"
!define PRODUCT_PUBLISHER "OE5RNL&OE5NVL"
!define PRODUCT_WEB_SITE "http://www.oevsv.at"
!define PRODUCT_DIR_REGKEY "Software\Microsoft\Windows\CurrentVersion\App Paths\hm2.exe"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"

; MUI 1.67 compatible ------
!include "MUI.nsh"

; MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "worldwide.ico"
!define MUI_UNICON "worldwide.ico"

; Welcome page
!insertmacro MUI_PAGE_WELCOME
; License page
!insertmacro MUI_PAGE_LICENSE "..\GNU_GENERAL_PUBLIC_LICENSE_V3.txt"
; Directory page
;!insertmacro MUI_PAGE_DIRECTORY
; Instfiles page
!insertmacro MUI_PAGE_INSTFILES
; Finish page
!define MUI_FINISHPAGE_RUN "$INSTDIR\HamMessenger2.exe"
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_INSTFILES

; Language files
!insertmacro MUI_LANGUAGE "English"

; MUI end ------

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "../prod/SetupHamMessenger2-W.0.5.7a.exe"
InstallDir "$PROGRAMFILES\HamMessenger2"
InstallDirRegKey HKLM "${PRODUCT_DIR_REGKEY}" ""
ShowInstDetails show
ShowUnInstDetails show

Section "Hauptgruppe" SEC01
  SetOutPath "$INSTDIR"
  SetOverwrite ifnewer
  File "..\dist\main.ui"
  File "..\dist\newgroup.ui"
  File "..\dist\HamMessenger2.exe"
  CreateDirectory "$SMPROGRAMS\HamMessenger2"
  CreateShortCut "$SMPROGRAMS\HamMessenger2\HamMessenger2.lnk" "$INSTDIR\HamMessenger2.exe"
  CreateShortCut "$DESKTOP\HamMessenger2.lnk" "$INSTDIR\HamMessenger2.exe"
  CreateDirectory "$APPDATA\HamMessenger2"
  SetOutPath "$APPDATA\HamMessenger2"
SectionEnd

Section "Hauptgruppe1" SEC02
  SetOutPath "$APPDATA"
  SetOverwrite ifnewer
  CreateDirectory "$APPDATA\HamMessenger2\res"
  SetOutPath "$APPDATA\HamMessenger2\res"
  File "..\dist\res\buzzer_x.wav"
  File "..\dist\res\hinweis.wav"
  File "..\dist\res\Raute_klein.jpg"
  File "..\dist\res\worldwide.png"
SectionEnd

Section -AdditionalIcons
  SetOutPath $INSTDIR
  WriteIniStr "$INSTDIR\${PRODUCT_NAME}.url" "InternetShortcut" "URL" "${PRODUCT_WEB_SITE}"
  CreateShortCut "$SMPROGRAMS\HamMessenger2\Website.lnk" "$INSTDIR\${PRODUCT_NAME}.url"
  CreateShortCut "$SMPROGRAMS\HamMessenger2\Uninstall.lnk" "$INSTDIR\uninst.exe"
SectionEnd

Section -Post
  WriteUninstaller "$INSTDIR\uninst.exe"
  WriteRegStr HKLM "${PRODUCT_DIR_REGKEY}" "" "$INSTDIR\hm2.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\HamMessenger2.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
SectionEnd


Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK "$(^Name) wurde erfolgreich deinstalliert."
FunctionEnd

Function un.onInit
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "M�chten Sie $(^Name) und alle seinen Komponenten deinstallieren?" IDYES +2
  Abort
FunctionEnd

Section Uninstall
  Delete "$INSTDIR\${PRODUCT_NAME}.url"
  Delete "$INSTDIR\uninst.exe"

  Delete "$INSTDIR\HamMessenger2.exe"
  Delete "$INSTDIR\main.ui"
  Delete "$INSTDIR\newgroup.ui"
  
  Delete "$APPDATA\HamMessenger2\application.ini"
  Delete "$APPDATA\HamMessenger2\groups.ini"
  
  Delete "$APPDATA\HamMessenger2\HamMessenger2_log.json"
  Delete "$APPDATA\HamMessenger2\HamMessenger2_DEBUG_log.json"
   
  Delete "$APPDATA\HamMessenger2\HM2.log"
  Delete "$APPDATA\HamMessenger2\res\buzzer_x.wav"
  Delete "$APPDATA\HamMessenger2\res\hinweis.wav"
  Delete "$APPDATA\HamMessenger2\res\Raute_klein.jpg"
  Delete "$APPDATA\HamMessenger2\res\worldwide.png"
  RMDir "$APPDATA\HamMessenger2\res"
  RMDir "$APPDATA\HamMessenger2"

  Delete "$SMPROGRAMS\HamMessenger2\Uninstall.lnk"
  Delete "$SMPROGRAMS\HamMessenger2\Website.lnk"
  Delete "$DESKTOP\HamMessenger2.lnk"
  Delete "$SMPROGRAMS\HamMessenger2\HamMessenger2.lnk"


  RMDir "$SMPROGRAMS\HamMessenger2"
  RMDir "$INSTDIR"

  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  DeleteRegKey HKLM "${PRODUCT_DIR_REGKEY}"
  SetAutoClose true
SectionEnd