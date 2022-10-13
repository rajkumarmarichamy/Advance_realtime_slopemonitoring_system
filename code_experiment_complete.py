import urllib.request
import requests
import json
import time
import smtplib
import datetime


def check_moisturecontent():
    read_url1 = 'https://api.thingspeak.com/channels/1794023/feeds.json?api_key='
    read_key1 = 'FE77LV8BARRFSNXX'
    read_header1 = '&results=2'
    new_url1 = read_url1 + read_key1 + read_header1
    get_data1 = requests.get(new_url1).json()
    global moisture_percent
    try:
        moisture_percent = get_data1['feeds'][1][str('field1')]
    except IndexError:
        moisture_percent = "0"
    print("output value from the moisture sensor: ", moisture_percent)
    return moisture_percent


def check_displacement():
    read_url2 = 'https://api.thingspeak.com/channels/1794023/feeds.json?api_key='
    read_key2 = 'FE77LV8BARRFSNXX'
    read_header2 = '&results=2'
    new_url2 = read_url2 + read_key2 + read_header2
    get_data2 = requests.get(new_url2).json()
    global displacement
    try:
        displacement = get_data2['feeds'][1][str('field3')]
    except IndexError:
        displacement = "0"
    print("output value from the displacement sensor: ", displacement)
    return displacement


def send_mail(subject, body, head):
    sender_email = "brightfutureaspirants3@gmail.com"
    rec_email = "twdraji1999@gmail.com"
    password = "tycymiogximroqeg"
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, password)
        msg = f'Subject: {subject}\n\n{body}'
        smtp.sendmail(sender_email, rec_email, msg)
    print(f'{head} email has been sent to', rec_email)


total = 0
Alert = False
Alert_d_l = False
Alert_d_h = False
while True:
    check_displacement()
    subjectd1= 'Alert from Node-1 thingspeak python'
    bodyd1 = f'Displacement of the slope reached the threshold in the node-1, the displacement is {displacement} mm'
    subjectd2 = 'High Alert from Node-1 thingspeak python'
    bodyd2 = f'Displacement of the slope reached the higher threshold in the node-1, the displacement is {displacement} mm'
    if int(displacement) >= 10:
        print("Alert displacement is more that 10mm from node 1")
        if not Alert_d_l:
            send_mail(subjectd1, bodyd1, "Alert displacement from Node-1")
            Alert_d_l = True
    if int(displacement) >= 20:
        print("Alert displacement is more that 20mm from node 1")
        if not Alert_d_h:
            send_mail(subjectd2, bodyd2, "High Alert displacement from Node-1")
            Alert_d_h = True
    check_moisturecontent()
    subject1 = 'Alert from Node-1 thingspeak python'
    body1 = f'Moisture level is high in the slope right now from the node 1 the moisture content is {moisture_percent} %'
    subject2 = 'Alert from Node-1 thingspeak python'
    body2 = f'Moisture level is reduced in the slope right now from the node 1 the moisture content is {moisture_percent} %'
    subject3 = 'High Alert from Node-1 thingspeak python'
    body3 = f'Moisture level is been high for last one hour from the node 1 right now the moisture content is {moisture_percent} %'
    if int(moisture_percent) >= 50:
        print("Alert moisture level is more than 50% from the node 1")
        total = total + 25
        if not Alert:
            send_mail(subject1, body1, "Alert from the Node-1")
            Alert = True
            #urllib.request.urlopen('https://maker.ifttt.com/trigger/alertmoisturelevel/json/with/key/cIbli6YWlFgARft-yXyWSP')
            print("Alert sent by text")
    elif int(moisture_percent) < 50:
        print("Alert moisture level is less than 50% from the node 1")
        if Alert:
            send_mail(subject2, body2, "Alert retired")
            #urllib.request.urlopen('https://maker.ifttt.com/trigger/removealertmoisturelevel/json/with/key/cIbli6YWlFgARft-yXyWSP')
            print("No Alert sent by text")
            Alert = False
            total = 0
    if total >= 3600:
        total = 0
        send_mail(subject3, body3, "High alert")
        #urllib.request.urlopen('https://maker.ifttt.com/trigger/removealertmoisturelevel/json/with/key/cIbli6YWlFgARft-yXyWSP')
        print("High Alert sent by text")
    time.sleep(20)