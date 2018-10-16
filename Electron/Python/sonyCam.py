import urllib.request
from urllib.request import getproxies
from urllib.request import urlopen
from urllib.request import ProxyHandler
from urllib.request import build_opener
from urllib.request import install_opener
import json
import time
import re

class sonyCam:

	proxy_support = urllib.request.ProxyHandler({'https': 'http://proxy.anan-nct.ac.jp:8080'})
	opener = urllib.request.build_opener(proxy_support)
	urllib.request.install_opener(opener)

	url = 'http://192.168.122.1:8080/sony/camera'
	header = {'Content-Type': 'application/json'}
	timeout = 5.0

	def parseJson(self,json_str):
		json_dict = json.loads(json_str)
		result = None
		try:
			result = '{}'.format(json_dict['result'])
		except:
			result = '{}'.format(json_dict['error'])
		finally:
			value = result.strip('[\'\"]')
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

	# 実行しないと接続が完了しません
	# 実行後しばらく待たないとAPIが動きません(5～7秒程度)
	def startRecMode(self):
		return self.request('startRecMode','')

	# 写真を撮影後、その写真のURLを返します
	# URLは、次の写真を撮るまで使えます
	def actTakePicture(self):
		return self.request('actTakePicture','')

	# ライブビューのストリームのURLを返します
	def startLiveview(self):
		return self.request('startLiveview','')

	# ライブビューのストリームを停止します
	def stopLiveview(self):
		return self.request('stopLiveview','')

	# シャッターを半押しします
	def actHalfPressShutter(self):
		return self.request('actHalfPressShutter','')

	# シャッターの半押しを解除します
	def cancelHalfPressShutter(self):
		return self.request('cancelhalfPressShutter','')

	# F値を設定します
	def setFNumber(self,num):
		return self.request('setFNumber',num)

	# 設定されているF値を取得します
	def getFNumber(self):
		return self.request('getFNumber','')

	# 対応しているF値を取得します
	def getSupportedFNumber(self):
		return self.request('getSupportedFNumber','')

	# 設定されているF値と変更可能なF値を取得します
	def getAvailableFNumber(self):
		return self.request('getAvailableFNumber','')

	# ポストビュー(actTakePictureやawaitTakePictureでのレスポンスの画像)のサイズを設定します
	def setPostviewImageSize(self,size):
		return self.request('setPostviewImageSize',size)

	# 設定されているポストビューの大きさを取得します
	def getPostviewImageSize(self):
		return self.request('getPostviewImageSize','')

	# 対応しているポストビューの大きさを取得します
	def getSupportedPostviewImageSize(self):
		return self.request('getSupportedPostviewImageSize','')

	# 設定されているポストビューの大きさと変更可能なポストビューの大きさを取得します
	def getAvailablePostviewImageSize(self):
		return self.request('getAvailablePostviewImageSize','')

	# ISO感度を設定します
	def setIsoSpeedRate(self,num):
		return self.request('setIsoSpeedRate','\''+num+'\'')

	# 設定されているISO感度を取得します
	def getIsoSpeedRate(self):
		return self.request('getIsoSpeedRate','')

	# 対応しているISO感度を取得します
	def getSupportedIsoSpeedRate(self):
		return self.request('getSupportedIsoSpeedRate','')

	# 設定されているISO感度と変更可能なISO感度を取得します
	def getAvailableIsoSpeedRate(self):
		return self.request('getAvailableIsoSpeedRate','')

	# シャッタースピードを設定します
	def setShutterSpeed(self,num):
		return self.request('setShutterSpeed','\''+num+'\'')

	# 対応しているシャッタースピードを取得します
	def getSupportedShutterSpeed(self):
		return self.request('getSupportedShutterSpeed','')

	# 設定されているシャッタースピードを取得します
	def getShutterSpeed(self):
		return self.request('getShutterSpeed','')

	# 設定されているシャッタースピードと変更可能なシャッタースピードを取得します
	def getAvailableShutterSpeed(self):
		return self.request('getAvailableShutterSpeed','')

	# カメラとの接続を切ります
	def stopRecMode(self):
		return self.request('stopRecMode','')

	# 写真が撮れるか確認します
	def canTakePicture(self):
		result = self.request('getEvent','false')
		value = result.find('actTakePicture') >= 0
		return value

if __name__ == '__main__':
	cam = sonyCam()

	# 実行しないと接続が完了しません
	# 実行後しばらく待たないと準備が完了しません
	if cam.canTakePicture():
		print(cam.parseJson(cam.actTakePicture()))
	else:
		print(False)

	# set系のメソッドの引数は、文字列で指定するようにしています
	# parseJson()で、actTakePicture()やstartLiveview()で返ってくるJsonからURLを抜き出せます
	# エラーが返ってきたときは、エラーコードとエラーの内容が取り出せます