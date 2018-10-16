import threading
import queue
import os
import io
from PIL import Image
import SimpleLiveviewSlicer

class getStreamImage:

	mJpegQueue = queue.Queue(2)
	whileFetching = False
	fileName = './data.jpg'

	slicer = None


	def startRetrieve(self,streamUrl):
		self.slicer = SimpleLiveviewSlicer.SimpleLiveviewSlicer()
		self.slicer.open(streamUrl)

		try:

			while self.whileFetching:
				print('fetching...')
				payload = self.slicer.nextPayload()
				if payload is None:
					print('Liveview Payload is None')
					continue
				if self.mJpegQueue.full():
					try:
						self.mJpegQueue.get_nowait()
					except:
						print('mJpegQueue.Enpty')

				self.mJpegQueue.put_nowait(payload[0])

		except Exception as e:
			print('error while fetching', e.args)
		finally:
			self.whileFetching = False
			print('fetching finally')

	def startSaveImage(self):
		while self.whileFetching:
			try:
				print('Saving...')
				jpegData = self.mJpegQueue.get()
				image = Image.open(io.BytesIO(jpegData))
				image.save(self.fileName)
				print('Save success')
			except Exception as e:
				print('error saving image', e.args)

	def start(self,streamUrl):
		print('getImg start')

		if streamUrl is None:
			print('start() streamUrl is None')
			return False
		if self.whileFetching:
			print('start() already starting')
			return False

		self.whileFetching = True

		thread_obj1 = threading.Thread(target=self.startRetrieve, kwargs={'streamUrl':streamUrl})
		thread_obj1.start()

		thread_obj2 = threading.Thread(target=self.startSaveImage)
		thread_obj2.start()

		return True