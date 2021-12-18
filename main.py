#!/usr/bin/python3
from os import error
import subprocess
import re
import requests
from bs4 import BeautifulSoup
import sys

invalid_email = ["service.aliyun.com", "35.cn"]


class xuemo_inga:

    def __init__(self, domain):
        self.domain = domain
        self.phone = ''
        self.email = ''
        self.c_domain = []
        self.Registrant = ''
        self.sub_domain = []

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
                    for thing in invalid_email:
                        if thing in self.email:
                            self.email = ""
                            break
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
        if self.Registrant:
            self.reverse_whois_api(self.Registrant)
        print(self.c_domain)

    def is_valid(self):

        print("##################")
        print(self.domain)
        vaild = []
        for thing in dir(self):
            if not callable(getattr(self, thing)) and not thing.startswith("__") and thing != "domain" and thing != "c_domain" and getattr(self, thing) != "" and thing != "sub_domain":
                print(thing + ":"+getattr(self, thing))
                vaild.append(thing)
        return vaild != []

    def subdomain_crack(self):
        self.subdomainfuzz(self.domain)
        if self.c_domain != []:
            for domain in self.c_domain:
                self.subdomainfuzz(domain)

    def subdomainfuzz(self, data):
        file = open("main.txt")
        for thing in file.read().split("\n"):
            all_domain = thing+"."+data
            response = requests.get(
                "http://scan.javasec.cn/run.php?url="+all_domain)
            if response.content != b'':
                print(response.content)
                self.sub_domain.append(response.content)
        file.close()


def main():
    if len(sys.argv) == 1:
        print("Usage of this tool:")
        print("-d domain")
        print("-f file")
        exit(0)
    elif len(sys.argv) == 3:
        domain_list = []
        if sys.argv[1] == "-d":
            domain_list = [sys.argv[2]]
        elif sys.argv[1] == "-f":
            file = open(sys.argv[2])
            domain_list = file.read().split('\n')
            file.close()
    for domain in domain_list:
        inga = xuemo_inga(domain)
        inga.whois()
        if inga.is_valid():
            inga.reverse_whois()
        else:
            print("whois failed")
            exit(0)
        # inga.subdomain_crack()


if __name__ == "__main__":
    main()
