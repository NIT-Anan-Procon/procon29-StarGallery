import io
import binascii
import urllib.request
from urllib.request import getproxies
from urllib.request import urlopen
from urllib.request import ProxyHandler
from urllib.request import build_opener
from urllib.request import install_opener

class SimpleLiveviewSlicer:

	proxy_support = urllib.request.ProxyHandler({'https': 'http://proxy.anan-nct.ac.jp:8080'})
	opener = urllib.request.build_opener(proxy_support)
	urllib.request.install_opener(opener)

	CONNECTION_TIMEOUT = 2000

	inputStream = None

	def open(self, streamUrl):
		print('open slicer:'+streamUrl)
		if self.inputStream is None:
			self.inputStream = urlopen(streamUrl)
			print('open success')
		else:
			print('slicer already opened')
		return True


	def nextPayload(self):
		payload = None
		while self.inputStream is not None and payload is None:
			readLength = 1+1+2+4
			commonHeader = self.inputStream.read(readLength)
			headerLength = len(commonHeader)
			if commonHeader is None or headerLength is not readLength:
				print('Cannot read stream for common header.')
			if commonHeader[0] is not 0xff:
				print('Unexpected data format. (Start byte)')

			if commonHeader[1] is 0x12:
				readLength = 4+3+1+2+118+4+4+24
				commonHeader = None
				self.inputStream.read(readLength)
			elif commonHeader[1] in {0x01, 0x11}:
				payload = self.readPayload()

		print('return payload')
		return payload


	def readPayload(self):

		if self.inputStream is not None:
			readLength = 4+3+1+4+1+115
			payloadHeader = self.inputStream.read(readLength)

			if payloadHeader is None or len(payloadHeader) is not readLength:
				print('Cannot read stream for payload header.')
				return None,None

			if payloadHeader[0] is not 0x24 or payloadHeader[1] is not 0x35 or payloadHeader[2] is not 0x68 or payloadHeader[3] is not 0x79:
				print('Unexpected data format. (Start code)')
				return None,None

			jpegSize = self.bytesToInt(payloadHeader, 4, 3)
			paddingSize = self.bytesToInt(payloadHeader, 7, 1)

			jpegData = self.inputStream.read(jpegSize)
			paddingData = self.inputStream.read(paddingSize)

			return jpegData, paddingData
		else:
			return None,None


	def bytesToInt(self, byteData, startIndex, count):
		return int(binascii.hexlify(byteData[startIndex:startIndex+count]), 16)
