# -*- coding: UTF-8 -*-

import unittest
from main import (
	get_data, process_line
)
from datetime import datetime as dt



class WhatsappAnalyticsTest(unittest.TestCase):

	def test_process_line(self):
		line = "7 Nov à 14:10 - Samy Ouardini: Mehdi lova lova"
		processed_line = process_line(line)

		self.assertTrue(isinstance(processed_line, dict))
		self.assertEqual(processed_line['author'], 'Samy Ouardini')
		self.assertEqual(processed_line['text'], "Medhi lova lova")
		print processed_line['date']
		self.assertTrue(isinstance(processed_line['date'], dt.datetime))