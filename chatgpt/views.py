from django.shortcuts import render
from django.http import HttpResponse
import openai
# Create your views here.

openai.api_key = "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"


#chatGPT에게 채팅 요청 API
def chatGPT(prompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    print(completion)
    result = {completion.choices[0].message.content}
    return result

#chatGPT에게 그림 요청 API
def imageGPT(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="256x256"
    )
    result =response['data'][0]['url']
    return result

def index(request):
    return render(request, 'chatgpt/index.html')

def chat(request):
    #post로 받은 question
    prompt = request.POST.get('question')
    #type text or image
    type = request.POST.get('type')

    #type가 text면 chatGPT에게 채팅 요청 , type가 image면 imageGPT에게 채팅 요청
    if type == 'text':
        result = chatGPT(prompt)
    elif type == 'image':
        result = imageGPT(prompt)
    return HttpResponse(result) 

