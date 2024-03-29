from django.shortcuts import render
from .models import CoffeeCafe, Review, ReviewImage
from rest_framework.decorators import api_view, permission_classes
from .serializers import CoffeeCafeSerializer, ReviewSerializer, ReviewImageSerializer, CoffeeCafeImageSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.db.models import Max

# Create your views here.
# @api_view(['GET'])
# @permission_classes([AllowAny])

# Coffeecafe Get
def get_coffeecafes(request, type):
    coffeecafes = CoffeeCafe.objects.all()
    # if type == 1: # Stars
    #     coffeecafes = CoffeeCafe.objects.order_by('-total_score')[:10]
    # elif type == 2: # Options
    #     pass
    # elif type == 3: # New
    #     coffeecafes = CoffeeCafe.objects[-1:-10:-1]
    if request.method == 'GET':
        serializer_coffeecafes = CoffeeCafeSerializer(coffeecafes, many = True)
        return JsonResponse(serializer_coffeecafes.data, safe=False)

# Coffeecafe Detail
def get_coffeecafes_detail(request, id):
    coffecafe_detail = CoffeeCafe.objects.get(id = id)
    if request.method == 'GET':
        serializer_coffeecafe_detail = CoffeeCafeSerializer(coffecafe_detail)
        return JsonResponse(serializer_coffeecafe_detail.data, safe=False)

# Coffeecafe Create
def create_coffeecafe(request):
    if request.method == 'POST':
        # coffee_cafe_cnt = CoffeeCafe.objects.aggregate(Max('id'))['id__max']

        data = request.POST.copy()
        # if coffee_cafe_cnt:
            # data['id'] = coffee_cafe_cnt + 1
        # else:
            # data['id'] = 1
        serializer_coffeecafe = CoffeeCafeSerializer(data=data)
        images = request.FILES.getlist('image')
        
        if serializer_coffeecafe.is_valid():
            coffeecafe = serializer_coffeecafe.save()
        
            for i, image in enumerate(images): 
                # cafe : id -> 필수
                coffeecafe_images = {'cafe': coffeecafe.id, 'image' : image}
                serializer_coffeecafe_image = CoffeeCafeImageSerializer(data = coffeecafe_images)
                if serializer_coffeecafe_image.is_valid():
                    serializer_coffeecafe_image.save()
        else:
            print(serializer_coffeecafe.errors)

    return JsonResponse(serializer_coffeecafe.data, safe=False)

# Review All
def get_review_all(request):
    review = Review.objects.all()
    if request.method == 'GET':
        serializer_review = ReviewSerializer(review)
        return JsonResponse(serializer_review.data, safe=False)

# Review Get
def get_review(request, id):
    review = Review.objects.get(id=id)
    if request.method == 'GET':
        serializer_review = ReviewSerializer(review)
        return JsonResponse(serializer_review.data, safe=False)

# Review Create, Update
def post_coffeecafe_detail_review(request, id, type):
    # id : cafe.id
    # type : id → update / 0 → create

    if request.method == 'POST':
        # review_cnt = Review.objects.aggregate(Max('id'))['id__max']

        # if review_cnt == None:
            # review_cnt = 0
        
        data = request.POST.copy() 
        data['cafe'] = id
        # data['score'] = float(data['score'])
        # data['type'] = int(data['type'])
        # data['user'] = int(data['user'])
  
        if type == 0:  
            
            # data['id'] = review_cnt + 1

            # total_score Algoritm
            # coffee_cafe : id에 대응하는 Cafe -> total_scroe
            # review_set : id에 대응하는 review -> 리뷰의 길이
            coffee_cafe = CoffeeCafe.objects.get(id=id)
            review_set = Review.objects.filter(cafe_id=id)
            # 1. total_score = 기존의 total_score * 리뷰의 길이 + 입력 받은 점수
            total_score = float(coffee_cafe.total_score) * len(review_set) + float(data['score'])
            # 2. total_score = 1에서 계산한 total_score / 리뷰의 길이  + 1
            coffee_cafe.total_score = round(total_score / (len(review_set)+1), 2) 
            coffee_cafe.save()
            
            update_cafe_score(coffee_cafe, id, data)

            # if data['type'] == "1":
            #     vibe_set = Review.objects.filter(cafe_id=id, type=1)
            #     vibe_score = float(coffee_cafe.vibe) * len(vibe_set) + float(data['score'])
            #     coffee_cafe.vibe = round(vibe_score / (len(vibe_set)+1), 2)
            #     coffee_cafe.save()
            # elif data['type'] == "2":
            #     seat_set = Review.objects.filter(cafe_id=id, type=2)
            #     seat_score = float(coffee_cafe.seat) * len(seat_set) + float(data['score'])
            #     coffee_cafe.seat = round(seat_score / (len(seat_set)+1), 2)
            #     coffee_cafe.save()
            # elif data['type'] == "3":
            #     coffee_set = Review.objects.filter(cafe_id=id, type=3)
            #     coffee_score = float(coffee_cafe.coffee) * len(coffee_set) + float(data['score'])
            #     coffee_cafe.coffee = round(coffee_score / (len(coffee_set)+1), 2)
            #     coffee_cafe.save()
            # elif data['type'] == "4":
            #     plug_set = Review.objects.filter(cafe_id=id, type=4)
            #     plug_score = float(coffee_cafe.plug) * len(plug_set) + float(data['score'])
            #     coffee_cafe.plug = round(plug_score / (len(plug_set)+1), 2)
            #     coffee_cafe.save()
            #
                
            serializer_coffeecafe_detail_reivew = ReviewSerializer(data=data)
        else:
            existing_review = Review.objects.filter(id=type).first()
            serializer_coffeecafe_detail_reivew = ReviewSerializer(existing_review, data=data, partial=True)
        

        images = request.FILES.getlist('image')
        if serializer_coffeecafe_detail_reivew.is_valid():
            review = serializer_coffeecafe_detail_reivew.save()
            for i, image in enumerate(images):
                 review_image_data = {'review': review.id, 'image' : image}
                 serializer_review_image = ReviewImageSerializer(data=review_image_data)
                 if serializer_review_image.is_valid():
                    serializer_review_image.save()
        else:
            print(serializer_coffeecafe_detail_reivew.errors)
        return JsonResponse(serializer_coffeecafe_detail_reivew.data, safe=False)

# Review Delete
def delete_review(request, id):
    if request.method == 'DELETE':

        # total_score Algo
        # review : 해당 리뷰
        review = Review.objects.get(id=id)
        # review_set : 해당 리뷰와 같은 카페들의 리뷰들
        review_set = Review.objects.filter(cafe_id=review.cafe_id)
        # coffee_cafe : 해당 리뷰의 카페의 정보
        coffee_cafe = CoffeeCafe.objects.get(id=review.cafe_id)
        total_score = float(coffee_cafe.total_score) * (len(review_set)) - float(review.score)
        
        if (len(review_set)-1):
            coffee_cafe.total_score = round(total_score / (len(review_set)-1), 2) 
        else:
            coffee_cafe.total_score = 0

        coffee_cafe.save()

        review_type = review.type
        print(review_type)
        if review_type == 1:
            field_name = "vibe"
        elif review_type == 2:
            field_name = "seat"
        elif review_type == 3:
            field_name = "coffee"
        elif review_type == 4:
            field_name = "plug"

        review_set = review_set.filter(type=review_type)
        score = getattr(coffee_cafe, field_name)
        new_score = float(score) * len(review_set) - float(review.score)
        if (len(review_set)-1):
            setattr(coffee_cafe, field_name, round(new_score / (len(review_set)-1), 2))
        else:
            setattr(coffee_cafe, field_name, 0)
        coffee_cafe.save()

        # if review_type == "1":
        #     vibe_set = Review.objects.filter(cafe_id=review.cafe_id, type=1)
        #     vibe_score = float(coffee_cafe.vibe) * len(vibe_set) - float(review.score)
        #     if (len(vibe_set)-1):
        #         coffee_cafe.vibe = round(vibe_score / (len(vibe_set)-1), 2)
        #     else:
        #         coffee_cafe.vibe = 0
        #     coffee_cafe.save()

        # elif review_type == "2":
        #     seat_set = Review.objects.filter(cafe_id=review.cafe_id, type=2)
        #     seat_score = float(coffee_cafe.seat) * len(seat_set) - float(review.score)
        #     if (len(seat_set)-1):
        #         coffee_cafe.seat = round(seat_score / (len(seat_set)-1), 2)
        #     else:
        #         coffee_cafe.seat = 0
        #     coffee_cafe.save()

        # elif review_type == "3":
        #     coffee_set = Review.objects.filter(cafe_id=review.cafe_id, type=3)
        #     coffee_score = float(coffee_cafe.coffee) * len(coffee_set) - float(review.score)
        #     if (len(coffee_set)-1):
        #         coffee_cafe.coffee = round(coffee_score / (len(coffee_set)-1), 2)
        #     else:
        #         coffee_cafe.coffee = 0
        #     coffee_cafe.save()
        # elif review_type == "4":
        #     plug_set = Review.objects.filter(cafe_id=review.cafe_id, type=4)
        #     plug_score = float(coffee_cafe.plug) * len(plug_set) - float(review.score)
        #     if (len(plug_set)-1):
        #         coffee_cafe.plug = round(plug_score / (len(plug_set)-1), 2)
        #     else:
        #         coffee_cafe.plug = 0
        #     coffee_cafe.save()
        #
            
        review.delete()
    return JsonResponse("Review Deleted", safe=False)

# Review Image Delete
def delete_review_image(request, id):
    if request.method == 'DELETE':
        review_image = ReviewImage.objects.get(id=id)
        review_image.delete()
    return JsonResponse("Review Image Deleted", safe=False)



# Function

def update_cafe_score(coffee_cafe,id, data):
 
    if data['type'] == "1":
        field_name = 'vibe'
    elif data['type'] == "2":
        field_name = 'seat'
    elif data['type'] == "3":
        field_name = 'coffee'
    elif data['type'] == "4":
        field_name = 'plug'
    else:
        return

    review_set = Review.objects.filter(cafe_id=id, type=data['type'])
    # getattr(object, attribute_name) : Object의 Attribute를 호출
    score = getattr(coffee_cafe, field_name)
    new_score = (float(score) * len(review_set) + float(data['score'])) / (len(review_set) + 1)
    # setattr(object, attribute_name, value) : Object에 Attribute에 Value를 추가
    setattr(coffee_cafe, field_name, round(new_score, 2))
    coffee_cafe.save()