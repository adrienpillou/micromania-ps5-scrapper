from requests import get
from bs4 import BeautifulSoup
from win10toast import ToastNotifier
from prettytable import PrettyTable
import time
from datetime import datetime
import json

url = "https://www.micromania.fr/consoles-ps5.html"
delay = 10
notify = True

productTileClass = "product-tile"
productNameClass = "product-name"
priceClass = "pricing-container"

def load_settings():
    global url, delay, notify
    f = open('settings.json',)
    data = json.load(f)
    url = data["url"]
    print("url set to: ", url)
    delay = data["delay"]
    print("delay set to: ", delay)
    notify = data["notify"]
    print("notify set to: ", notify)
    f.close()

def scrap():
    res = get(url)
    if (res.status_code != 200):
        print(f"[{res.status_code}] Erreur chargement de la page.")
        return 1

    soup = BeautifulSoup(res.text, "html.parser")
    products = soup.find_all(class_ = productTileClass)
    table = PrettyTable(["Titre", "Prix", "Disponibilité"])

    for p in products:
        title = p.find(class_ = productNameClass).get_text().strip()
        price = p.find(class_ = "sales").get_text().strip()
        buttonClass = p.find("button")["class"]
        if("add-to-cart" in buttonClass):
            available = True
        else:
            available = False
        
        if (available and notify):
            notif = ToastNotifier()
            notif.show_toast("ALERTE MICROMANIA", f"{title} est disponible au prix de {price}.", duration=10)

        row = [title, price, available]
        table.add_row(row)

    date = datetime.now()
    print("\n", date.strftime("%H:%M:%S"))
    print(table)

def main():
    while (True):
        scrap()
        time.sleep(delay)

if __name__ == "__main__":
    load_settings()
    main()

