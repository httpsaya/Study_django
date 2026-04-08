import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from apps.integers.models import Comments


class WSConsumer(AsyncWebsocketConsumer):


    async def connect(self):

        self.video_id = self.scope["url_route"]["kwargs"]["video_id"]
        self.comment_group_name = f'video_{self.video_id}'

        await self.channel_layer.group_add(
            self.comment_group_name,
            self.channel_name,
        )

        await self.accept()

        old_comments = await self.get_comments()
        for comment in old_comments:
            await self.send(text_data=json.dumps({
                'message': comment['message'],
                'username': comment['user'],
            }))
    

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.comment_group_name,
            self.channel_name
        )

    
    async def receive(self, text_data=None, bytes_data=None):

        data = json.loads(text_data)
        message = data['message']
        username = data['username']

        await self.save_comment(username, message)

        await self.channel_layer.group_send(
            self.comment_group_name,
            {
                'type': 'new_comment',
                'message': message,
                'username': username
            }
        )


    async def new_comment(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))
    
    
    @sync_to_async
    def get_comments(self):
        return list(
            Comments.objects.filter(video_id=self.video_id)
            .order_by('sent_at')
            .values('user', 'message')
        )
    
    
    @sync_to_async
    def save_comment(self, username, message):
        Comments.objects.create(
            user=username,
            message=message,
            video_id=self.video_id
        )