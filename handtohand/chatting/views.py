import json

from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

from chatting.dto import *
from chatting.models import Room, Content
from post.models import Post
from user.models import User, Token

from user.models import Attendance


# from chatting.dto import main_dto, sub_dto


def delete_room(request, pk):
    if request.method == 'DELETE':
        try:
            room = Room.objects.get(id=pk)
            room.delete()
            return JsonResponse({"message": "삭제되었습니다."})

        except ObjectDoesNotExist:
            return JsonResponse({"error": "해당 방을 찾을 수 없습니다."}, status=404)

        except Exception as e:
            return JsonResponse({"error": f"오류가 발생했습니다: {str(e)}"}, status=500)

    return JsonResponse({"error": "DELETE 요청이 필요합니다."}, status=405)

# Create your views here.
def create_room(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            post_id = data.get("post_id")
            post = Post.objects.get(id=post_id)
            owner = post.user
            token = data.get("token")
            token = Token.objects.get(token=token)
            customer = User.objects.get(id=token.email_id)
            customer = customer
            room = Room(
                post=post,
                owner=owner,
                customer=customer
            )
            room.full_clean() #데이터 유효성 검사
            room.save()
            return JsonResponse({"result": "success"})
        except Exception as e:
            print(e)
            return JsonResponse({"result": "fail"})


def main_dto(pk):
    nested_json = {"main": []}
    user = User.objects.get(pk=pk)
    main_room = Room.objects.filter(owner=user)

    for m in main_room:
        chat = Content.objects.filter(
            Q(user=user, room=m.pk) | Q(user=m.customer, room=m.pk)
        )
        chat_data = []
        for c in chat.order_by('pk'):  # Order chat by pk
            chat_data.append({
                "pk": c.pk,
                "fields": {
                    "content": c.content,
                    "user": c.user.nickname,
                    "room": c.room.id
                }
            })
        main_content = {
            "owner" : m.owner.adopt_count,
            "custom" : m.customer.adopt_count,
            "customN" : m.customer.nickname,
            "ownerN" : m.owner.nickname,
            "point" : m.post.point,
            "room_id": m.pk,
            "title": m.post.title,
            "chat": chat_data,
            "post_id": m.post.pk,
        }
        nested_json["main"].append(main_content)

    return nested_json


def sub_dto(pk):
    nested_json = {"sub": []}
    user = User.objects.get(pk=pk)
    sub_room = Room.objects.filter(customer=user)

    for m in sub_room:
        chat = Content.objects.filter(
            Q(user=user, room=m.pk) | Q(user=m.customer, room=m.pk)
        )
        chat_data = []
        for c in chat.order_by('pk'):  # Order chat by pk
            chat_data.append({
                "pk": c.pk,
                "fields": {
                    "content": c.content,
                    "user": c.user.nickname,
                    "room": c.room.id
                }
            })
        sub_content = {
            "owner": m.owner.adopt_count,
            "custom": m.customer.adopt_count,
            "customN": m.customer.nickname,
            "ownerN": m.owner.nickname,
            "point": m.post.point,
            "room_id": m.pk,
            "title": m.post.title,
            "chat": chat_data,
            "post_id": m.post.pk
        }
        nested_json["sub"].append(sub_content)

    return nested_json


def show_chat(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_token = data.get("token")
        user = Token.objects.get(token=user_token)
        user_id = user.email_id
        user = User.objects.get(id=user_id)
        print(user_id)
        try:
            main = main_dto(user_id)
            sub = sub_dto(user_id)
            context = {
                "user": user.nickname,
                "main": main,
                "sub": sub
            }
            return JsonResponse(context)
        except Exception as e:
            print(e)
            return JsonResponse({"error": str(e)}, status=500)


def create_chat(request):
    if request.method == "POST":
        try:
            data = request.data
            content = data.get("content")
            user_token = data.get("token")
            token = Token.objects.get(token=user_token)
            user= User.objects.get(id=token.email_id)
            user_nickname = user.nickname
            room = data.get("room_id")
            room=Room.objects.get(id=room)

            content_obj = Content(
                content=content,
                user=user,
                room=room
            )
            content_obj.save()

            return JsonResponse({"message": "success"})
        except Exception as e:
            print(e)
            return JsonResponse({"message": "error", "error_details": str(e)})
    else:
        return JsonResponse({"message": "Invalid request method"})


def choice(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            room_id = data.get("room_id")
            room = Room.objects.get(id=room_id)
            user1 = User.objects.get(id=room.owner_id)
            user2 = User.objects.get(id=room.customer_id)
            post = Post.objects.get(id=room.post_id)
            user1.adopt_count = user1.adopt_count+1
            user1.point = user1.point+post.point
            user2.point = user2.point-post.point
            room.delete()
            user1.save()
            user2.save()

            return JsonResponse({"message": "처리되었습니다."})

        except json.JSONDecodeError:
            return JsonResponse({"error": "올바른 JSON 형식이 아닙니다."}, status=400)

        except ObjectDoesNotExist:
            return JsonResponse({"error": "해당 정보를 찾을 수 없습니다."}, status=404)

        except Exception as e:
            return JsonResponse({"error": f"오류가 발생했습니다: {str(e)}"}, status=500)

    return JsonResponse({"error": "POST 요청이 필요합니다."}, status=405)



