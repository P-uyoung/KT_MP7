from django.shortcuts import render
from openai import OpenAI
from .models import ChatHistory

client = OpenAI(api_key="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")
# Create your views here.


#chatGPT에게 채팅 요청 API
def chatGPT(prompt):
    completion = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}])
    print(completion)
    result = completion.choices[0].message.content
    return result

def your_view(request):
    if request.method == 'POST':
        prompt = request.POST.get('question')
        result = chatGPT(prompt)
    else:
        result = None

    chat_history = ChatHistory.objects.all().order_by('-created_at')  # 최신 대화부터 표시
    return render(request, 'your_template.html', {'chat_history': chat_history, 'result': result})


#chatGPT에게 그림 요청 API
def imageGPT(prompt):
    response = client.images.generate(prompt=prompt,
    n=1,
    size="256x256")
    result =response['data'][0]['url']
    return result

def index(request):
    return render(request, 'gpt/index.html')

def chat(request):
    #post로 받은 question
    prompt = request.POST.get('question')

    #type가 text면 chatGPT에게 채팅 요청 , type가 image면 imageGPT에게 채팅 요청
    result = chatGPT(prompt)
    
    # 새로운 대화 기록을 데이터베이스에 저장
    ChatHistory.objects.create(user_message=prompt, gpt_response=result)
    
    # 데이터베이스에서 모든 대화 기록을 조회
    chat_history = ChatHistory.objects.all().order_by('created_at')
    sessions = ChatHistory.objects.values_list('session_id', flat=True).distinct()

    context = {
        'question': prompt,
        'result': result,
        'chat_history': chat_history,
        'sessions' : sessions
    }

    return render(request, 'gpt/result.html', context) 