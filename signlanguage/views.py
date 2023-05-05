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

# from pybo.model import Result
from .models import Result

# Create your views here.

logger = logging.getLogger('mylogger')

def index(request):
    return render(request, 'language/index.html')

def upload(request):
    if request.method == 'POST' and request.FILES['files']:

        results=[]
        #form에서 전송한 파일을 획득한다.
        files = request.FILES.getlist('files')
        for idx,file in enumerate(files, start=0):
                # files:

            # logger.error('file', file)
            # class names 준비
            class_names = list(string.ascii_lowercase)
            class_names = np.array(class_names)


            # mlflow 로딩
            mlflow_uri="http://mlflow.carpediem.so/"
            mlflow.set_tracking_uri(mlflow_uri)
            model_uri = "models:/Sign_Signal/production"
            model = mlflow.keras.load_model(model_uri)

            answer_str = request.POST.getlist('answer')[idx]

            # history 저장을 위해 객체에 담아서 DB에 저장한다.
            # 이때 파일시스템에 저장도 된다.
            result = Result()
            result.answer = answer_str
            result.image = file
            result.pub_date = timezone.datetime.now()
            result.save()


            # 흑백으로 읽기
            img = cv2.imread(result.image.path, cv2.IMREAD_GRAYSCALE)

            # 크기 조정
            img = cv2.resize(img, (28, 28))

            # input shape 맞추기
            test_sign = img.reshape(1, 28, 28, 1)

            # 스케일링
            test_sign = test_sign / 255.

            # 예측 : 결국 이 결과를 얻기 위해 모든 것을 했다.
            pred = model.predict(test_sign)
            pred_1 = pred.argmax(axis=1)

            result_str = class_names[pred_1][0]

            if(result_str==answer_str) :
                is_correct = True
            else :
                is_correct = False

            #결과를 DB에 저장한다.
            result.result = result_str
            result.is_correct = is_correct
            result.save()
            results.append(result)



        context = {
            'results': results,
        }


    # http method의 GET은 처리하지 않는다. 사이트 테스트용으로 남겨둠
    else:
        test = request.GET['test']
        logger.error(('Something went wrong!!',test))

    return render(request, 'language/result.html', context)    

