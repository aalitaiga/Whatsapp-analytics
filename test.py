# -*- coding: UTF-8 -*-

import unittest
import datetime as dt
from main import (
	get_data
)

class WhatsappAnalyticsTest(unittest.TestCase):

	def test_get_data(self):
		data = get_data("1H.txt")
		self.assertFalse(data.empty)
		print data.head()


if __name__ == '__main__':
	unittest.main()