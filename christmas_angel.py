import argparse
import json
import os
import random

import yagmail

language_defaults = {
    "en": {
        "subject": "Christmas Greetings!",
        "contents":
        "You should find you loved one on the card! Buy a nice gift! :)",
        "encoding": "utf-8"
    },
    "hu": {
        "subject": "Karácsonyi angyal - 2022",
        "contents":
        "Szia!\n\nA csatolt PDF-ből kiderül, hogy ki az a szerencsés rokon, akinek te lehetsz a karácsonyi angyala. Ne mondd el senkinek és kérlek ne válaszolj erre az emailre, hacsak nem magadat húztad, ami elméletben lehetetlen!\n\nÁldott Ünnepet!",
        "encoding": "iso-8859-2"
    },
    "test": {
        "subject": "TESZT angyal - 2022",
        "contents":
        "Szia!\n\n Ez csak a karácsonyi szokásos teszt üzenet. Itt egy vicc kárpótlásul:\n\n Ferike és Katika karácsonyra ajándékba megkapja a képes Bibliát. Nézegetik, nézegetik, a Madonna a Kisjézussal című képnél megkérdezi Ferike a testvérét: \n- Hol van Jézus apukája? \nKatika elgondolkozva nézi a képet: \n- Biztosan ő fényképezett.\n\n",
        "encoding": "iso-8859-2"
    }
}


def run(args):
    # https://stackoverflow.com/questions/25200220/generate-a-random-derangement-of-a-list
    def random_derangement(n):
        while True:
            v = [i for i in range(n)]
            for j in range(n - 1, -1, -1):
                p = random.randint(0, j)
                if v[p] == j:
                    break
                else:
                    v[j], v[p] = v[p], v[j]
            else:
                if v[0] != 0:
                    return tuple(v)

    config = json.load(open(args.config_name, 'r'))
    recipients = config['recipients']
    n_participants = len(recipients)

    derangement = random_derangement(n_participants)
    pairs = [(recipients[ind]["name"], recipients[rec]["name"]) for ind, rec in enumerate(derangement)]
    
    if args.undesirable_match is not None:
        pair, rev_pair = tuple(args.undesirable_match.split(',')), tuple(reversed(args.undesirable_match.split(',')))
        while pair in pairs or rev_pair in pairs:
            derangement = random_derangement(n_participants)
            pairs = [(recipients[ind]["name"], recipients[rec]["name"]) for ind, rec in enumerate(derangement)]

    yag = yagmail.SMTP(config["authmail"], oauth2_file="~/oauth2.json")
    yag.set_logging(yagmail.logging.INFO)

    html = open(f"card_template_{args.language}.html", "r").read()

    for ind, rec in enumerate(derangement):
        angel_mail = recipients[ind]["mail"]
        angel_name = recipients[ind]["name"]

        recipient_name = recipients[rec]["name"]

        if args.language == "test":
            message = html.format(angel_name, "#teszt#")
        else:    
            message = html.format(angel_name, recipient_name)

        open('template.html',
             'w',
             encoding=language_defaults[args.language]["encoding"]).write(
                 message)
        os.system(
            f'wkhtmltopdf --encoding {language_defaults[args.language]["encoding"]} template.html out.pdf'
        )

        yag.send(to=angel_mail,
                 subject=language_defaults[args.language]["subject"],
                 contents=language_defaults[args.language]["contents"].replace("Szia", f"Szia {angel_name}"),
                 attachments=['./out.pdf'])

        os.system('rm template.html')
        os.system('rm out.pdf')


parser = argparse.ArgumentParser()
parser.add_argument('--language', default="test", type=str, choices=["en", "hu", "test"])
parser.add_argument('--config_name', type=str, required=False, default="./config.json")
parser.add_argument('--undesirable_match', type=str, required=False, default=None)

args = parser.parse_args()

run(args=args)
