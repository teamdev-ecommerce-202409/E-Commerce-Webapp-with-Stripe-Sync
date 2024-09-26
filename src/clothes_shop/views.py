from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from clothes_shop.models import Clothes
from clothes_shop.serializers import ClothesSerializer


@api_view(["GET", "POST"])
def clothes_list(request):
    """
    List all clothes, or create a cloth.
    """
    if request.method == "GET":
        clothes = Clothes.objects.all()
        serializer = ClothesSerializer(clothes, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = ClothesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT", "DELETE"])
def clothes_detail(request, pk):
    """
    Update or delete a cloth.
    """
    try:
        cloth = Clothes.objects.get(pk=pk)
    except Clothes.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        serializer = ClothesSerializer(cloth, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        cloth.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
