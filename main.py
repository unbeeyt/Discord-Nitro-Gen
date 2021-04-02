import os
from time import sleep
import requests
import random
import string


os.system("cls")

amount = int(input("How much codes will be generated:"))
print ("Classic Nitro is 16chars and Boost Nitro is 24chars")
nitro = input("Boost codes or Classic codes (boost or classic):")

if "boost" in nitro or "classic" in nitro:
    pass
else:
    print("Answer must be boost or classic")
    exit()


checker = input(f"Enable Checker(yes or no):")

def scrape():
    scraped = 0
    f = open("proxies.txt", "a+")
    f.truncate(0)
    r = requests.get('https://api.proxyscrape.com/?request=displayproxies&proxytype=http&timeout=1500&ssl=yes')
    proxies = []
    for proxy in r.text.split('\n'):
        proxy = proxy.strip()
        if proxy:
            proxies.append(proxy)
    for p in proxies:
        scraped = scraped + 1 
        f.write((p)+"\n")
    f.close()
    print("Scraped proxies.")

if checker == "yes":
    scrapep = input("Auto proxy scrape (yes or no):")
    print("If no, every check will be on random proxy.")
    mult = input("Multiple checks for proxy (yes or no):")
    if scrapep == "yes":
        scrape()
else:
    print(f"If true, before code will be discord.gift/")
    prefix = input("Prefix before codes (yes or no)")
    if "yes" in prefix or "no" in prefix:
        pass
    else:
        print("Answer must be yes or no")
        exit()


print("Generating  codes!")
if checker != "yes":
    sleep(1)

fulla = amount
f = open("codes.txt", "w+", encoding="UTF-8")
try:
    p = open("proxies.txt", encoding="UTF-8")
except FileNotFoundError:
    p = open("proxies.txt", "w+", encoding="UTF-8")
    print("No proxies found in proxies.txt!")
    raise SystemExit



rproxy = p.read().split('\n')
for i in rproxy:
    if i == "" or i == " ":
        index = rproxy.index(i)
        del rproxy[index]
p.close()

if not rproxy:
    print(f"No proxies found in proxies.txt!")
    raise SystemExit

if checker != "yes":
    while amount > 0:
        amount = amount - 1
        if "boost" in nitro:
            code = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(24)])
        else:
            code = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(16)])
        if prefix == "yes":
            print(f"Generated code {code}")
            f.write(f"discord.gift/{code}\n")
        else:
            print(f"Generated code {code}")
            f.write(f"{code}\n")

else:
    while amount > 0:
        f = open(f"working-codes.txt","a", encoding="UTF-8")
        try:
            if not rproxy[0]:
                print("All proxies are invalid!")
                exit()
        except:
            print(f"All proxies are invalid!")
            exit()
        if mult == "yes":
            proxi = rproxy[0]
        else:
            proxi = random.choice(rproxy)
        proxies = {
            "https": proxi
        }
        amount = amount - 1
        if "boost" in nitro:
            code = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(24)])
        else:
            code = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(16)])
        try:
            url = requests.get(f"https://discordapp.com/api/v6/entitlements/gift-codes/{code}", proxies=proxies, timeout=3)
            if url.status_code == 200:
                print(f"Working Code {code}")
                f.write(f"\ndiscord.gift/{code}")
                f.close()
            elif url.status_code == 404:
                fulla = fulla - 1
                print(f"Invalid Code")
            elif url.status_code == 429:
                fulla = fulla - 1
                if mult == "yes":
                    print(f"Proxy {proxi} is ratelimited! | Switching proxy")
                else:
                    print(f"Proxy {proxi} is ratelimited!")
                index = rproxy.index(proxi)
                del rproxy[index]
            else:
                fulla = fulla - 1
                print(f"Invalid Error! | Status code {url.status_code}")
        except:
            index = rproxy.index(proxi)
            del rproxy[index]
            pw = open(f"proxies.txt","w", encoding="UTF-8")
            for i in rproxy:
                pw.write(i + "\n")
            pw.close()
            fulla = fulla - 1
            print(f"Failed connecting to proxy {proxi} Removing from list!")

f.close()
print(f"Successfully generated {fulla} codes!")

input()
