from Movie.serializers import *
from rest_framework import status
from rest_framework import generics, mixins

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from Movie.user_permissions import IsUserPermission
from django.http import JsonResponse


# user register view
class RegisterApi(generics.GenericAPIView):
    # fetching serializer data
    serializer_class = UserSerializer
    # adding authentications & auth user with role
    authentication_classes = []

    # post method for user registration
    def post(self, request, *args, **kwargs):
        '''
        This function is used for post data into database of particuar model and
            method is POST this method is used for only post the data and this function
            contating serializer data fetching serializer data and register  user with details
        '''
        parameters = request.data.copy()
        serializer = self.get_serializer(data=parameters)
        # validating serializer
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"status":"sucess","Message": "User Created Successfully.  Now Perform Login To Get Your Token"},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({"Status": "Error","Message":'User Name Already Exist'}, status=status.HTTP_406_NOT_ACCEPTABLE)



class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    '''user login view'''

    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class UploadMoviesApiView(generics.ListCreateAPIView):
    serializer_class = MovieSerializers
    queryset = Movie.objects.all()
    permission_classes = [IsAuthenticated, IsUserPermission ]


class UploadCastApiView(generics.ListCreateAPIView):
    serializer_class = CastSerializers
    queryset = Cast.objects.all()
    permission_classes = [IsAuthenticated, IsUserPermission ]




@api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes([IsAuthenticated, IsUserPermission])
def Movies_detail(request, pk):
    '''
    This function is used for update team details of particular Movie and this
    function contain get, multimple get objects
    '''
    try:
        # get the model name with filtering team id
        tutorial = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return JsonResponse({"Status": "Error","Message": 'The Movie Does Not Exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # fetch serializer data and add model into serializer
        movie_serializer = MovieSerializers(tutorial)
        return JsonResponse(movie_serializer.data)
    return JsonResponse({"Status": "Error","Message": 'Data not available!'}, status=status.HTTP_404_NOT_FOUND)


class Cast_ListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsUserPermission]
    ## authentication token and permissions of user we can change permissions
    """
    book list api view user can see his books details only"""

    def get(self, request):
        try:
            # get the model data
            tutorial = Cast.objects.all()
        except Cast.DoesNotExist:
            return JsonResponse({"Status": "Error","Message": 'Cast Does Not Exist'}, status=status.HTTP_404_NOT_FOUND)

        cast_serializer = CastSerializers(tutorial, many=True)
        return JsonResponse(cast_serializer.data, safe=False)