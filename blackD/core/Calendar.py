import calendar


class clndr():
	def year(self, x):
		yy = x
		print(calendar.calendar(yy))


	def month(self, x, z):
		yy = x
		mm = z
		
		print(calendar.month(yy, mm))  
clndr = clndr()
clndr.year(2010)