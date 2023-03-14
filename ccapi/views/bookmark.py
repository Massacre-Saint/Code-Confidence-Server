"""Module sets up Djnago Viewset for the class of Bookmark"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from ccapi.models import Bookmark, User
from django.db import IntegrityError

class BookmarkView(ViewSet):
    """Class creates the viewset for Bookmark class"""
    def list(self, request):
        """Get method get list of all Bookmark instances"""
        bookmarks = Bookmark.objects.all()
        serializer = BookmarkSerilaizer(bookmarks, many=True)

        return Response(serializer.data)

    def create(self, request):
        """Post method creates one or more bookmarks from JSON data"""
        body = request.data
        bookmarks = Bookmark.objects.all()
        try:
            if (body['title'] == 'Code Confidence Resources'):
                create_bookmark_from_json(body)
                parent_bookmarks = bookmarks.filter(id=body['parentId'])
                if len(parent_bookmarks) == 0:
                    return Response({'error': 'Parent bookmark does not exist'}, status=status.HTTP_404_NOT_FOUND)
            bookmark = create_bookmark_from_json(body)
            serializer = BookmarkSerilaizer(bookmark)

            return Response(serializer.data)

        except IntegrityError:
            # If a UNIQUE constraint error occurs, return a 409 Conflict response
            return Response({'error': 'Bookmark with this id already exists'}, status=status.HTTP_409_CONFLICT)

    def update(self, request, pk):
        """Put method updates instance of bookmark"""
        body = request.data
        bookmark = Bookmark.objects.get(pk=pk)
        bookmark.index = body['index']
        bookmark.parent_id = body['parent_id']
        bookmark.title = body['title']
        if 'url' in body:
            bookmark.url = body['url']
        bookmark.save()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Delete method deletes the instance and children of pk"""
        bookmark = Bookmark.objects.get(pk=pk)
        bookmarks = Bookmark.objects.all()
        if bookmark.title == 'Code Confidence Resources':
            bookmarks.delete()
        try:
            for index in bookmarks:
                if bookmark.id == index.parent_id:
                    index.delete()
        except:
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        bookmark.delete()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class BookmarkSerilaizer(serializers.ModelSerializer):
    """Class creates the serializer for BookMark class"""
    class Meta:
        depth = 1
        model = Bookmark
        fields = (
          'id',
          'index',
          'parent_id',
          'title',
          'url',
        )

def create_bookmark_from_json(json_data, parent_folder=None):
    # create or retrieve the parent bookmark
    bookmark, created = Bookmark.objects.get_or_create(
        id=int(json_data['id']),
        defaults={
            'index': json_data['index'],
            'parent_id': int(json_data['parentId']),
            'title': json_data['title'],
            'url': json_data.get('url', None),
        },
    )

    if not created:
        # if the bookmark already exists, update the non-unique fields
        bookmark.index = json_data['index']
        bookmark.parent_id = int(json_data['parentId'])
        bookmark.title = json_data['title']
        bookmark.url = json_data.get('url', None)
        bookmark.save()

    # recursively create child bookmarks
    if 'children' in json_data:
        for child_data in json_data['children']:
            create_bookmark_from_json(child_data)

    return bookmark
