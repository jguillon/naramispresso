#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import re
import json
import numpy as np
import smtplib
import argparse

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

parser = argparse.ArgumentParser(
    description='summarize ARAMIS LAB\'s Nespresso orders and send bills accordingly',
    prog='naramispresso',
    epilog='see https://github.com/jguillon/naramispresso for updates, bugs reports and answers')

parser.add_argument('typeform_csv', help='csv file exported from Typeform')
parser.add_argument('--send', help='send bills', action='store_true')
parser.add_argument('--date', help='reception date') # '03/08/2018 entre 9h00 et 18h00'
args, unknown_args = parser.parse_known_args()

with open('parameters.json') as f:
    params = json.load(f)

if args.send:
    if not args.date:
        print('Please specify a reception date using the \'--date\' argument.')
        exit(1)

    with open('bill.mail.html', 'r') as html_file:
        mail_html = html_file.read()
        mail_html = mail_html.replace('{reception_date}', args.date)
        mail_html = mail_html.replace('{paypal_id}', params['paypal_id'])
        mail_html = mail_html.replace('{slack_url}', params['slack_url'])
        mail_html = mail_html.replace('{contact_mail}', params['contact_mail'])
        mail_html = mail_html.replace('{office_address}', params['office_address'])
        html_file.close()

with open(args.typeform_csv, 'rU') as csv_file:
    nespresso_report_reader = csv.reader(csv_file, delimiter=',', quotechar='"')

    # Extract prices on first row
    first_row = nespresso_report_reader.__next__()
    brands = first_row[1:-8]
    prices = [0 for i in range(len(brands))]
    overall_quantities = [0 for i in range(len(brands))]
    overall_total = 0
    for i, brand in enumerate(brands):
        m = re.search('[0-9]+,[0-9]+', brand)
        prices[i] = float(m.group(0).replace(',','.'))

    # Itarate over customers lines
    for row in nespresso_report_reader:

        ## Information extraction
        first_name = row[-8]
        last_name = row[-7]
        mail = row[-6]
        quantities = [int(i) if i else 0 for i in row[1:-8]]
        overall_quantities = [sum(x) for x in zip(overall_quantities, quantities)]
        total = sum([quantities[i] * prices[i] for i in range(len(brands))])
        overall_total = overall_total + total
        print('\n' + first_name + ' ' + last_name + ' <' + mail + '> :')
        
        ## HTML table creation
        command_details = ''
        for i, quantity in enumerate(quantities):
            if quantity > 0:
                print(str(quantity) + ' x ' + brands[i])
                command_details = command_details \
                    + '\t\t\t\t<tr bgcolor="#f4ede8" style="color: #313131;">' \
                    + '<td>' + brands[i] + '</td>' \
                    + '<td>' + str(quantity) + ' x ' + str(prices[i]) + '€' + '</td>' \
                    + '<td>' + str(quantity * prices[i]) + '€' + '</td>' \
                    + '</tr>\n'
        print("=> " + str(sum(quantities)) + ' BOXES (' + str(total) + "€)")
        
        if args.send:

            ## Mail content writing
            perso_mail_html = mail_html.replace('{first_name}',
                                                first_name)
            perso_mail_html = perso_mail_html.replace('{last_name}',
                                                      last_name)
            perso_mail_html = perso_mail_html.replace('{first_name}',
                                                      first_name)
            perso_mail_html = perso_mail_html.replace('{command_details}',
                                                      command_details)
            perso_mail_html = perso_mail_html.replace('{total}',
                                                      str(total) )
            perso_mail_text = 'Oops! Use a modern mail app!'

            ## Mail object building
            msg = MIMEMultipart('related')
            msg['Subject'] = 'Naramispresso : Confirmation de Commande'
            msg['From'] = 'Naramispresso'
            msg['To'] = mail

            msg_alt = MIMEMultipart('alternative')
            msg.attach(msg_alt)

            part1 = MIMEText(perso_mail_text, 'plain', 'utf-8')
            msg_alt.attach(part1)

            part2 = MIMEText(perso_mail_html, 'html', 'utf-8')
            msg_alt.attach(part2)

            ## Deal with images
            fp = open('img/naramispresso-logotext-bw.png', 'rb')
            image1 = MIMEImage(fp.read())
            fp.close()
            image1.add_header('Content-ID', '<naramispresso-logotext-bw>')
            msg.attach(image1)

            fp = open('img/naramispresso-mail-header.jpeg', 'rb')
            image2 = MIMEImage(fp.read())
            fp.close()
            image2.add_header('Content-ID', '<naramispresso-mail-header>')
            msg.attach(image2)
            try:
                print('Sending bill...')
                ## Mail sending
                smtp_server = smtplib.SMTP_SSL(params['mail_server']['address'],
                                               params['mail_server']['port'])
                smtp_server.ehlo()
                # smtp_server.starttls()
                smtp_server.login(params['mail_server']['login'],
                                  params['mail_server']['password'])
                # smtp_server.sendmail(msg['From'], msg['To'], msg.as_string())
                smtp_server.sendmail(msg['From'], params['contact_mail'],
                                     msg.as_string())
                smtp_server.close()
                print('            ...OK')
            except Exception as e:
                print(e)
                print('Somehting went wrong when trying to send the mails.')

    csv_file.close()

    ## Print recap'
    print("\n============= TOTAL =============\n")
    for i, quantity in enumerate(overall_quantities):
        if quantity > 0:
            print(str(quantity) + ' x ' + brands[i])
    print("=> " + str(sum(overall_quantities)) + ' BOXES (' +
          str(overall_total) + "€)")
