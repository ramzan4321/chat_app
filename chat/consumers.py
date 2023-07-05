import json
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import ChatMessages
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		room = self.scope["url_route"]["kwargs"]["chat_box_name"]
		_list = room.split("_")
		if _list[0] != 'g':
			tem_list = sorted(_list, key=lambda x: x.lower())
			self.roomGroupName = tem_list[0]+"_"+tem_list[1]
			self.to = _list[1]
		else:
			self.roomGroupName = _list[1]
			self.to = 'group'

		await self.channel_layer.group_add(
			self.roomGroupName ,
			self.channel_name
		)
		await self.accept()
	async def disconnect(self , close_code):
		await self.channel_layer.group_discard(
			self.roomGroupName ,
			self.channel_layer
		)
	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json["message"]
		username = text_data_json["username"]
		await self.channel_layer.group_send(
			self.roomGroupName,{
				"type" : "sendMessage" ,
				"message" : message ,
				"username" : username ,
			})
	async def sendMessage(self , event) :
		message = event["message"]
		username = event["username"]
		await message_entry(username, self.to, message, self.roomGroupName)
		await self.send(text_data = json.dumps({"message":message ,"username":username}))
		
@database_sync_to_async
def message_entry(username, to, message, group_name):
	user = User.objects.filter(username=username).first()
	entry = ChatMessages(user=user, to=to, message=message, group_name=group_name)
	entry.save()
