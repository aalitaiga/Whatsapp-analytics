# -*- coding: UTF-8 -*-

import unittest
import datetime as dt
from main import (
	get_data, process_line
)


class WhatsappAnalyticsTest(unittest.TestCase):

	def test_process_line(self):
		line = "07 Nov à 14:10 - Samy Ouardini: Mehdi lova lova"
		processed_line = process_line(line)

		self.assertTrue(isinstance(processed_line, dict))
		self.assertEqual(processed_line['author'], 'Samy Ouardini')
		self.assertEqual(processed_line['text'], "Mehdi lova lova")
		self.assertTrue(isinstance(processed_line['date'], dt.datetime))

	def test_get_data(self):
		data = get_data("1H.txt")
		self.assertFalse(data.empty)
		print data.head()


if __name__ == '__main__':
	unittest.main()