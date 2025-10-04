from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class UserMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        messages = request.user.messages.all()  # Assuming a related_name='messages' on your Message model
        return Response({"messages": [msg.content for msg in messages]})