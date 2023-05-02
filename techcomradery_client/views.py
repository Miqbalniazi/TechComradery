from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import SocialMediaUser, SubscriptionUser
from django.db.utils import IntegrityError


METHOD_NOT_ALLOWED = JsonResponse(
    {"status": 405, "message": "HTTP method not allowed"})
USER_EXISTS = JsonResponse(
    {"status": 200, "message": "Email already exists", "exists": True})
USER_NOT_EXISTS = JsonResponse(
    {"status": 200, "message": "Email not exists", "exists": False})


def user_exists(email):
    if User.objects.filter(email=email).exists():
        return True
    else:
        return False


@csrf_exempt
def is_user_exists(request):
    if request.method == "POST":
        try:
            email = request.POST['email']
            res = user_exists(email)

        except BaseException as e:
            return JsonResponse({
                "status": 400,
                "message": f'{str(e)} is required',
            })

        if res:
            return USER_EXISTS

        else:
            return USER_NOT_EXISTS

    else:
        return METHOD_NOT_ALLOWED


def get_pwd_or_social_id(request):
    social = request.POST['social']
    social_id = request.POST['social_id']
    image_url = request.POST['imageUrl']
    password = request.POST['password']
    # print(social, social_id, image_url, password, type(password))

    # todo: change to bool when getting from FEND
    if password == "None":
        return ["social", social, social_id, image_url, ""]

    else:
        return ["techcomradery", "", "", "", password]


@csrf_exempt
def register(request):
    if request.method == "POST":
        try:
            email = request.POST['email']
            res = user_exists(email)

        except BaseException as e:
            return JsonResponse({
                "status": 400,
                "message": f'{str(e)} is required',
            })

        if res:
            return USER_EXISTS

        else:
            try:
                email = request.POST['email']
                first_name = request.POST['givenName']
                last_name = request.POST['familyName']
                result = get_pwd_or_social_id(request)

            except BaseException as e:
                return JsonResponse({
                    "status": 400,
                    "message": f'{str(e)} is required',
                })

            user = User.objects.create(email=email, username=email)
            user.first_name = first_name
            user.last_name = last_name

            if result[0] == "social":
                SocialMediaUser.objects.create(
                    user=user,
                    social_media=result[1],
                    social_media_id=result[2],
                    image_url=result[3]
                ).save()

            else:
                user.set_password(result[4])
                SocialMediaUser.objects.create(
                    user=user,
                    social_media=result[0]
                ).save()

            user.save()
            return JsonResponse({
                'status': 200,
                'message': f'user created {user.first_name} {user.last_name}',
                'created': True
            })

    else:
        return METHOD_NOT_ALLOWED


@csrf_exempt
def subscribe(request):
    if request.method == "POST":
        try:
            name = request.POST['name']
            email = request.POST['email']
            whatsapp = request.POST['whatsapp']
            linkedin = request.POST['linkedin']
            provides = request.POST['provides']
            referred_by = request.POST['referred_by']
            email_sent = request.POST['email_sent']

        except BaseException as e:
            return JsonResponse({
                "status": 400,
                "message": f'{str(e)} is required',
            })
        
        try:
            sub_user = SubscriptionUser.objects.create(
                name=name,
                email=email,
                whatsapp=whatsapp,
                linkedin=linkedin,
                providing=provides,
                referred_by=referred_by,
                email_sent=email_sent
            )
            # sub_user.save()

            return JsonResponse({
                "status": 200,
                'message': f'user created',
                'referral': sub_user.referral,
            })
        
        except IntegrityError as e:
            return JsonResponse({
                "status": 404,
                "message": "Email is already subscribed.",
                "error": f"{e}",
            })
    
    else:
        return METHOD_NOT_ALLOWED