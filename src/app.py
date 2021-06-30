import os
import sys
from fanstoken import FansToken

if __name__ == '__main__':
    try:
        while True:
            os.system('cls')
            print('''
 ________     ___    ___ ________    _____  ________  ________  ________  _______      
|\   __  \   |\  \  /  /|\   __  \  / __  \|\   ____\|\   __  \|\   ___ \|\  ___ \     
\ \  \|\  \  \ \  \/  / \ \  \|\  \|\/_|\  \ \  \___|\ \  \|\  \ \  \_|\ \ \   __/|    
 \ \  \\\\\  \  \ \    / / \ \  \\\\\  \|/ \ \  \ \  \    \ \  \\\\\  \ \  \ \\\\ \ \  \_|/__  
  \ \  \\\\\  \  /     \/   \ \  \\\\\  \   \ \  \ \  \____\ \  \\\\\  \ \  \_\\\\ \ \  \_|\ \ 
   \ \_______\/  /\   \    \ \_______\   \ \__\ \_______\ \_______\ \_______\ \_______\\
    \|_______/__/ /\ __\    \|_______|    \|__|\|_______|\|_______|\|_______|\|_______|
             |__|/ \|__|                                                                                                                                                                                                                                                                                                   
              ''')
            print("[1]  Add phone scan QR code")
            print("[2]  Run phone scan QR code")
            print("[3]  Show lists phone")
            print("[4]  Delete phone")
            print("[5]  Exit")
            
            select = input('\nEnter your select: ')
            
            fans = FansToken()
            if select == '1':
                fans.addphone()
            elif select == '2':
                fans.scan()
            elif select == '3':
                fans.listphone()
            elif select == '4':
                fans.deletephone()
            elif select == '5':
                print('\n\nExit Good by !')
                sys.exit(0)
    except KeyboardInterrupt:
        print('\n\nExit Good by !')
        sys.exit(0)
        
        