#!/usr/bin/python3
import subprocess
import re


class xuemo_inga:
    def __init__(self, domain):
        self.domain = domain

    def whois(self):
        cmd = subprocess.Popen(
            'whois '+self.domain, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            output, err = cmd.communicate()
            if err:
                print(err.decode('gbk'))
            else:
                output = output.decode('gbk')
                email = re.findall(
                    r'Contact Email:(.*)\n', output)[0].strip()
                phone = re.findall(
                    r'Contact Phone:(.*)\n', output)[0].strip()
                print(phone)
        except:
            pass
        finally:
            cmd.kill()


def main():
    domain = input("please input the domain:")
    inga = xuemo_inga(domain)
    inga.whois()


if __name__ == "__main__":
    main()
