import os
import sys
import time
import requests

import base64
import jwt
import json

import getpass

versionSoftware = "0.1 [beta]"


url_refreshToken = 'https://apis.bitkubnext.com/v1.0/auth/refresh-token'
url_sendOTP      = 'https://apis.bitkubnext.com/v1.0/auth/login-with-phone/req'
url_login        = 'https://apis.bitkubnext.com/v1.0/auth/login-with-phone'
url_airdrop      = 'https://apis.bitkubnext.com/v1.0/wallets/erc20/airdrop'


webapi                              = 'URL_API' # ตรงนี้ค้องใส่ URL API BOT สนใจใช้โปรดติดต่อนักพัฒนา
Token_auth                          = ""
url_fanstokenlists_show             = webapi+'/api/fanstokenlists_show'
url_fanstokenlists_getphone         = webapi+'/api/fanstokenlists_getphone'
url_fanstokenlists_add              = webapi+'/api/fanstokenlists_add'
url_pythonregister                  = webapi+'/api/pythonregister'
url_pythonlogin                     = webapi+'/api/pythonlogin'
url_fanstokenlists_getphonecount    = webapi+'/api/fanstokenlists_getphonecount'

headers_default  = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}



def methodGet(_url, _headers):
    return 0


def methodPost(_url, _data, _headers):
    data = requests.post(_url, data=_data, headers=_headers)
    return data


def insert_Newtoken():

    phone = input('Enter your phone: ')
    phone = "+66"+phone[1:10]

    r_botCounts = methodPost(url_fanstokenlists_getphonecount, '{"phone": "'+phone+'"}', {'content-type': 'application/json', 'Accept-Charset': 'UTF-8', 'Authorization': str(Token_auth)})

    if 'FanstokenListsCount' in r_botCounts.json()['JWTAuth']:

        if r_botCounts.json()['JWTAuth']['FanstokenListsCount'] > 0 :
            print("\n['ERROR']: Have phone: "+phone)
            input('\nEnter to continue')

        else:

            
            recaptcha_token = input('Enter recaptcha_token: ')

            r_sendOTP = methodPost(url_sendOTP, '{"phone":"'+phone+'","recaptcha_token":"'+recaptcha_token+'","otp_req":true}', headers_default)

            if 'ref' in r_sendOTP.json():

                os.system('cls')
                
                print("Phone: "+phone)
                print ("Ref: "+r_sendOTP.json()['ref'])
                opt = input('Enter opt: ')


                r_login = methodPost(url_login, '{"otp":"'+opt+'","phone":"'+phone+'","ref":"'+r_sendOTP.json()['ref']+'"}', headers_default)

                if 'refresh_token' in r_login.json():

                    r_fanstokenlists_add = methodPost(url_fanstokenlists_add, '{"phone":"'+phone+'","token":"'+r_login.json()['refresh_token']+'"}', {'content-type': 'application/json', 'Accept-Charset': 'UTF-8', 'Authorization': str(Token_auth)})
                            
                    print("\n['OK']: record inserted. insert success")
                    input('\nEnter to continue')

                else:
                    print("\n['ERROR']: OTP not found")
                    input('\nEnter to continue')

            else:
                print("\n['ERROR']: "+str(r_sendOTP.json()))
                input('\nEnter to continue')


def Runbot():

    event = input('Enter Event: ')

    r_botAll = methodPost(url_fanstokenlists_show, '', {'content-type': 'application/json', 'Accept-Charset': 'UTF-8', 'Authorization': str(Token_auth)})

    # exit()
    for x in r_botAll.json()['JWTAuth']['FanstokenLists']:
        refresh_token = x['token']
        refresh_phone = x['phone']
        
        data_refreshToken = '{"refresh_token": "'+refresh_token+'"}'
        r_refreshToken    = requests.post(url_refreshToken, data=data_refreshToken, headers=headers_default)

        if 'access_token' in r_refreshToken.json():

            recaptcha_token = input('\nEnter recaptcha_token: ')

            headers      = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8', 'Authorization': 'Bearer '+str(r_refreshToken.json()['access_token'])}
            data_airdrop = '{"qr_event_id": "'+event+'", "recaptcha_token": "'+recaptcha_token+'"}'
            r_airdrop    = requests.post(url_airdrop, data=data_airdrop, headers=headers)

            print("\nPhone: "+refresh_phone)
            print(r_airdrop.json())

        else:
            print("\nPhone: "+refresh_phone)
            print("\n['ERROR']: refresh_token not found")
            input('\nEnter to continue')
    
    print("\n['OK']: Run Success !")
    input('\nEnter to continue')


def Show_Bot():
    
    print("")

    r_botAll = methodPost(url_fanstokenlists_show, '', {'content-type': 'application/json', 'Accept-Charset': 'UTF-8', 'Authorization': str(Token_auth)})
    sumBalance = 0
    i = 0

    for x in r_botAll.json()['JWTAuth']['FanstokenLists']:

        refresh_id    = x['id']
        refresh_token = x['token']
        refresh_phone = x['phone']

        data_refreshToken = '{"refresh_token": "'+refresh_token+'"}'
        r_refreshToken    = requests.post(url_refreshToken, data=data_refreshToken, headers=headers_default)

        
        if 'access_token' in r_refreshToken.json():


            txt = r_refreshToken.json()['access_token']

            token_split = txt.split(".")

            base64_message = token_split[1]+'=='
            base64_bytes = base64_message.encode('ascii')
            message_bytes = base64.b64decode(base64_bytes)
            message = message_bytes.decode('ascii')

            # print(message)

            y = json.loads(message)
            # print(y["primary_wallet_address"])
            r_wallet  = requests.get('https://bkcscan.com/api?module=account&action=tokenbalance&contractaddress=0x9C04EFD1E9aD51A605eeDcb576159242FF930368&address='+y['primary_wallet_address']+'', headers=headers_default)

            Balance = r_wallet.json()['result'][0:-18] != '' and r_wallet.json()['result'][0:-18] or 0
            sumBalance += int(Balance)
            i += 1

            print("["+str(i)+"] ID: "+str(refresh_id)+" Phone >> "+refresh_phone+" >> Balance : "+str(Balance))

            

    if i == 0:
        print("- Lists Empty")

    print("\nSum all account: "+str(sumBalance)+" Fans token")
    input('\nEnter to continue')


def main():
    n = 0
    while n != 1:
        os.system('cls')

        print("\n[ * Ddeveloped by STP5940 * ]\n")
        print("[1]  Add phone scan QR code")
        print("[2]  Run phone scan QR code")
        print("[3]  Show lists phone")
        print("[#]  Update token phone         (Coming soon)")
        print("[#]  Delete phone               (Coming soon)")
        print("[#]  Upgrade to Pro Version     (Coming soon)")
        print("[7]  logout")
        print("\n[0]  Software Version [FREE]")

        
        typerun = input('\nEnter your type run: ')

        if typerun == "1":
            insert_Newtoken()

        if typerun == "2":
            Runbot()

        if typerun == "3":
            Show_Bot()

        if typerun == "7":
            Token_auth = ""
            n = 1

        if typerun == "0":
            os.system('cls')
            print("\nDnate: 0x049A4816AE82f26D9cd595424E709AAfa281c374")
            print("\nCurrent version: "+str(versionSoftware))
            input('\nEnter to continue')


if __name__ == "__main__":

    try:
        a = 0
        while a != 1:
            os.system('cls')

            print("\n[ * Ddeveloped by STP5940 * ]\n")
            print("[1]  Login")
            print("[2]  Register")
            print("[3]  Exit")

            
            typerun = input('\nEnter number: ')

            if typerun == "1":

                username          = input('\nEnter username: ')
                password          = getpass.getpass('Enter password: ')

                r_pythonlogin = methodPost(url_pythonlogin, '{"username":"'+username+'","password":"'+password+'"}', headers_default)

                if 'JWTAuth' in r_pythonlogin.json():
                    if r_pythonlogin.json()['JWTAuth']['status'] :
                        print("\n"+r_pythonlogin.json()['JWTAuth']['message'])
                        Token_auth = r_pythonlogin.json()['JWTAuth']['token']
                        time.sleep(1)
                        main()
                    else:
                        print("\n"+r_pythonlogin.json()['JWTAuth']['message'])
                        input('\nEnter to continue')

            if typerun == "2":
                username          = input('\nEnter username: ')
                password          = getpass.getpass('Enter password: ')
                confirm_password  = getpass.getpass('Enter confirm password: ')

                r_pythonregister = methodPost(url_pythonregister, '{"username":"'+username+'","password":"'+password+'","confirm_password":"'+confirm_password+'"}', headers_default)

                print("\n"+r_pythonregister.json()['JWTAuth']['message'])
                input('\nEnter to continue')
            
            if typerun == "3":
                print('\nExit Good by !')
                exit()

        # main()
    except KeyboardInterrupt:
        print('\n\nExit Good by !')
        sys.exit(0)











