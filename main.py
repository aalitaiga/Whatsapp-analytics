# -*- coding: UTF-8 -*-

""" Script to analyse whatsapp data """
import datetime as dt
import pandas as pd
import re

from utils import *

# Improve way action are handled
string = r"""(?P<date>\d{1,2} \w{3,4} à \d{1,2}:\d{2}) - (?P<name>[\+\w]+(?::\s*[\w\+]+)*|[\+\w\s]+?)(?:\s(?P<action>a été ajouté\(e\)|est parti|a retiré [^\n]*|a changé (?:le sujet en ”.*?”|l'icône de ce groupe|de [^à]+à [^\n]*))|:)(?P<message>.*?)(?=\s*\d{1,2} \w{3,4} à \d{1,2}:\d{2}|$)"""
regex = re.compile(string)

french_d = {
		'Jan': '01', 'Feb': '02', 'Mars': '03', 'Avr': '04',
		'Mai': '05', 'Juin': '06', 'Juil': '07', 'Aout': '08',
		'Sep': '09', 'Oct': '10', 'Nov': '11',
		'Dec': '12'
	}

def get_data(filename):
	with open(filename, 'r') as f:
		lines = f.readlines()
	data = ''.join(lines)
	matches = re.finditer(regex, data)
	df =  pd.DataFrame([match.groupdict() for match in matches])
	return clean_data(df)


def clean_data(df):
	# Change format to dd mm HH:mm
	df.apply(format_date, axis=1)
	# Then to dd mm HH:mm YYYY
	year_serie = get_year(df)
	df['date'] = df.date + ' ' + year_serie.astype(str)

	df['date'] = pd.to_datetime(df['date'], format="%d %m %H:%M %Y")
	df.loc[df.message != '', 'action'] = 'message'
	df.loc[df.message == '', 'message'] = pd.np.nan
	return df

	
def format_date(row):
	day, month, _, message_time = row['date'].split(' ')
	# zero-padding for day and time
	if len(day) == 1:
		day = '0' + day
	if len(message_time.split(':')[0]) == 1:
		message_time = '0' + message_time
	row['date'] = ' '.join([day, french_d[month], message_time])
	return row

def get_year(df):
	months = df['date'].apply(lambda x: x.split(' ')[1])
	a = dt.datetime.now().month
	b = dt.datetime.now().year
	l = []

	for _, row in months[::-1].iteritems():
		if row <= a:
			l.append(b)
		else:
			l.append(b-1)
			b -= 1
		a = row
	return  pd.Series(l[::-1])

# English regex
# (?P<date>\d{2}\/\d{2}\/\d{2} \d{2}:\d{2}:\d{2}): 
# (?P<name>\w+(?::\s*\w+)*|[\w\s]+?)(?:\s+(?P<action>joined|left|was removed|changed 
#	the (?:subject to “\w+”|group icon))|:\s(?P<message>(?:.+|\n(?!\n))+))
#
# French regex
# (?P<date>\d{1,2} \w{3,4} à \d{1,2}:\d{2}) - 
# (?P<name>[\+\w]+(?::\s*[\w\+]+)*|[\+\w\s]+?)(?:\s(?P<action>a été ajouté\(e\)
# |est parti|a retiré [^\n]*|a changé (?:le sujet en ”.*?”|l'icône de ce groupe
# de [^à]+à [^\n]*))|:)(?P<message>.*?)(?=\s*\d{1,2} \w{3,4} à \d{1,2}:\d{2}|$)

if __name__ == '__main__':
	df = get_data('1H_2.txt')
	gb

