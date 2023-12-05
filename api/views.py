from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Products,Carts,Reviews
from api.serializers import ProductSerializers,ProductModelSerializer,UserSerializer,CartSerializer,ReviewSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework import authentication,permissions




# Create your views here.
class productView(APIView):
    def get(self,request,*args,**kwargs):
        qs=Products.objects.all()
        serializer=ProductSerializers(qs,many=True)

        return Response(data=serializer.data)

    def post(self, request, *args, **kwargs):

        serializer=ProductSerializers(data=request.data)

        if serializer.is_valid():

            print(serializer.validated_data)
            Products.objects.create(**serializer.validated_data)
            return Response(data=serializer.data)
        else:

            return Response(data=serializer.errors)


class ProductDetailView(APIView):
    def get(self,request,*args,**kwargs):

        print(kwargs)
        id = kwargs.get("id")
        qs = Products.objects.get(id=id)
        serializer = ProductSerializers(qs,many=False)

        return Response(data=serializer.data)

    def put(self, *args, **kwargs):

        return Response(data='Updating a product')
    def delete(self,request,*args,**kwargs):

        id = kwargs.get('id')
        Products.objects.filter(id=id).delete()
        return Response(data='Object deleted')

# class ProductViewsetView(viewsets.ViewSet):
#
#     def list(self,request,*args,**kwargs):
#
#         qs = Products.objects.all()
#         serializer = ProductModelSerializer(qs,many=True)
#
#         return Response(data=serializer.data)
#
#     def create(self,request,*args,**kwargs):
#
#         serializer = ProductModelSerializer(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data)
#
#         else:
#             return Response(data=serializer.errors)
#
#     def retrieve(self,request,*args,**kwargs):
#
#         id = kwargs.get("pk")
#
#         qs = Products.objects.get(id=id)
#         serializer = ProductModelSerializer(qs,many=False)
#
#         return Response(data=serializer.data)
#
#
#
#     def destroy(self,request,*args,**kwargs):
#         id = kwargs.get("pk")
#         Products.objects.filter(id=id).delete()
#         return  Response(data="deleted")
#
#     def update(self,request,*args,**kwargs):
#         id = kwargs.get("pk")
#         obj = Products.objects.get(id=id)
#         serializer = ProductModelSerializer(data=request.data,instance=obj)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data)
#         else:
#             return Response(data=serializer.errors)
#     @action(methods=["GET"],detail=False)
#     def categories(self,request,*args,**kwargs):
#
#         res = Products.objects.values_list('category',flat=True).distinct()
#         return Response(data=res)
# class UserView(viewsets.ViewSet):
#     def create(self,request,*args,**kwargs):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data)
#         else:
#
#             return Response(data=serializer.errors)
class ProductModelViewsetView(viewsets.ModelViewSet):

    serializer_class = ProductModelSerializer
    queryset= Products.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=["GET"],detail=False)
    def categories(self,request,*args,**kwargs):
        res = Products.objects.values_list('category',flat=True).distinct()
        return Response(data=res)

    @action(methods=["POST"],detail=True)
    def addto_cart(self,request,*args,**kwargs):

        id = kwargs.get("pk")
        item = Products.objects.get(id=id)
        user = request.user
        user.carts_set.create(product=item)

        return Response(data="item added to cart")

    @action(methods=["POST"],detail=True)
    def add_review(self,request,*args,**kwargs):

        user = request.user
        id = kwargs.get("pk")
        object = Products.objects.get(id=id)
        serializer = ReviewSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(product=object,user=user)
            return Response(data=serializer.data)
        else:

            return Response(data=serializer.errors)

    @action(methods=["GET"],detail=True)
    def review(self,request,*args,**kwargs):

        # id = kwargs.get("pk")
        # product = Products.objects.get(id=id)
        product = self.get_object()

        qs = product.reviews_set.all()
        serializer = ReviewSerializer(qs,many=True)

        return Response(serializer.data)


        # qs = product.reviews_set.all()


class CartView(viewsets.ModelViewSet):

    serializer_class = CartSerializer
    queryset = Carts.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):

        #return self.requset.user.carts_set.all()
        return Carts.objects.filter(user=self.request.user)


    # def list(self,request,*args,**kwargs):
    #
    #     qs = request.user.carts_set.all()
    #     serializer = CartSerializer(qs,many=True)
    #     return Response(data=serializer.data)
# class UserView(viewsets.ModelViewSet):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()

class ReviewDeleteView(APIView):
    def delete(self,request,*args,**kwargs):

        id = kwargs.get('pk')
        Reviews.objects.filter(id=id).delete()
        return Response(data="Review Deleted")





class UserModelViewsetView(viewsets.ModelViewSet):

    serializer_class = UserSerializer
    queryset = User.objects.all()






















