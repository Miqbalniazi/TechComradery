from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from .models import AskingQuestion, UserResponse, MasterQuestion, BusinessRequirementDocument
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from techcomradery_client.models import SocialMediaUser
import openai, os
from .encryption_key import decrypt


SAVE_PATH = f"techcomradery_chatbot{os.sep}templates{os.sep}"
openai.api_key = decrypt("xp2hNgl[MsKTt[Z9xs>o<77Y8GqgpKOj5g8yo6gIwyP[P8<{x6<")

TOP_HTML = """
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
  <script>
    mermaid.initialize({ startOnLoad: true });
  </script>
</head>
<body>
"""

BOTTOM_HTML = """
</body>
</html>
"""


def get_mermaid_html(text):
    return TOP_HTML + """<div class="mermaid">""" + text + """\n</div>""" + BOTTOM_HTML


def home(request):
    print("USER IN HOME", request.user)
    asking_questions = AskingQuestion.objects.all()
    user_responses = UserResponse.objects.all()
    for question in asking_questions:
        print("QUESTION", question)
    
    for response in user_responses:
        print("RESPONSE", response)
    
    context = {
        'user': request.user,
    }
    
    return render(request, "chatbot.html")


def login(request):
    if request.method == "POST":
        # email = request.POST['email']
        # password = request.POST['password']
        user = authenticate(request, username="test@test.com", password="1234")
        if user is not None:
            auth_login(request, user)
            return redirect("home/")
        
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, "login.html")


@csrf_exempt
def get_response(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        event_question = data['event_question']
        media_user = SocialMediaUser.objects.get(id=data['user_id'])
        print("QUESTION", event_question)

        user_responses = UserResponse.objects.all().filter(social_media_user=media_user)
        # print(len(user_responses))
        if len(user_responses) == 0:
            question_number = 1
        
        else:
            # question number will come from the session of the user
            last_user_response = UserResponse.objects.all().filter(social_media_user=media_user).order_by('date_time')[0]
            if len(user_responses) > 0:
                questions = AskingQuestion.objects.all()
                for question in questions:
                    if question.asking_question == last_user_response.question:
                        question_number = question.id + 1
                    
                    else:
                        question_number = 1
            
            else:
                question_number = 1

            # question_number = int(data['question_number'])
        
        print("QUESTION NUMBER", question_number)

        # question = AskingQuestion.objects.get(id=question_number)
        question = MasterQuestion.objects.get(named_id=10)


        # send 5 random question as hints/examples

    return JsonResponse({
        # 'user': user.first_name,
        'question_number': 13,
        'question': question.question
    })


@csrf_exempt
def save_response(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        event_question = data['event_question']
        event_answer = data['event_answer']
        user_id = data['user_id']
        brd_id = data['brd_id']

        brd = BusinessRequirementDocument.objects.get(id=brd_id)
        question = AskingQuestion.objects.get(asking_question=event_question)
        media_user = SocialMediaUser.objects.get(id=user_id)

        user_response = UserResponse.objects.create(social_media_user=media_user, brd_id=brd, question=question, answer=event_answer, rectify_answer="")
        # print("USER RESPONSE", user_response.question)
        # print("USER RESPONSE", user_response.answer)
        # print("USER RESPONSE", user_response.id)

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt="draw a workflow diagram in mermaid from the following text:" + event_answer,
            temperature=0.7,
            max_tokens=1000,
            n=1,
            stop=None,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        choices = response.choices
        ai_output = choices[0].text

        ai_output = ai_output.replace("```mermaid", "")
        complete_html = get_mermaid_html(ai_output)
        file_name = f"{SAVE_PATH}diagram_{user_id}.html"

        with open(file_name, 'w') as f:
            f.write(complete_html)
        
        return JsonResponse({
            "file": "created",
            "status": 200
        })


def display(request, user_id):
    file_name = f"diagram_{user_id}.html"
    return render(request, file_name)
