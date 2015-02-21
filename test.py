# -*- coding: UTF-8 -*-

import unittest
import datetime as dt
import pandas as pd
from pandas.util.testing import assert_frame_equal, assert_series_equal

from main import (
	get_data, get_year, format_date
)

class WhatsappAnalyticsTest(unittest.TestCase):

	def test_get_data(self):
		data = get_data("1H.txt")
		self.assertFalse(data.empty)

	def test_format_date(self):
		test_df = pd.DataFrame([
			{'date': '12 Avr à 10:32'},
			{'date': '30 Avr à 1:09'},
			{'date': '2 Mai à 12:17'},
		])
		expected_dates = pd.DataFrame([
			'12 04 10:32',
			'30 04 01:09',
			'02 05 12:17'
		], columns=['date'])
		new_df = test_df.apply(format_date, axis=1)
		assert_frame_equal(new_df, expected_dates)

	def test_get_year(self):
		test_df = pd.DataFrame([{
			'date': '21 02 22:34'
		}])
		expected_date = int(dt.datetime.now().strftime('%Y'))
		new_df = get_year(test_df)
		if dt.datetime.now() < dt.datetime(expected_date, 02, 21, 22, 34):
			assert_series_equal(new_df, pd.Series([expected_date]))
		else:
			assert_series_equal(new_df, pd.Series([expected_date-1]))

if __name__ == '__main__':
	unittest.main()