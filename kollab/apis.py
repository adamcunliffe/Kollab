import json
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def signup(request):
	print("sign up triggered")
	if request.method == 'POST':
		formData = json.loads(request.body)
		try:
			for d in formData:
				print(d)
		except KeyError:
			HTTPResponse("Fail")

	return HTTPResponse("OK")