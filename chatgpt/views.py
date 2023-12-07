from django.shortcuts import render
from openai import OpenAI
from .models import ChatHistory
from django.db.models import Max

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
    
    # ChatHistory 모델에서 session_id의 최대값을 구함
    max_session_id = ChatHistory.objects.aggregate(Max('session_id'))['session_id__max']
    # 인스턴스가 없을 경우 max_session_id는 None이 될 것이므로, 이 경우 next_session_id를 1로 설정
    next_session_id = int(max_session_id or 0) + 1
    
    # 새로운 대화 기록을 데이터베이스에 저장
    ChatHistory.objects.create(session_id=next_session_id, user_message=prompt, gpt_response=result)
    
    # 현재 세션 ID의 대화 기록만 조회
    chat_history = ChatHistory.objects.filter(session_id=next_session_id).order_by('created_at')

    context = {
        # 'question': prompt,
        # 'result': result,
        'chat_history': chat_history,
        'current_session_id' : next_session_id,
        'sessions' : list(range(1,int(next_session_id)+1))
    }

    return render(request, 'gpt/result.html', context) 

def rechat(request):
    if request.method == 'POST':
        
        prompt = request.POST.get('question')  # post로 받은 question
        current_session_id = request.POST.get('session_id')

        result = chatGPT(prompt)
        ChatHistory.objects.create(session_id=current_session_id, user_message=prompt, gpt_response=result) # 새로운 대화 기록을 데이터베이스에 저장
        
        
    else:  # 선택된 세션의 채팅 기록을 표시
        current_session_id = request.GET.get('session_id')

    chat_history = ChatHistory.objects.filter(session_id=current_session_id).order_by('created_at')
    sessions = ChatHistory.objects.values_list('session_id', flat=True).distinct()
    
    # ChatHistory 모델에서 session_id의 최대값을 구함
    max_session_id = ChatHistory.objects.aggregate(Max('session_id'))['session_id__max']
    # 인스턴스가 없을 경우 max_session_id는 None이 될 것이므로, 이 경우 next_session_id를 1로 설정
    next_session_id = int(max_session_id or 0) + 1
    
    # 새로운 대화 기록을 데이터베이스에 저장
    ChatHistory.objects.create(session_id=next_session_id, user_message=prompt, gpt_response=result)
    
    # 현재 세션 ID의 대화 기록만 조회
    chat_history = ChatHistory.objects.filter(session_id=next_session_id).order_by('created_at')

    context = {
        # 'question': prompt,
        # 'result': result,
        'chat_history': chat_history,
        'current_session_id' : next_session_id,
        'sessions' : list(range(1,int(next_session_id)+1))
    }

    return render(request, 'gpt/result.html', context) 

def rechat(request):
    if request.method == 'POST':
        
        prompt = request.POST.get('question')  # post로 받은 question
        current_session_id = request.POST.get('session_id')

        result = chatGPT(prompt)
        ChatHistory.objects.create(session_id=current_session_id, user_message=prompt, gpt_response=result) # 새로운 대화 기록을 데이터베이스에 저장
        
        
    else:  # 선택된 세션의 채팅 기록을 표시
        current_session_id = request.GET.get('session_id')

    chat_history = ChatHistory.objects.filter(session_id=current_session_id).order_by('created_at')
    sessions = ChatHistory.objects.values_list('session_id', flat=True).distinct()

    context = {
        # 'question': prompt,
        # 'result': result,
        'chat_history': chat_history,
        'current_session_id' : current_session_id,
        'sessions' : sessions,
        # 'question': prompt,
        # 'result': result,
        'chat_history': chat_history,
        'current_session_id' : current_session_id,
        'sessions' : sessions
    }

    return render(request, 'gpt/result.html', context) 