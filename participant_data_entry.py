# -*- coding: utf-8 -*-
"""Participant Data Entry.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1b9_WVXcqR1u9LeiXzEoUY9iC7BJk4hFF
"""

import pandas as pd
import requests
import os

os.system('cls')

site = input("Enter site URL")
token = input("Enter the API KEY")
slug = input("Enter the tournament slug")

r = requests.get(
        f'{site}api/v1/institutions',
        headers={
                'Authorization': 'token '+token
                })

institutions = r.json()

x=0
sheet = pd.read_excel(open('database.xlsx', 'rb'),
                           sheet_name='Judges')


for k in sheet['Short']:

    short = sheet['Short'][x]
    institution = None
    for i in institutions:
        if i['code'] == short:
            institution = i['url']
            print(f"{Fore.YELLOW}{institution}{Style.RESET_ALL}")
            break



    name = sheet['Name'][x]
    score = sheet['Score'][x]
    email = sheet['Email'][x]
    number = sheet['Number'][x]
    gender = sheet['Gender'][x]
    if gender == 'Male':
        gender='M'
    elif gender == 'Female':
        gender='F'
    else:
        gender='O'
    x = x+1


    r = requests.post(
        f'{site}api/v1/tournaments/{slug}/adjudicators',
        json = {
        "name": name,
        "email": email,
        "anonymous": False,
        "institution": institution,
        "base_score": float(score),
        "breaking": False,
        "trainee": False,
        "independent": True,
        "adj_core": False,
        "institution_conflicts": [],
        "team_conflicts": [],
        "adjudicator_conflicts": [],
        "gender": gender
        },
        headers={
                'Authorization': 'token '+token
                })

    status = r.status_code
    print(f"{status}: {name}, {institution}")
    if status != 201:
        print(f"Error occured while posting {name}, {short}\n Error {status}\n{r.text}")

print("SUCCESSFUL")

y=0
sheet = pd.read_excel(open('database.xlsx', 'rb'),
                           sheet_name='Teams')

for k in sheet['Team']:

    name = sheet['Team'][y]
    code = sheet['Code'][y]
    for i in institutions:
        if i['code'] == code:
            institution = i['url']
            break



    S1 = sheet['S1'][y]
    E1 = sheet['E1'][y]
    P1 = '' #sheet['P1'][x]
    G1 = sheet['G1'][y]
    if G1 == 'Male':
        G1='M'
    elif G1 == 'Female':
        G1='F'
    else:
        G1='O'

    S2 = sheet['S2'][y]
    E2 = sheet['E2'][y]
    P2 = '' #sheet['P2'][x]
    G2 = sheet['G2'][y]
    if G2 == 'Male':
        G2='M'
    elif G2 == 'Female':
        G2='F'
    else:
        G2='O'

    y = y+1

    r = requests.post(
        f'{site}api/v1/tournaments/{slug}/teams',
        json = {
  "reference": name,
  "short_reference": name,
#  "code_name": "",
  "institution": institution,
  "speakers": [
    {
      "name": S1,
      "gender": G1,
      "email": E1,
      "phone": P1,
      "anonymous": False,
      "pronoun": "",
      "categories": [],
      "url_key": ""
    },
    {
      "name": S2,
      "gender": G2,
      "email": E2,
      "phone": P2,
      "anonymous": False,
      "pronoun": "",
      "categories": [],
      "url_key": ""
    }
  ],
  "use_institution_prefix": False,
  "break_categories": [],
  "institution_conflicts": []
},
        headers={
                'Authorization': 'token '+token
                })
    print(f"{name}")
    status = r.status_code
    if status != 201:
        print(f"Error occured while posting {name}\n Error {status}\n{r.text}")

print("SUCCESSFUL")