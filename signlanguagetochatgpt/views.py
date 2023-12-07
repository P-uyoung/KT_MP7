from django.shortcuts import render
from django.utils import timezone
import logging
from django.conf import settings
from django.core.files.storage import default_storage
import numpy as np
import cv2
import string
import mlflow
import mlflow.keras
from chatgpt.views import chatGPT
logger = logging.getLogger('mylogger')
from .models import ChatResult, Result

# global variable
test_sign = None

def getChatResult(self, id):
        query = "SELECT * FROM signlanguagetochatgpt_chatresult WHERE id = {0}".format(id)
        logger.info(">>>>>>>> getChatResult SQL : "+query)
        chatResult = self.t_exec(query)

def index(request):
    return render(request, 'languagechat/index.html')

def chat(request):
    global test_sign
    if request.method == 'POST' and request.FILES['files']:
        results=[]
        files = request.FILES.getlist('files')
        chatGptPrompt = ""
        for idx,file in enumerate(files, start=0):
            class_names = list(string.ascii_lowercase)
            class_names = np.array(class_names)
            mlflow_uri="http://mini7-mlflow.carpediem.so/"
            mlflow.set_tracking_uri(mlflow_uri)
            model_uri = "models:/Sign_Signal/production"
            model = mlflow.keras.load_model(model_uri)
            result = Result()
            result.image = file
            result.pub_date = timezone.datetime.now()
            result.save()
            img = cv2.imread(result.image.path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                print('Image not loaded')
                continue
            if img.size == 0:
                print('Image is empty')
                continue
            img = cv2.resize(img, (28, 28))
            test_sign_tmp = img.reshape(1, 28, 28, 1)
            test_sign = test_sign_tmp / 255.
            pred = model.predict(test_sign)
            pred_1 = pred.argmax(axis=1)
            result_str = class_names[pred_1][0]
            result.result = result_str
            result.save()
            results.append(result)
            chatGptPrompt += result.result
        chatResult = ChatResult()
        chatResult.prompt = chatGptPrompt
        chatResult.pub_date = timezone.datetime.now()
        chatResult.save()
        selectedChatResult = ChatResult.objects.get(id=chatResult.id)
        content = chatGPT(selectedChatResult.prompt)
        selectedChatResult.content = content
        selectedChatResult.save()
        context = {
            'question': selectedChatResult.prompt,
            'result': selectedChatResult.content,
            'image_url': results[0].image.url if results else None
        }
    return render(request, 'languagechat/result.html', context)
