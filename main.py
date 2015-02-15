# -*- coding: UTF-8 -*-

""" Script to analyse whatsapp data """
import datetime as dt
import pandas as pd
import re

# Shorten the regex
string = r"""(?P<date>\d{1,2} \w{3,4} à \d{1,2}:\d{2}) - (?P<name>[\+\w]+(?::\s*[\w\+]+)*|[\+\w\s]+?)(?:\s(?P<action>a été ajouté\(e\)|est parti|a retiré [^\n]*|a changé (?:le sujet en ".*?"|l'icône de ce groupe|de [^à]+à [^\n]*))|:)(?P<message>.*?)(?=\s*\d{1,2} \w{3,4} à \d{1,2}:\d{2}|$)"""
regex = re.compile(string)

french_d = {
		'Jan': 'January', 'Feb': 'February', 'Mars': 'March', 'Avr': 'April',
		'Mai': 'May', 'Juin': 'June', 'Juil': 'July', 'Sep': 'September',
		'Oct': 'October', 'Nov': 'November', 'Dec': 'December'
	}

def get_data(filename):
	with open(filename, 'r') as f:
		lines = f.readlines()
	data = ''.join(lines)
	matches = re.finditer(regex, data)
	return pd.DataFrame([match.groupdict() for match in matches])


def clean_data(df):
	df.apply(format_date, axis=1)
	# Find a way to also get the year
	df['date'] = pd.to_datetime(df['date'], format="%d %B %H:%M")
	return df

	
def format_date(row):
	day, month, _, message_time = row['date'].split(' ')
	#import ipdb; ipdb.set_trace()
	# zero-padding for day and time
	if len(day) == 1:
		day = '0'.append(day)
	if len(message_time.split(':')[0]) == 1:
		message_time = '0'.append(message_time)
	row['date'] = ' '.join([day, french_d[month], message_time])
	return row


# English regex
# (?P<date>\d{2}\/\d{2}\/\d{2} \d{2}:\d{2}:\d{2}): 
# (?P<name>\w+(?::\s*\w+)*|[\w\s]+?)(?:\s+(?P<action>joined|left|was removed|changed 
#	the (?:subject to “\w+”|group icon))|:\s(?P<message>(?:.+|\n(?!\n))+))
#
# French regex
# (?P<date>\d{1,2} \w{3,4} à \d{1,2}:\d{2}) - 
# (?P<name>[\+\w]+(?::\s*[\w\+]+)*|[\+\w\s]+?)(?:\s(?P<action>a été ajouté\(e\)
# |est parti|a retiré [^\n]*|a changé (?:le sujet en ".*?"|l'icône de ce groupe
# de [^à]+à [^\n]*))|:)(?P<message>.*?)(?=\s*\d{1,2} \w{3,4} à \d{1,2}:\d{2}|$)

if __name__ == '__main__':
	print clean_data(get_data('1H_2.txt'))

