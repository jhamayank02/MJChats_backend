from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Room
from .models import Message
from django.utils import timezone

# Create your views here.

# Function to check user credentials
@csrf_exempt
def chatCredentialsCheck(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)

        # Grab username, room_option, room_code, room_pass
        username = json_data['username']
        room_option = json_data['room_option']
        room_code = json_data['room_code']
        room_pass = json_data['room_pass']

        # If any field is blank return 400 response code
        if username == '' or room_option == '' or room_code == '' or room_pass == '':
            response = {"status": 400, "msg": "Blank fields are not allowed"}
            return JsonResponse(response)

        # If user wants to create a new room create it
        if room_option == '1':
            newRoom = Room(room_code=room_code,room_creator=username, room_pass=room_pass)
            newRoom.save()

            response = {"status": 200, "msg": "Room has been created successfully"}
            return JsonResponse(response)
        
        # If user has a room_code and password let him/her enter in the room
        if room_option == '2':
            room = Room.objects.filter(room_code=room_code).first()

            if room is not None:
                if room.room_pass == room_pass:
                    response = {"status": 200, "msg": "Successfully entered in the room"}
                    return JsonResponse(response)
                else:
                    response = {"status": 400, "msg": "Make sure you have entered the correct password"}
                    return JsonResponse(response)

            else:
                response = {"status": 400, "msg": "Room does not exist"}
                return JsonResponse(response)

    return HttpResponse(status=404)

# Fetch all the messages from a particular room_code
@csrf_exempt
def prevMsgs(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        room_code = json_data['room_code']

        allMsgs = Message.objects.filter(sent_to_room=room_code).values("sent_by","sent_on","msg")
        msgList = list(allMsgs)
        response = {"status": 200, "msgs": msgList}
        return JsonResponse(response)