import calendar
from datetime import datetime

class clndr():
	def year(self, x):
		yy = x
		print(calendar.calendar(yy))


	def month(self, x, z):
		yy = x or datetime.now().year
		mm = z or datetime.now().month
		
		print(calendar.month(yy, mm))  
clndr = clndr()
clndr.month(0, 0)