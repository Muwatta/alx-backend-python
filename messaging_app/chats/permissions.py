from rest_framework.permissions import BasePermission

class IsParticipantOfConversation(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow only authenticated users
        if not request.user.is_authenticated:
            return False
        # Check if user is a participant in the conversation
        return obj.participants.filter(id=request.user.id).exists()