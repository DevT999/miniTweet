# parsing data from the client
from rest_framework.parsers import JSONParser
# To bypass having a CSRF token
from django.views.decorators.csrf import csrf_exempt
# for sending response to the client
from django.http import HttpResponse, JsonResponse
# API definition for tweet
from .serializers import TweetSerializer
# Tweet model
from .models import Tweet

@csrf_exempt
def tweets(request):
    if(request.method == 'GET'):
        tweets = Tweet.objects.all()
        serializer = TweetSerializer(tweets, many=True)
        return JsonResponse(serializer.data,safe=False)
    elif(request.method == 'POST'):
        data = JSONParser().parse(request)
        serializer = TweetSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)