import os
import mysql.connector
import requests
import cloudscraper
import base64
import random
import time
from dotenv import load_dotenv
from anticaptchaofficial.recaptchav2proxyless import *


class FansToken:

    def __init__(self):
        load_dotenv(os.path.abspath(".env"))
        self.db_host = os.getenv('DB_HOST')
        self.db_user = os.getenv('DB_USER')
        self.db_pass = os.getenv('DB_PASSWORD')
        self.db_name = os.getenv('DB_BATABASE')

        self.proxy_enable = os.getenv('PROXY_ENABLE')
        self.proxy_user = os.getenv('PROXY_USER')
        self.proxy_pass = os.getenv('PROXY_PASS')
        self.proxy_host = os.getenv('PROXY_HOST')
        self.proxy_port = os.getenv('PROXY_PORT')

        self.url_refreshToken = 'https://apis.bitkubnext.com/v1.0/auth/refresh-token'
        self.url_sendOTP = 'https://apis.bitkubnext.com/v1.0/auth/login-with-phone/req'
        self.url_login = 'https://apis.bitkubnext.com/v1.0/auth/login-with-phone'
        self.url_airdrop = 'https://apis.bitkubnext.com/v1.0/wallets/erc20/airdrop'

        self.solver = recaptchaV2Proxyless()
        self.solver.set_verbose(1)
        self.solver.set_key(os.getenv('API_KEY'))
        self.solver.set_website_key(os.getenv('WEBSITE_KEY'))

    def request(self, method, url, data=None, header_append=None):
        user_anget = []
        f = open(os.path.abspath("src/user-anget.txt"), "r")
        for x in f:
            user_anget.append(x.splitlines()[0])

        headers = {
            'content-type': 'application/json',
            'Accept-Charset': 'UTF-8',
            'User-Agent': user_anget[random.randint(0, 804)],
        }
        if header_append != None:
            for item in header_append:
                headers.setdefault(header_append[item, header_append[item]])

        session = requests.session()
        scraper = cloudscraper.create_scraper(
            sess=session,
            delay=10,
            interpreter='js2py',
            captcha={
                'provider': 'anticaptcha',
                'api_key': os.getenv('API_KEY'),
                'no_proxy': True
            })
        if self.proxy_enable.upper() == 'TRUE':
            proxies = {
                "http": f"http://{self.proxy_user}:{self.proxy_pass}@{self.proxy_host}:{self.proxy_port}",
                "https": f"http://{self.proxy_user}:{self.proxy_pass}@{self.proxy_host}:{self.proxy_port}"
            }
            scraper.proxies = proxies
        if method == 'GET':
            r = scraper.get(url, headers=headers)
            return {
                'status': r.status_code,
                'text': r.text,
                'json': r.json() if r.status_code != 403 else None,
            }
        elif method == 'POST':
            r = scraper.post(url, data=data, headers=headers)
            return {
                'status': r.status_code,
                'text': r.text,
                'json': r.json() if r.status_code != 403 else None,
            }
        else:
            return None

    def sqlcommand(self, action, str_sqlcommand, value=None):
        db = mysql.connector.connect(
            host=self.db_host,
            user=self.db_user,
            password=self.db_pass,
            database=self.db_name
        )
        if action == 'SELECT':
            cur = db.cursor()
            query = str(str_sqlcommand)
            cur.execute(query)
            return cur.fetchall()
        elif action == 'INSERT':
            cur = db.cursor()
            cur.execute(str_sqlcommand, value)
            db.commit()
        elif action == 'DELETE':
            cur = db.cursor()
            cur.execute(str_sqlcommand)
            db.commit()

    def addphone(self):
        phone = input('Enter your phone: ')
        phone = "+66" + phone[1:10]

        self.solver.set_website_url(self.url_sendOTP)
        recaptcha_token = self.solver.solve_and_return_solution()
        if recaptcha_token != 0:
            data_sendOTP = '{"phone":"' + phone + '","recaptcha_token":"' + recaptcha_token + '","otp_req":true}'
            r_sendOTP = self.request('POST', self.url_sendOTP, data=data_sendOTP)
            if r_sendOTP['status'] == 403:
                print("\n['ERROR']: Access denied")
                input('\nEnter to continue')
            else:
                if 'ref' in r_sendOTP['json']:
                    os.system('cls')

                    print("Phone: " + phone)
                    print("Ref: " + r_sendOTP['json']['ref'])
                    opt = input('Enter opt: ')

                    data_login = '{"otp":"' + opt + '","phone":"' + phone + '","ref":"' + r_sendOTP['json']['ref'] + '"}'
                    r_login = self.request('POST', self.url_login, data=data_login)
                    if r_login['status'] == 403:
                        print("\n['ERROR']: Access denied")
                        input('\nEnter to continue')
                    else:
                        if 'refresh_token' in r_login['json']:
                            botCounts = self.sqlcommand('SELECT', f"SELECT * FROM `t_fanstokenlists` WHERE phone = '{phone}'")
                            if len(botCounts) > 0:
                                print("\n['ERROR']: Have phone: " + phone)
                                input('\nEnter to continue')
                            else:
                                self.sqlcommand('INSERT', "INSERT INTO `t_fanstokenlists` (id, phone, token) VALUES (NULL, %s, %s)", (phone, r_login['json']['refresh_token']))
                                print("\n['OK']: record inserted. insert success")
                                input('\nEnter to continue')
                        else:
                            print("\n['ERROR']: OTP not found")
                            input('\nEnter to continue')
                else:
                    print("\n['ERROR']: Phone number or recaptcha token not found")
                    input('\nEnter to continue')
        else:
            print("task finished with error " + self.solver.error_code)
            input('\nEnter to continue')

    def scan(self):
        event = input('Enter Event (Url or Event ID) : ')
        event_count = len(event.split('?event='))
        if event_count == 2:
            event = event.split('?event=')[1]

        skip = False
        botCounts = self.sqlcommand('SELECT', 'SELECT token, phone FROM `t_fanstokenlists`')
        for x in botCounts:
            refresh_token = x[0]
            refresh_phone = x[1]

            data_refreshToken = '{"refresh_token": "' + refresh_token + '"}'
            r_refreshToken = self.request('POST', self.url_refreshToken, data=data_refreshToken)
            if r_refreshToken['status'] == 403:
                print("\n['ERROR']: Access denied")
                input('\nEnter to continue')
                skip = True
                break
            else:
                if 'access_token' in r_refreshToken['json']:
                    self.solver.set_website_url(url_refreshToken)
                    recaptcha_token = self.solver.solve_and_return_solution()
                    if recaptcha_token != 0:
                        headers = {
                            'Authorization': 'Bearer ' + str(r_refreshToken['json']['access_token'])
                        }
                        data_airdrop = '{"qr_event_id": "' + event + '", "recaptcha_token": "' + recaptcha_token + '"}'
                        r_airdrop = self.request('POST', self.url_airdrop, data=data_airdrop, header_append=headers)

                        print("\nPhone: " + refresh_phone)
                        print(r_airdrop['json'])
                    else:
                        print("\ntask finished with error " + self.solver.error_code)
                        input('\nEnter to continue')
                        skip = True
                        break
                else:
                    print("\nPhone: " + refresh_phone)
                    print("\n['ERROR']: refresh_token not found")
                    input('\nEnter to continue')
        if skip == False:
            print("\n['OK']: Run Success !")
            input('\nEnter to continue')
            
    def listphone(self):
        botCounts = self.sqlcommand('SELECT', "SELECT id, token, phone FROM `t_fanstokenlists`")
        totalBalance = 0

        skip = False

        for index, x in enumerate(botCounts):
            refresh_id = x[0]
            refresh_token = x[1]
            refresh_phone = x[2]
            
            data_refreshToken = '{"refresh_token": "' + refresh_token + '"}'
            r_refreshToken = self.request('POST', self.url_refreshToken, data=data_refreshToken)
            if r_refreshToken['status'] == 403:
                print("\n['ERROR']: Access denied")
                input('\nEnter to continue')
                skip = True
                break
            else:
                if 'access_token' in r_refreshToken['json']:
                    access_token = r_refreshToken['json']['access_token']
                    token_split = access_token.split(".")

                    base64_message = token_split[1] + '=='
                    base64_bytes = base64_message.encode('ascii')
                    message_bytes = base64.b64decode(base64_bytes)
                    message = message_bytes.decode('ascii')

                    y = json.loads(message)
                    r_wallet = self.request('GET', f'https://bkcscan.com/api?module=account&action=tokenbalance&contractaddress=0x9C04EFD1E9aD51A605eeDcb576159242FF930368&address={y["primary_wallet_address"]}')

                    Balance = r_wallet['json']['result'][0:-18] != '' and r_wallet['json']['result'][0:-18] or 0
                    totalBalance += int(Balance)

                    print(f"[{str(index)}] ID: {str(refresh_id)} Phone >> {refresh_phone} >> Balance : {str(Balance)}")

            time.sleep(random.randint(1, 6))
        if len(botCounts) == 0:
            print("- Lists Empty")

        if skip == False:
            print(f"\nSum all account: {str(totalBalance)} Fans token")
            input('\nEnter to continue')

    def deletephone(self):
        phones = self.sqlcommand('SELECT', 'SELECT id, phone FROM `t_fanstokenlists`')

        phone_id_list = []

        for phone in phones:
            phone_id_list.append(phone[0])
            print(f'[ID: {phone[0]}] -> Phone: {phone[1]}')

        input_id = input('\n Enter ID Phone: ')
        if int(input_id) in phone_id_list:
            self.sqlcommand('DELETE', f'DELETE FROM `t_fanstokenlists` WHERE id={input_id}')

            print("\n['OK']: Delete Success !")
            input('\nEnter to continue')
        else:
            print("\n['Error']: Unknown Phone ID")
            input('\nEnter to continue')
