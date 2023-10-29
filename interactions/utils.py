from rest_framework import status

# from interactions.models import Recommendation

# def recomendation_counter(user, categories, flag=False):
#     for category in categories:
#         recommendation_obj, created = Recommendation.objects.get_or_create(user=user, category=category)
#         if flag:
#             recommendation_obj.count += 1
#         else:
#             recommendation_obj.count -= 1

#         recommendation_obj.save()
