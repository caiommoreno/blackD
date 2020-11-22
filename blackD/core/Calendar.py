import calendar
from datetime import datetime

class clndr():
	def year(self, x):
		yy = x
		year = calendar.calendar(yy)
		return year


	def month(self, x, z):
		yy = x or datetime.now().year
		mm = z or datetime.now().month
		month = calendar.month(yy, mm)
		return month
clndr = clndr()
clndr.month(0, 0)