#encoding=utf8
from xlwt import *

class Save_Excle:

	def __init__(self):
		self.count = 0
		self.book = Workbook()
		self.sheet1 = self.book.add_sheet('Sheet 1')

	def write_excle(self,templist):
		for x in range(len(templist)):
			print(self.count,x,templist[x])
			self.sheet1.write(self.count,x,templist[x])
		self.count+=1
	
	def store_excle(self,xlsfile):
		self.book.save(xlsfile)