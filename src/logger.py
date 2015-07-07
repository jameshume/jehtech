import thread
import re
import time
import sqlparse
import traceback
import pprint

class DebugPrinter(object):
	THREAD_ID_COL_WIDTH = 4
	TIME_COL_WIDTH      = 6

	def __init__(self, indentSpaces=3, printThreadId=True, printTimestamp=True):
		self._enabled = False
		self._indentForThread = {}
		self._nameForThread = {}
		self._threadCounter = 0
		self._indentSpaces = indentSpaces
		self._lock = thread.allocate_lock()
		self._printThreadId = printThreadId
		self._printTimestamp = printTimestamp
		self._createdTime = time.time()

	def __IncreaseIndent(self, threadId):
		assert(self._enabled)
		assert(self._lock.locked())
		self._indentForThread[threadId] = self._indentForThread.get(threadId, 0) + self._indentSpaces

	def __DecreaseIndent(self, threadId):
		assert(self._enabled)
		assert(self._lock.locked())
		self._indentForThread[threadId] = self._indentForThread.get(threadId, 0) - self._indentSpaces
		if self._indentForThread < 0:
			self._indentForThread = 0

	def GetIndent(self):
		with self._lock:
			threadId = thread.get_ident()
			indent =  self._indentForThread[threadId]
			if self._printThreadId: 
				indent += self.THREAD_ID_COL_WIDTH
			if self._printTimestamp:
				indent += self.TIME_COL_WIDTH
			return indent

	def IncreaseIndent(self):
		with self._lock:
			if self._enabled:
				self.__IncreaseIndent(thread.get_ident())

	def DecreaseIndent(self):
		with self._lock:
			if self._enabled:
				self.__DecreaseIndent(thread.get_ident())

	def __TheadIdColString(self, threadId, title=None):
		assert(self._enabled)
		assert(self._lock.locked())
		if threadId not in self._nameForThread:
			self._nameForThread[threadId] = self._threadCounter
			self._threadCounter += 1

		if self._printThreadId: 
			if title is None: return "{0:>{width}x}| ".format(self._nameForThread[threadId], width=self.THREAD_ID_COL_WIDTH)
			else:             return "{0:>{width}}| ".format(title, width=self.THREAD_ID_COL_WIDTH)
		else:
			return ""

	def __TimestampColString(self, title=None):
		assert(self._enabled)
		assert(self._lock.locked())
		if self._printTimestamp: 
			if title is None:
				return "{0:>{width}.0f}| ".format(round(time.time() - self._createdTime, 2) * 100, width=self.TIME_COL_WIDTH)
			else:
				return "{0:>{width}}| ".format(title, width=self.TIME_COL_WIDTH)
		else:
			return ""

	def PrintTitle(self, string):
		with self._lock:
			if self._enabled:
				threadId = thread.get_ident()
				print self.__TheadIdColString(threadId),
				print self.__TimestampColString(),
				print " " * self._indentForThread.get(threadId, 0),
				print string,
				print "{"
				self.__IncreaseIndent(threadId)

		return self

	def __enter__(self):
		pass

	def __exit__(self, extype, exvalue, extb):
		if extype is not None:
			self.Print('----------------------------------')
			self.Print('--- AN EXCEPTION OCCURRED HERE ---') 
			self.Print(' '.join(traceback.format_exception(extype, exvalue, extb)))
			self.Print('----------------------------------')
		self.EndTitle()
		return False # Don't suppress any exceptions!

	def EndTitle(self):
		with self._lock:
			if self._enabled:
				threadId = thread.get_ident()
				self.__DecreaseIndent(threadId)
				print self.__TheadIdColString(threadId),
				print self.__TimestampColString(),
				print " " * self._indentForThread[threadId],
				print "}"

	def Print(self, string):
		with self._lock:
			if self._enabled:
				threadId = thread.get_ident()
				print self.__TheadIdColString(threadId),
				print self.__TimestampColString(),

				padding            = " " * self._indentForThread.get(threadId, 0)
				newLineReplPadding = "\n{} {}  ".format(self.__TheadIdColString(threadId), self.__TimestampColString('...')) + padding
				print padding,
				print re.sub(r'[\n\r]+', newLineReplPadding, string)

	def PrintObject(self, obj, title=None):
		if title is not None:
			self.Print(title)
			self.IncreaseIndent()
		self.Print(pprint.pformat(obj, indent=2))
		if title is not None:
			self.DecreaseIndent()
	
	def PrintSQL(self, sqlString):
		self.PrintTitle("Executing SQL")
		self.Print( sqlparse.format(sqlString, reindent=True, keyword_case='upper') )
		self.EndTitle()

	def Enable(self):
		with self._lock:
			self._enabled = True
	
	def Disable(self):
		with self._lock:
			self._enabled = False


PRINTER = DebugPrinter()

def GetDebugPrinter():
	return PRINTER


