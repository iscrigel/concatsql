#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__	= "@iscenigmax || Carlos A. Sanchez"
__version__ = "1.0.0"
__license__ = "MIT"
__email__ 	= "ing.casr@gmail.com"
__status__ 	= "Prototype"

"""
Concat-SQL
Arguments
	-e 	= [Run the process with the information contained in config.json]
	-u  = [Upgrade config.json with the information sent in the additional parameters]
		pathfiles="path0,path1,path2"	[Flights in the wrapper file folders]
		namefile="complete.sql"			[Output file name and path]
		openfile=1 						[Open file generated after execution]
		fromdate="yyyy-MM-dd"			[Filter files more equal date]
		todate="yyyy-MM-dd"				[Filter files with same date less]
	-l = [List configuration config.json]
	-v = [Check parameters config.json]

TODO(@iscenigmax): 
	-Send file via FTP or email
	-Compatibility to respond through a browser
"""

import datetime, getopt, json, sys, os, time
from glob import glob

class App(object):
	def __init__(self):
		try:
			self.options, remainder = getopt.getopt(sys.argv[1:], 'elvru:')
			self.config = Config()
	   	except getopt.GetoptError as err:
			self.ExitApp(err)

	def usage(self):
		for o, a in self.options:
			if o == '-e':
				self.Execute()
			elif o == '-l':
				self.getList()
			elif o == '-v':
				self.Valid()
			elif o == '-u':
				self.Save(a)
			else:
				self.ExitApp('Option not available')

	def getList(self):
		data = self.config.getListParameter()
		for key,value in data.items():
			if isinstance(value, list):
				print 'KEY=',key,'	VALUE=\n['
				for item in value:
					print ' item=',item
				print ']'
			else:
				print 'KEY=',key,'	VALUE=',value

	def Valid(self):
		data = self.config.getListParameter()

		if len(data) == 0:
			self.ExitApp('File config.json is empty')
		elif not data.has_key('pathfiles'):
			self.ExitApp('The property is empty pathfiles config.json')
		else:
			listPath = data['pathfiles']
			if len(listPath) == 0:
				self.ExitApp('The route list is empty')
			else:
				for path in listPath:
					if len(path) == 0:
						self.ExitApp('The value of path is empty')

		MsgApp('config.json valid')
		return True

	def Save(self,data):
		for item in data.split(','):
			values = item.split('=')
			if len(values) < 2:
				self.ExitApp('Does not meet the requirements of [KEY]=[VALUE]')
			if values[0] == 'namefile':
				if len(values[1]) == 0:
					self.ExitApp('filename requires a file name at least one character')
			elif values[0] == 'openfile':
				if values[1] not in ['1','0']:
					self.ExitApp('openfile requires a binary value of 1 or 0')
			elif values[0] in ['todate','fromdate']:
				if len(values[1]) == 0:
					self.ExitApp('todate or fromdate requires a date value YYYY-MM-DD valid')
				try:
					datetime.datetime.strptime(values[1],'%Y-%m-%d')
				except:
					self.ExitApp('todate or fromdate requires a valid date format YYYY-MM-DD valid')
			elif values[0] == 'pathfiles':
				if len(values[1].split(',')) == 0:
					self.ExitApp('pathfiles requires at least one route to record')

			self.config.setParameter(values[0],values[1])
			MsgApp('%s recorded with the value %s successfully' % (values[0],values[1]))

	def Execute(self):
		if self.Valid():
			paths = self.config.getParameter('pathfiles')
			fromdate = self.config.getParameter('fromdate')
			todate = self.config.getParameter('todate')
			openfile = self.config.getParameter('openfile')

			nameResult = self.config.getParameter('namefile')
			if len(nameResult) == 0:
				nameResult = time.strftime('%Y%m%d%H%M%S')

			fileW = open(nameResult,'wb+')
			for path in paths:
				for files in glob('%s/*.sql' % path):
					if os.path.isfile(files):
						addfile = True

						if len(todate) > 0:
							ultima_modificacion = time.strftime('%Y-%m-%d', time.gmtime(os.path.getmtime(files)))
							if ultima_modificacion > todate:
								addfile = False

						if len(fromdate) > 0:
							ultima_modificacion = time.strftime('%Y-%m-%d', time.gmtime(os.path.getmtime(files)))
							if ultima_modificacion <= fromdate :
								addfile = False
						
						if addfile:
							fileW.write('\n\n/*\nFile add %s %s\n*/\n\n' % (time.strftime('%Y/%m/%d %H:%M:%S'),files))
							fileR = open(files,'r')
							fileW.write(fileR.read())
							fileR.close()
			fileW.close()
			if openfile == 1:
				os.startfile(nameResult)

			MsgApp('Execution completed successfully')

	def ExitApp(self, msg):
		print  'Oups :( !!!',msg,'!!!'
		sys.exit(2)

class Config(object):
	def __init__(self):
		if os.path.exists('config.json'):
			self.archivo = open('config.json', 'r')
			try:
				self.data = json.load(self.archivo)
			except:
				MsgApp('The file is corrupt or without config.json correct format, will be reconstructed to the base')
				self.Rebuild()
		else:
			self.Rebuild()
		self.archivo.close()

	def setParameter(self, key, value):
		if key == 'pathfiles':
			self.data[key].append(value)
		else:
			self.data[key] = value
		
		self.archivo = open("config.json","wb+")
		json.dump(self.data,self.archivo)
		self.archivo.close()

	def getParameter(self,key):
		return self.data[key]

	def getListParameter(self):
		return self.data

	def Rebuild(self):
		self.data = {'pathfiles':[],'namefile':'','openfile':0,'fromdate':'','todate':''}
		self.archivo = open("config.json","wb+")
		json.dump(self.data,self.archivo)

def MsgApp(msg):
	print  ':) !!!',msg,'!!!'

def main():
	app = App()
	app.usage()

if __name__ == "__main__":
   main()