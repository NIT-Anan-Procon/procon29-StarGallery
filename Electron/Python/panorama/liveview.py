import threading
import getStreamImage
import json
import urllib.request
from urllib.request import getproxies
from urllib.request import urlopen
from urllib.request import ProxyHandler
from urllib.request import build_opener
from urllib.request import install_opener
import json

class liveview:

	proxy_support = urllib.request.ProxyHandler({'https': 'http://proxy.anan-nct.ac.jp:8080'})
	opener = urllib.request.build_opener(proxy_support)
	urllib.request.install_opener(opener)

	def parseJson(self,json_str):
		json_dict = json.loads(json_str)
		result = None
		try:
			result = '{}'.format(json_dict['result'])
		except:
			return None
		finally:
			value = result.replace('\'','')
			while value.find('[') == 0:
				value = value[1:-1]
			return value

	def request(self,method,params):
		url = "http://192.168.122.1:8080/sony/camera"
		obj = '{\'method\' : ' + method + ',\'params\' : ['+params+'],\'id\' : 1,\'version\' : \'1.0\'}'
		print(obj)
		json_data = obj.encode("utf-8")
		headers = {"Content-Type" : "application/json"}

		request = urllib.request.Request(url, data=json_data, headers=headers, method='POST')
		with urllib.request.urlopen(request) as response:
			response_body = response.read().decode("utf-8")

		return response_body

	def startRecMode(self):
		return self.request('startRecMode','')

	# ライブビューのストリームのURLを返します
	def startLiveview(self):
		return self.parseJson(self.request('startLiveview',''))

	# ライブビューのストリームのURLを返します
	def stopLiveview(self):
		return self.parseJson(self.request('stopLiveview',''))

	def startGetImage(self,url):
		getImg = getStreamImage.getStreamImage()
		if getImg.start(url):
			print('getImg finish')
		else:
			print('getImg error')

	def start(self):
		print('start liveview')
		try:
			self.startRecMode()
			resultUrl = self.startLiveview()
			if resultUrl is None:
				print('startLiveview error')
			else:
				print(resultUrl)
				thread_obj = threading.Thread(target=self.startGetImage, kwargs={'url':resultUrl})
				thread_obj.start()
		except:
			print('start error')
