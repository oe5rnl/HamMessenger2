import os, platform


def getOs():
    os = platform.platform()
    if os[:7] == 'Windows':
        return "Windows"

    elif os[:5] == 'Linux':
        return "Linux"
    
    elif os[:3] == 'Mac': # ???????????

        return "Mac"
    
    else:
        return 'unknown OS'

def isOsWindows():
    os = platform.platform()
    if os[:7] == 'Windows':
        return True
    else:
        return False


def getUserDataPath():
    print("OS================"+str(getOs()))
    if getOs() == 'Windows':
        print("WWWW")
        p = os.getenv('APPDATA')+'\\HamMessenger2\\'
        print("p========="+str(p))
        return p
    elif getOs() == 'Linux':
        return os.path.abspath(os.getcwd()).replace('\\','/')+'/'   
    else:
        return os.path.abspath(os.getcwd()).replace('\\','/')+'/'   

def getAPPPath():
    if getOs() == 'Windows':     
        p = os.path.abspath(os.getcwd()).replace('\\','/')+'/'   
        return(p)
    elif getOs() == 'Linux':
        return os.path.abspath(os.getcwd()).replace('\\','/')+'/' 
    else:
        return os.path.abspath(os.getcwd()).replace('\\','/')+'/' 

def getUserPath():
    pass


# if __name__ == "__main__":
#     print(getOs())