import json

from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Area, Post
from user.models import Token, User


def create_area(request): # 지역 생성
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        if name:
            area = Area.objects.create(name=name)
            return JsonResponse({'message': '지역이 성공적으로 생성되었습니다.', 'name': area.name})
        else:
            return JsonResponse({'message': '이름을 입력해주세요.'}, status=400)


def delete_area(request, pk): # 지역 삭제
    area = get_object_or_404(Area, pk=pk)

    if request.method == 'DELETE':
        area_name = area.name
        area.delete()
        return JsonResponse({'message': '지역이 성공적으로 삭제되었습니다.', 'name': area_name})

    return JsonResponse({'message': 'POST 요청이 아닙니다.'}, status=400)



# def create_post(request):
#     if request.method == 'POST':
#         title = request.POST.get('title')
#         content = request.POST.get('content')
#         point = request.POST.get('point')
#     return JsonResponse({'message': '작성 성공'})
def create_post(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title')
        content = data.get('content')
        point = data.get('point')
        area = data.get('area')
        area = Area.objects.get(name=area)
        token = data.get('token')
        token = Token.objects.get(token=token)
        user= User.objects.get(id=token.email_id)
        post = Post(
            title=title,
            content=content,
            point=point,
            numChat=0,
            user=user,
            area=area
        )
        post.full_clean()  # 데이터 유효성 검사 실행
        post.save()
    return JsonResponse({'message': '작성 성공'})

def post_list(request):
    if request.method == "POST":
        data = json.loads(request.body)
        #data = request.POST
        area_name = data.get('area')
        try:
            area = Area.objects.get(name=area_name)
            posts = Post.objects.filter(area=area).order_by('-created_at')


            post_list = []
            for post in posts:
                post_data = {
                    "pk": post.pk,
                    "fields": {
                        "title": post.title,
                        "content": post.content,
                        "created_at": post.created_at,
                        "point": post.point,
                        "user": post.user.nickname,  # Assuming user has a 'nickname' field
                        "area": post.area.name,       # Assuming area has a 'name' field
                        "numChat": post.numChat,
                        "declare": post.declare,
                        "userId" : post.user_id
                    }
                }
                post_list.append(post_data)

            return JsonResponse({"posts": post_list}, safe=False)
        except Area.DoesNotExist:
            return JsonResponse({"error": "Area not found"}, status=404)

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'DELETE':
        post.delete()
        return JsonResponse({'message': '게시물이 성공적으로 삭제되었습니다.'})

def post_detail(request, pk):
    post = Post.objects.get(id=pk)

    # post.save()
    context = {
        "id" : post.pk,
        "title" : post.title,
        "content" : post.content,
        "numChat" : post.numChat,
        "point" : post.point,
        "created_at" : post.created_at,
        "area" : post.area.name
    }
    return JsonResponse(context)
    # post.objects.filter(id)


# 신고 올리기
def declare_post(request, pk):
    post = Post.objects.get(id=pk)
    post.declare += 1
    post.save()
    return JsonResponse({'message': '신고 횟수 +1 성공.'})


#채택하기

def update_post(request,pk):# 게시물 수정
    post = Post.objects.get(id=pk)
    if request.method == 'PUT':
        data = json.loads(request.body)
        print(data)
        title = data.get('title')
        content = data.get('content')
        point = data.get('point')
        post.title = title
        post.content = content
        post.point = point
        post.save()
    return JsonResponse({'message': '수정 성공'})



def my_post(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        token = data.get('token')
        token_obj = Token.objects.get(token=token)
        user = User.objects.get(id=token_obj.email_id)
        posts = Post.objects.filter(user=user)

        post_list = []
        for post in posts:
            post_data = {
                "pk": post.pk,
                "fields": {
                    "title": post.title,
                    "content": post.content,
                    "created_at": post.created_at,
                    "point": post.point,
                    "user": post.user.nickname,  # Assuming user has a 'nickname' field
                    "area": post.area.name,       # Assuming area has a 'name' field
                    "numChat": post.numChat,
                    "declare": post.declare,
                    "userid": post.user_id
                }
            }
            post_list.append(post_data)
        print(post_list)
        return JsonResponse(post_list, safe=False)

def get_areas(request):
    try:
        areas = Area.objects.all()
        areas_list = [{'id': area.id, 'name': area.name} for area in areas]
        return JsonResponse({'areas': areas_list})
    except Exception as e:
        return JsonResponse({'error': f'오류가 발생했습니다: {str(e)}'}, status=500)