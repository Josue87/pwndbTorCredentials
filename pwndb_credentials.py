import requests
from bs4 import BeautifulSoup
import argparse
import re


class FindPasswords():
    def __init__(self, mail, proxy):
        self.url = "http://pwndb2am4tzkvold.onion/"
        name, service = self.__parse_mail(mail)
        self.session = None
        if name and service:
            self.data = {
                    "domain":	service,
                    "domainopr":	"0",
                    "luser":	name,
                    "luseropr":	"0",
                    "submitform":	"em"
                }
            self.session = requests.session()
            self.session.proxie = {}
            #TOR PROXY
            self.session.proxies['http'] = proxy
            self.session.proxies['https'] = proxy
        
    def __parse_mail(self, mail):
        name = None
        service = None
        try:
            split_mail = mail.split("@")
            name = split_mail[0]
            service = split_mail[1]
        except:
            pass
        return name, service

    def request_data(self):
        result = []
        if self.session is not None:
            response = self.session.post(self.url, data=self.data, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, features="html.parser")
                try:
                    passwords = soup.find("pre").get_text()
                    for line in re.findall("\[password\] => .*", passwords):
                        newpass = line.split("=> ")[1]
                        if newpass != "12cC7BdkBbru6JGsWvTx4PPM5LjLX8g49X":
                            result.append(newpass)
                except Exception as e:
                    print(e)

        return result
    
if __name__ == "__main__":
    print("Author: @JosueEncinar")
    print("---------------------")
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mail", help="Email to search passwords", required=True)
    parser.add_argument("-p", "--proxy", help="TOR proxy", default="socks5h://localhost:9050")
    args = parser.parse_args()
    mail = args.mail
    proxy = args.proxy
    match = re.match(
        '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', mail)
    if match:
        print(f"Looking passwords for {mail}")
        passwords = FindPasswords(mail, proxy)
        try:
            data = passwords.request_data()
            print("--------- Passwords list --------")
            print(data)
        except TimeoutError as e:
            print("[-] Error when connecting with pwndb2am4tzkvold.onion")
        except Exception as e:
            print("[-] Something was wrong")
            print(e)

    else:
        print("Please enter a valid mail")