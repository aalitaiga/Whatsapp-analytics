# -*- coding: UTF-8 -*-

""" Script to analyse whatsapp data """
from datetime import datetime as dt
import pandas as pd


def get_data(filename):
	with open(filename, 'r') as f:
		lines = f.readlines()

	d = []
	for line  in lines:
		d.append(process_line)

	df = pd.DataFrame(d)
	return df


def process_line(line):
	d = {
		'Jan': 'January', 'Feb': 'February', 'Mars': 'March', 'Avr': 'April',
		'Mai': 'May', 'Juin': 'June', 'Juil': 'July', 'Sep': 'September',
		'Oct': 'October', 'Nov': 'November', 'Dec': 'December'
	}

	date, rest_line = line.split(" - ")
	date = date.split(" ")
	date[2] = d[date[2]]
	new_date = " ".join(date)
	date = dt.datetime(new_date, "%d %B à %X")
	author, text = rest_line.split(": ")

	return {
		'author': author, 'date': date, 'text': text
	}




