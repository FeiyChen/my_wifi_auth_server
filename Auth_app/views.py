from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from Auth_app.forms import PwdForm
from Auth_app.models import User, FL_freq
from Auth_app.extract import extract_cf
from django.views.decorators.csrf import csrf_exempt
import json
import os
import time

from datetime import timedelta
from django.core.signing import TimestampSigner
from bloom_filter import BloomFilter #bloomfilter stores the multiple characteristic frequencies 
signer = TimestampSigner()

bloom = BloomFilter(max_elements = 100000)
freq = range(15300,15500)
for f in freq:
	bloom.add(f)


# Create your views here.
def home(request):
	if request.GET:
		# import pdb;pdb.set_trace()
		# user_list = User.objects.all()
		# User.objects.all().delete()
		# import pdb;pdb.set_trace()
		res = User.objects.get_or_create(mac = request.GET['mac'])
		User.objects.filter(mac = request.GET['mac']).update(gw_id = request.GET['gw_id']\
			,gw_address=request.GET['gw_address'],gw_port=request.GET['gw_port'],url=request.GET['url'])
		# res[0].gw_id = request.GET['gw_id']
		# res[0].gw_address=request.GET['gw_address']
		# res[0].gw_port=request.GET['gw_port']
		# res[0].url=request.GET['url']
		# res[0].save()
		# import pdb;pdb.set_trace()
		# User.objects.create(gw_id=request.GET['gw_id'],gw_address=request.GET['gw_address'],mac=request.GET['mac'],gw_port=request.GET['gw_port'],url=request.GET['url'])
		# received_get['gw_id'] = request.GET['gw_id']
		# received_get['gw_address'] = request.GET['gw_address']
		# received_get['gw_port'] = request.GET['gw_port']
		# received_get['url'] = request.GET['url']
		# received_get['mac'] = request.GET['mac']
		# return render(request,'login.html')
		return HttpResponse('Please post the pictures')
	else:
		return HttpResponse('no Gateway information!')

@csrf_exempt
def login(request): 
	
	if request.method == 'POST':
		print('received post request!!!!!!!!!!!!!',time.ctime(time.time()))
		t2 = time.time()
		# user = User.objects.get_or_create(mac = request.POST.get('mac'))
		user = User.objects.get(mac = request.POST.get('mac'))
		print('get user!!!!!!!!!!!!!',time.ctime(time.time()))
		
		imgs = request.FILES.getlist("uploadfile",None) 
		t0 = time.time()
		print('get images!!!!!!!!!!!!',time.ctime(time.time()))
		if not imgs:
			return HttpResponse("no file for upload")
		else:
			for img in imgs:
				if os.path.exists("/home/fychen/UPloadFIle/%s" % user.mac) == False:
					os.makedirs("/home/fychen/UPloadFIle/%s" % user.mac)
				des = open(os.path.join("/home/fychen/UPloadFIle/%s" % user.mac, img.name),"wb+")
				for chunk in img.chunks():
					des.write(chunk)
				des.close()
			# return HttpResponse("upload success")
			t3 = time.time()
			print('stored the images!!!!!!!!!!!!',time.ctime(time.time()))
			print('store the images', t3 - t0)
			cf = extract_cf("/home/fychen/UPloadFIle/%s" % user.mac)
			# import pdb;pdb.set_trace()
			pwd = cf.extract()
			print('cf extracting time',time.time() - t3)
			print('authentication start!!!!!!!!!!!!!!',time.ctime(time.time()))
			if int(pwd) in bloom:
				# global token
				user.token = signer.sign(pwd)
				# import pdb;pdb.set_trace()
				user.save()
				# import pdb;pdb.set_trace()
				print('pwd success!!!!!!!!!!!!!!',time.ctime(time.time()))
				return HttpResponseRedirect('http://%s:%s/wifidog/auth?token=%s'%(user.gw_address,user.gw_port,user.token))
			else:

				# token = signer.sign(pwd)
				# return HttpResponseRedirect('http://%s:%s/wifidog/auth?token=%s'%(received_get['gw_address'],received_get['gw_port'],token))
				return HttpResponse('wrong password! Please try again.')


	# 	form = PwdForm(request.POST)

	# 	if form.is_valid():
	# 		pwd = form.cleaned_data['passwd']
	# 		# if pwd <= FL_freq.objects.all()[0].max_freq and pwd >= FL_freq.objects.all()[0].min_freq:
	# 		if isinstance(int(pwd),int) and int(pwd) in bloom:
	# 		 # and pwd in bloom:
	# 		    global token
	# 		    token = signer.sign(pwd)
	# 		    # token = '123'
	# 		    return HttpResponseRedirect('http://%s:%s/wifidog/auth?token=%s'%(received_get['gw_address'],received_get['gw_port'],token))
	# 		    # return HttpResponseRedirect('http://192.168.1.1:2060/wifidog/auth?token=%s' % token)
	# 		else: 
	# 			return HttpResponse('wrong password!')

	# 	else:
	# # 	form = PwdForm()
	# 		return HttpResponse('form is invalid')
	else:
		return HttpResponse('method = GET')

def auth(request):
	if request.GET['stage'] == 'login':
		# import pdb;pdb.set_trace()
		user = User.objects.get(mac = request.GET['mac'])
		# import pdb;pdb.set_trace()
		if request.GET['token']	== user.token:
			user.stage = request.GET['stage']
			user.ip = request.GET['ip']
			user.incoming = request.GET['incoming']
			user.outgoing = request.GET['outgoing']
			user.save()
		 # and received_get['mac'] == request.GET['mac']:
			response = HttpResponse('Auth: 1')
			# response.write("")
			return response 
			# (response, HttpResponseRedirect('/portal/?gw_id=%s' % received_get['gw_id']))
		else:
			return HttpResponse('Auth: 0')
	else:
		return HttpResponse('Auth: 0')

def ping(request):
	return HttpResponse('Pong')

def portal(request):
	# t1 = time.clock()
	# print('authentication time',t1-t0)
	print('authentication end!!!!!!!!!!!!!!',time.ctime(time.time()))
	return HttpResponse('YES')
	# return HttpResponseRedirect('www.baidu.com')
	
def msg(request):
	if request.GET:
		return HttpResponse('Auth ' + request.GET['message'])
	else:
		return HttpResponse('no message!')
