import os
import sys
import time
import requests
import mysql.connector


def sqlcommand( str_sqlcommand ):

    # connection to database
    db = mysql.connector.connect(host="you_host", user="you_user", password="you_password", database="you_database")
    
    cur = db.cursor()
    query = str(str_sqlcommand)
    cur.execute(query)
    return cur.fetchall()

def insert_Newtoken():

    url_sendOTP = 'https://apis.bitkubnext.com/v1.0/auth/login-with-phone/req'
    url_login   = 'https://apis.bitkubnext.com/v1.0/auth/login-with-phone'

    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

    phone = input('Enter your phone: ')
    phone = "+66"+phone[1:10]

    recaptcha_token = input('Enter recaptcha_token: ')

    data_sendOTP = '{"phone":"'+phone+'","recaptcha_token":"'+recaptcha_token+'","otp_req":true}'
    r_sendOTP    = requests.post(url_sendOTP, data=data_sendOTP, headers=headers)

    

    if 'ref' in r_sendOTP.json():

        os.system('cls')
        
        print("Phone: "+phone)
        print ("Ref: "+r_sendOTP.json()['ref'])
        opt = input('Enter opt: ')

        data_login = '{"otp":"'+opt+'","phone":"'+phone+'","ref":"'+r_sendOTP.json()['ref']+'"}'
        r_login  = requests.post(url_login, data=data_login, headers=headers)

        if 'refresh_token' in r_login.json():

            
            botCounts = sqlcommand("SELECT * FROM T_FanstokenLists WHERE phone = '"+phone+"' ")
            if len(botCounts) > 0 :
                print("\n['ERROR']: Have phone: "+phone)
                input('\nEnter to continue')

            else:

                mydb = mysql.connector.connect(
                host="you_host",
                user="you_user",
                password="you_password",
                database="you_database"
                )

                mycursor = mydb.cursor()

                sql = "INSERT INTO T_FanstokenLists (id, phone, token) VALUES (NULL, %s, %s)"
                val = (phone, r_login.json()['refresh_token'])

                mycursor.execute(sql, val)
                mydb.commit()
                
                print("\n['OK']: record inserted. insert success")
                input('\nEnter to continue')

        else:
            print("\n['ERROR']: OTP not found")
            input('\nEnter to continue')

    else:
        print("\n['ERROR']: Phone number or recaptcha token not found")
        input('\nEnter to continue')


def insert_Runbot():

    event = input('Enter Event: ')

    url_refreshToken = 'https://apis.bitkubnext.com/v1.0/auth/refresh-token'
    url_airdrop      = 'https://apis.bitkubnext.com/v1.0/wallets/erc20/airdrop'
    
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

    botCounts = sqlcommand("SELECT token, phone FROM T_FanstokenLists")
    
    for x in botCounts:
        refresh_token = x[0]
        refresh_phone = x[1]
        
        data_refreshToken = '{"refresh_token": "'+refresh_token+'"}'
        r_refreshToken    = requests.post(url_refreshToken, data=data_refreshToken, headers=headers)

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
    botCounts = sqlcommand("SELECT token, phone FROM T_FanstokenLists")
    i = 0

    for x in botCounts:
        refresh_token = x[0]
        refresh_phone = x[1]
        i += 1
        print("Phone["+str(i)+"]: "+refresh_phone)

    if i == 0:
        print("- Lists Empty")

    input('\nEnter to continue')


def main():
    n = 0
    while n != 1:
        os.system('cls')

        print("\n[ * Ddeveloped by STP5940 * ]\n")
        print("[1]  Add phone scan QR code")
        print("[2]  Run phone scan QR code")
        print("[3]  Show lists phone")
        print("[#]  Update token phone       (Coming soon)")
        print("[#]  Delete phone             (Coming soon)")

        
        typerun = input('\nEnter your type run: ')

        if typerun == "1":
            insert_Newtoken()

        if typerun == "2":
            insert_Runbot()

        if typerun == "3":
            Show_Bot()


if __name__ == "__main__":

    try:
        main()
    except KeyboardInterrupt:
        print('\n\nExit Good by !')
        sys.exit(0)











