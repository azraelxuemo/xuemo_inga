#!/usr/bin/python3
from os import error
import subprocess
import re
import requests
from bs4 import BeautifulSoup


class xuemo_inga:

    def __init__(self, domain):
        self.domain = domain
        self.phone = ''
        self.email = ''
        self.c_domain = []
        self.Registrant = ''

    def whois(self):
        cmd = subprocess.Popen(
            'whois '+self.domain, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            output, err = cmd.communicate()
            if err:
                print(err.decode('utf-8'))
            else:
                output = output.decode('utf-8')
                if re.findall(r'Contact Email:(.*)\n', output):
                    self.email = re.findall(
                        r'Contact Email:(.*)\n', output)[0].strip()
                if re.findall(
                        r'Contact Phone:(.*)\n', output):
                    self.phone = re.findall(
                        r'Contact Phone:(.*)\n', output)[0].strip()
                if re.findall(r'Registrant:(.*)\n', output):
                    self.Registrant = re.findall(
                        r'Registrant:(.*)\n', output)[0].strip()
        except error:
            print(error)
        finally:
            cmd.kill()

    def reverse_whois_api(self, data):
        s = requests.session()
        res = s.get(
            'https://www.reversewhois.io/?searchterm='+data)
        soup = BeautifulSoup(res.text, 'html.parser')
        for table in soup.find_all('table'):
            for td in table.find_all('td'):
                res = re.findall(
                    r'(.*\.[a-zA-Z0-9-]{2,})', td.get_text())
                if res:
                    self.c_domain.append(res[0])

    def reverse_whois(self):
        if self.email:
            self.reverse_whois_api(self.email)
        print(self.c_domain)

    def is_valid(self):
        return self.email != '' or self.Registrant != ''


def main():
    domain = input("please input the domain:")
    inga = xuemo_inga(domain)
    inga.whois()
    if inga.is_valid():
        inga.reverse_whois()
    else:
        print("whois failed")
        exit(0)


if __name__ == "__main__":
    main()
