import os
from .serializers import *
from .models import *
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.db.models import Q, Count
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

# Create your views here.
class AddPosts(ViewSet,PageNumberPagination):

    def list(self,request):
        data = SocailPosts.objects.all().values()
        data = self.paginate_queryset(data, request, view=self)
        return self.get_paginated_response (data)

    def create (self,request):
        #creating the  parent post 
        if request.user.is_admin:
            pk = request.user.pk  
            SocailPosts.objects.create(post_title = request.data['title'],user = User.objects.get(id=pk))
            last_post_id=SocailPosts.objects.filter(user_id=pk).order_by('-id').values('id')[0]['id']

            #saving the images with parent id
            allfiles= request.FILES
            count = 0
            object_list=[]
            last_post_id = SocailPosts.objects.get(id=last_post_id)

            for i in allfiles:

                count+=1

                myfile = request.FILES[i]
                file_name = default_storage.save(myfile.name,myfile)

                file_url = default_storage.url(file_name)
                file_url = (os.path.dirname(os.path.dirname(__file__))+file_url)
            
                object_list.append(Images(image = file_url,
                                                description=request.data['description'+ str(count)],
                                                tags = request.data['tag'+ str(count)],
                                                post = last_post_id ))

            Images.objects.bulk_create(object_list)
                
            return Response({"meesage":"Images uploaded sucessfully"},status=status.HTTP_201_CREATED)
        return Response({"message":"Unauthorized access"})


class LikeDislikePosts(ViewSet):
 
    def create (self,request):
        #creating the  parent post    
        pk = request.user.pk  
        user = User.objects.get(id=pk)

        try:
            post_id=SocailPosts.objects.get(id=request.data['post_id'])
        except:
            return Response("Invalid")
    

        data = LikeDislike.objects.filter(user= user,post = post_id).all()
        if len(data)>0:
    
            if request.data['is_liked']=="true" or request.data['is_liked']=="True":
                print("ok")
                data.update(like= True,user= user,post = post_id)
                return Response({"meesage":"Liked"},status=status.HTTP_201_CREATED)
            else:
                data.update(like= False,user= user,post = post_id)
                return Response({"meesage":"Disliked"},status=status.HTTP_201_CREATED)
        else:
            if request.data['is_liked']=="true" or request.data['is_liked']=="True":
             
                LikeDislike.objects.create(like= True,user= user,post = post_id)
                return Response({"meesage":"Liked"},status=status.HTTP_201_CREATED)
            else:
                LikeDislike.objects.create(like= False,user= user,post = post_id)
            return Response({"meesage":"Disliked"},status=status.HTTP_201_CREATED)
     
class GetPosts(ViewSet,PageNumberPagination):
    
    def list(self,request):
        
        data = SocailPosts.objects.all().values().annotate(total_likes = Count('likedislike', filter=Q(likedislike__like=True)),
                                                              total_dislikes =  Count('likedislike', filter=Q(likedislike__like=False)),)
        for i in data:    
            try:
                i['current_user_like_status']= LikeDislike.objects.filter(post = i['id'],user = request.user.pk).values()[0]['like']
             
            except:
                i['current_user_like_status']=""

            i['post_details']= Images.objects.filter(post_id = i['id']).values()
        
        data = self.paginate_queryset(data, request, view=self)
        return self.get_paginated_response (data)
            
       

    


class GetListOfLikedUsers(ViewSet,PageNumberPagination):
    def list(self,request):
        
        data = LikeDislike.objects.filter(like=True,post = request.query_params['id']).values('user','user__name','user__email')
        data = self.paginate_queryset(data, request, view=self)
        return self.get_paginated_response (data)



  