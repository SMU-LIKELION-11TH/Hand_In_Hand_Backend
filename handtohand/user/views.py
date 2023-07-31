from datetime import datetime

from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.views.decorators.csrf import csrf_exempt

from .decorators import email_verification_required
from .models import User, EmailVerification
from post.models import Area

from .utils import send_verification_email


def verify_email(request):
    token = request.GET.get('token')

    try:
        email_verification = EmailVerification.objects.get(token=token)
        email_verification.is_verified = True
        email_verification.save()

        return HttpResponse("인증확인되었습니다.")

    except EmailVerification.DoesNotExist:
        return HttpResponse("유효하지 않은 인증 토큰입니다.")


@csrf_exempt
@email_verification_required
def user_signup(request):
    timezone.deactivate()
    if request.method == 'POST':
        try:
            data = request.POST  # 클라이언트에서 전달된 데이터를 받아옵니다.

            # 데이터 유효성 검사
            name = data.get('name')
            email = data.get('email')
            password = data.get('password')
            nickname = data.get('nickname')
            date_of_birth_str = data.get('date_of_birth')
            address = data.get('address')
            area = data.get('area')

            if not all([name, email, password, nickname, date_of_birth_str, address]):
                return JsonResponse({"message": "누락된 필수 데이터가 있습니다."}, status=400)

            date_of_birth = parse_date(date_of_birth_str)

            if len(date_of_birth_str) == 6 and date_of_birth_str.isdigit():
                date_of_birth = datetime.strptime(date_of_birth_str, "%y%m%d")

            area = Area.objects.get(name=area)
            # User 객체 생성
            user = User(
                name=name,
                email=email,
                password=password,
                nickname=nickname,
                date_of_birth=date_of_birth,
                address=address,
                point=1000,
                area=area
            )
            user.full_clean()  # 데이터 유효성 검사 실행
            user.save()

            email_verification = EmailVerification.objects.create(user=user)
            send_verification_email(user, email_verification)

            return JsonResponse({"message": "회원가입에 성공하였습니다."}, status=201)
        except ValidationError as e:
            return JsonResponse({"message": str(e)}, status=400)
        except Exception as e:
            print(e)
            return JsonResponse({"message": "서버 오류가 발생했습니다."}, status=500)
    else:
        return JsonResponse({"message": "잘못된 요청입니다."}, status=400)





