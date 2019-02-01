#!/usr/bin/env python3.5
import requests
import os
import sys
import json
from lxml import html
import readline
import argparse


url = ''


def get_args():
    parser = argparse.ArgumentParser(description='Change status in EtaInango', prog=os.path.basename(__file__))
    parser.add_argument('-s', '--status', action='store_true', help='Show only status')
    return parser.parse_args()


def get_status(data):
    response = requests.get(url)
    tree = html.fromstring(response.text)
    items_lxml = tree.xpath('//tr[@class = "display_row"]')[0]
    name_link = items_lxml.xpath('//td/text()')
    status_person = name_link[name_link.index(data['left_fullname']) + 1]
    return status_person


def change_status(data, status_person):
    if (status_person == 'Work Report'):
        data["left_inout"] =  "Arrival"
        response = requests.post(url, data=data)
    elif (status_person == 'Arrival'):
        data["left_inout"] =  "Work Report"
        response = requests.post(url, data=data)


if __name__ == '__main__':
    data = {
    "left_fullname": "",
    "employee_passwd": "",
    "left_inout": "Arrival",
    "left_notes": "",
    "submit_button": "Submit",
    }
    args = get_args()
    show_status = str(args.status).lower()
    status = get_status(data)
    if show_status=='true':
        print('{} has status {}'.format(data["left_fullname"], status))
    else:
        print('{} has status {}'.format(data["left_fullname"], status))
        change_status(data, status)
        status = get_status(data)
        print('{} new status {}'.format(data["left_fullname"], status))
