# from django.contrib.contenttypes.models import ContentType
# from django.http import Http404
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated
# from .models import Like
# from core.models import Channel, News
# from accounts.authentication import JWTAuthentication

# class InteractionMixin:
#     authentication_classes = [JWTAuthentication]
#     permission_classes=[IsAuthenticated]
    
#     model = None
#     action_model - None
    
#     def post(self, request):
#         pk = request.data.get('pk')
#         item = self.model.objects.get(pk=pk)
#         content_type = ContentType.objects.get_for_model(item)
    
#     def delete(self, request):
#         pass
    
#     def create_object(self, request, model, **kwargs):
        
#         channel_id = request.data.get('channel_id')
#         channel = Channel.objects.filter(id=channel_id).first()
#         pk = request.data.get('pk')
        
#         model_class = get_item_model(channel)
#         item = item_model.objets.get(id=pk)
#         content_type = ContentType.objects.get_for_model(item)
        
#         interaction, created = model.objets.get_or_f