from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.generics import CreateAPIView, ListAPIView
from .serializers import (
    UserSerializer,
    UserProfileSerializer,
    EventsSerializer,
    UserCreateSerializer,
    CreateEventSerializer,
    CreateConnectionSerializer,
    UploadImageSerializer,
    AdgendaSerializer,
    MarketPlaceSerializer,
    ImageSerializer
)
from myapp.form_serializsers import MarketPlacePictureForm
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import (UserProfile,
                     Event,
                     Adgenda,
                     Connection,
                     AdgendaInvites,
                     MarketPlace,
                     UploadIMG,
                     Connection,
                     MarketPlacePictures,
                     EventInvites)
import logging
from rest_framework.permissions import IsAuthenticated
from myapp import helper
import json
import os
import base64
from django.core.files.base import ContentFile
from myapp import constants, config
import datetime
from django.db import connection
# Create your views here.
UserModel = get_user_model()
logger = logging.getLogger(__name__)
# from rest_framework.permissions import IsAuthenticated


class UserList(ListAPIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = User.objects.all()
    serializer_class = UserSerializer

# class Users(ListAPIView):
#     permission_classes = (AllowAny,)
#     queryset = Connection.all()
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class Users(APIView):
    res = None

    def get(self, req):
        permission_classes = (AllowAny,)
        queryset = Connection.objects.all()
        qr = Q()
        q = User.objects
        try:
            for o in queryset:
                conId = o.id
                if o not in [None, '']:
                    qr = ~Q(pk=conId)
                    q = q.filter(qr)
                    ser = UserSerializer(
                        q, many=True, context={'request': req})
                    res = Response(ser.data)
                else:
                    res = Response({'no record': 0})
        except Exception as e:
            res = Response({'error': 1, 'message': str(e)})
        return res


class UserDetail(APIView):
    permission_classes = (AllowAny,)

    def get(self, req):
        res = None
        try:
            serializer = UserSerializer(req.user)
            res = Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            res = Response({'error': 1, 'message': str(e)},
                           status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return res

    def post(self, req):
        data = req.data
        dic = {
            'username': data['username'],
            'password': data['username']
        }
        print(dic['username'])
        return Response(1)


class CurrentUser(APIView):
    permission_classes = (AllowAny,)

    def get(self, req, id):
        res = None
        qr = Q()
        q = UserProfile.objects
        hasId = False
        try:
            if id not in [None, '']:
                hasId = True
            if hasId:
                qr = Q(user=id)
                q = q.filter(qr)
                ser = UserProfileSerializer(
                    q, many=True, context={'request': req})
                res = Response(ser.data)
            else:
                res = Response(
                    {'error': 1}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            res = Response({'error': 1, 'message': str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res

class GlobalEvents(APIView):
    res = None
    def get(self, req):
        try:
            queryset = Event.objects.all()
            ser = EventsSerializer(queryset, many=True, context={'request': req})
            res = Response(ser.data)
        except Exception as e:
            res = Response(2)
        return res

class Events(APIView):
    # permission_classes = (AllowAny,)
    # def get(self, req, id):
    #     res = None
    #     qr = Q()
    #     event_id = id
    #     q = Event.objects
    #     try:
    #         qr = Q(pk=event_id)
    #         q = q.filter(qr)
    #         ser = EventsSerializer(q, many=True, context={'request': req})
    #         res = Response(ser.data)
    #     except Exception as e:
    #         logger.exception(e)
    #         res = Response({'error': 1, 'message': str(e)},
    #                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #     return res
    # permission_classes = (AllowAny,)
    def get(self, req, id):
        res = None
        qr = Q()
        event_id = id
        q = Event.objects
        try:
            qr = Q(pk=event_id)
            q = q.filter(qr)
            ser = EventsSerializer(q, many=True, context={'request': req})
            res = Response(ser.data)
        except Exception as e:
            logger.exception(e)
            res = Response({'error': 1, 'message': str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res

    def delete(self, req, id):
        try:
            if id not in [None, '']:
                o = Event.objects.get(pk=id)
                o.delete()
            res = Response(1)
        except Exception as e:
            res = Response({'error': 1, 'message': str(e)})
        return res

    def post(self, req):
        try:
            dic = req.data
            obj = Event(
                event_name=dic['event_name'],
                selected_address=dic['selected_address'],
                location=dic['location'],
                category=dic['category'],
                about_event=dic['about_event'],
                start_time=dic['start_time'],
                start_date=dic['start_date'],
                end_time=dic['end_time'],
                end_date=dic['end_date'],
                created_by=req.user,
                user=req.user
            )
            obj.save()
            # uploadEventImage(req, obj.id)
            res = Response({'success': 1, 'id': obj.id},
                           status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception(e)
            res = Response({'error': 1, 'message': str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res

    def put(self, req, id):
        try:
            data = req.data
            o = Event.objects.get(pk=id)
            o.event_name = data['event_name']
            o.selected_address = data['selected_address']
            o.location = data['location']
            o.category = data['category']
            o.about_event = data['about_event']
            o.start_time = data['start_time']
            o.start_date = data['start_date']
            o.end_time = data['end_time']
            o.end_date = data['end_date']
            o.user = req.user
            o.save()
            res = Response({'success': 1})
        except Exception as e:
            res = Response({'error': 1, "message": str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res

class searchEvent(APIView):
    permission_classes = (AllowAny,)

    def get(self, req):
        res = None
        qr = Q()
        term = req.GET.get('term')
        serializer = UserSerializer(req.user)
        user_id = serializer.data['id']
        q = Event.objects
        try:
            qr = Q(user=user_id)
            q = q.filter(qr)
            if term not in [None, '']:
                qr = Q(event_name__icontains=term)
                q = q.filter(qr)
                hasfilter = True
            else:
                qr = Q(user=user_id)
                q = q.filter(qr)
            ser = EventsSerializer(q, many=True, context={'request': req})
            res = Response(ser.data)

        except Exception as e:
            logger.exception(e)
            res = Response({'error': 1, 'message': str(e)},
                           status=status.HTTP_404_NOT_FOUND)
        return res

    def post(self, req):
        try:
            dic = req.data
            obj = Event(
                event_name=dic['event_name'],
                selected_address=dic['selected_address'],
                location=dic['location'],
                category=dic['category'],
                about_event=dic['about_event'],
                start_time=dic['start_time'],
                start_date=dic['start_date'],
                end_time=dic['end_time'],
                end_date=dic['end_date'],
                created_by=req.user,
                user=req.user
            )
            obj.save()
            # uploadEventImage(req, obj.id)
            res = Response({'success': 1, 'id': obj.id},
                           status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception(e)
            res = Response({'error': 1, 'message': str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res

    def put(self, req, id):
        try:
            data = req.data
            o = Event.objects.get(pk=id)
            o.event_name = data['event_name']
            o.selected_address = data['selected_address']
            o.location = data['location']
            o.category = data['category']
            o.about_event = data['about_event']
            o.start_time = data['start_time']
            o.start_date = data['start_date']
            o.end_time = data['end_time']
            o.end_date = data['end_date']
            o.user = req.user
            o.save()
            res = Response({'success': 1})
        except Exception as e:
            res = Response({'error': 1, "message": str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res


class EventList(APIView):
    permission_classes = (AllowAny,)
    def get(self, req):
        print(req.user)
        res = None
        qr = Q()
        serializer = UserSerializer(req.user)
        user_id = serializer.data['id']
        q = Event.objects  # .values_list('id', flat=True).filter(user=d)
        try:
            qr = Q(user=user_id)
            q = q.filter(qr)
            ser = EventsSerializer(q, many=True, context={'request': req})
            res = Response(ser.data)
        except Exception as e:
            logger.exception(e)
            res = Response({'error': 1, 'message': str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res


class UploadEventImage(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (AllowAny,)
    def post(self, req, id, format=None):
        res = None
        isExist = False
        try:
            if req.FILES['picture'] is not None:
                o = Event.objects.get(pk=id)
                o.event_image = req.FILES['picture']
                o.save()
                return Response({'success': 1}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            res = Response({'error': 1, 'message': str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res

class testUpload(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (AllowAny,)
    def post(self, req, id, format=None):
        res = None
        try:
            user = req.user
            # id = user.id
            event_id = id
            _user = UserModel._default_manager.get_by_natural_key(user.username)
            # _event = Event._def
            if req.FILES.get('picture') is not None:
                self.upload_test_picture(req.FILES['picture'], _user, event_id)
            return Response({ 'success': 1 })
        except UserModel.DoesNotExist:
            res = Response({ 'error': constants.ErrorCode.GEN_0010 }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.exception(e)
            res = Response({ 'error': 1, 'message': str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return res

    def upload_test_picture(self, f, o, event_id):
        dic = {
            'event_image': f
        }
        # assert isinstance(o, UserModel)
        # if o.profile_pic not in [None, '']: 
        #     self.remove_profile_pic(o)

        fname = f.name
        filepath = self.get_profile_pic_test_upload_path(fname, o, event_id)
        with open(filepath, 'wb+') as fp:
            for chunk in f.chunks():
                fp.write(chunk)
        t = Event.objects.get(pk=event_id)
        t.event_image = filepath
        t.save()

    def get_profile_pic_test_upload_path(self, filename, o, event_id):
        r = None
        try:
            j = self.get_test_profile_pic_dir(o, event_id)
            self.ensure_dir(j)
            r = os.path.join(j, filename)
        except:
            raise
        return r

    def ensure_dir(self, f):
        if not os.path.exists(f):
            os.makedirs(f) 
    
    def get_test_profile_pic_dir(self, o, event_id):
        j = None
        try:
            i = os.path.join(config.MEDIA_ROOT, 'events')
            j = os.path.join(i, '__{0}__'.format(event_id))

        except:
            raise

        return j

class CreateUserView(APIView):
    permission_classes = (AllowAny,)
    res = None

    def post(self, req):
        try:
            data = req.data
            user = User.objects.create_user(username=data['email'],
                                            email=data['email'],
                                            password=data['password'])
            res = Response({'success': 1})
        except Exception as e:
            res = Response({'error': 1, 'message': str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res


class LoginWithGmail(APIView):
    permission_classes = (AllowAny,)
    res = None

    def post(self, req):
        try:
            data = req.data
            print(data)
            user = User.objects.create_user(
                username=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                password=data['password'])
            res = Response({'success': 1})
            user.save()
        except Exception as e:
            res = Response({'error': 1, 'message': str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res


class UpdateUser(APIView):
    permission_classes = (AllowAny,)

    def put(self, req):

        try:
            dic = req.data
            usr = User.objects.get(pk=dic['id'])
            usr.first_name = dic['first_name']
            usr.last_name = dic['last_name']
            usr.save()
            obj = UserProfile(
                pk=dic['id'],
                email=dic['email'],
                phone=dic['phone'],
                company_name=dic['company_name'],
                steps=int(1),
                designation=dic['designation'],
                about_me=dic['about_me'],
                address=dic['address'],
                dob=dic['dob'],
                # organization_name=dic['organization_name'],
                position_held=dic['position_held'],
                passport=dic['passport'],
                account_no=dic['account_no'],
                main_interest=dic['main_interest'],
                sub_interest=dic['sub_interest'],
                created_date=helper.current_date(),
                user=req.user,
                created_by=req.user)
            obj.save()
            if obj:
                res = Response(1)
            else:
                res = Response(
                    {'error': 1}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            res = Response({'error': 1, 'message': str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res


class uploadUserProfile(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = UserProfile.objects.all()
    serializer_class = UploadImageSerializer


class SearchList(APIView):
    permission_classes = (AllowAny,)

    def get(self, req):
        res = None
        qr = Q()
        term = req.GET.get('term')
        serializer = UserSerializer(req.user)
        user_id = serializer.data['id']
        q = Event.objects
        try:
            # qr = Q(user=user_id)
            # q = q.filter(qr)
            if term not in [None, '']:
                qr = Q(event_name__icontains=term)
                q = q.filter(qr)
                hasfilter = True
            else:
                # qr = Q(user=user_id)
                # q = q.filter(qr)
                q = Event.objects.all()
            ser = EventsSerializer(q, many=True, context={'request': req})
            res = Response(ser.data)

        except Exception as e:
            logger.exception(e)
            res = Response({'error': 1, 'message': str(e)},
                           status=status.HTTP_404_NOT_FOUND)
        return res


class getTicket(APIView):
    permission_classes = (AllowAny,)
    res = None
    haseUser = False
    isCreated = False
    qr = Q()

    def get(self, req, id):
        try:
            evList = Event.objects.all().filter(pk=id)
            for s in evList:
                qr = EventInvites(
                    # user=req.user,
                    invite_id=req.user,
                    event_id=s.id,
                    status=1,
                    created_by=req.user
                )
                qr.save()
                res = Response({'success': 1})
            # queryset = Event.objects.filter(pk=id)
            # for obj in queryset:
            #     created_by_id = obj.created_by,
            #     if created_by_id not in [None, '']:
            #         isCreated = True
            #     else:
            #         res = Response(
            #             {'event': 0, 'message': 'event has been closed'}, status=status.HTTP_404_NOT_FOUND)
            # if user_id not in [None, '']:
            #     haseUser = True
            # if id in [None, '']:
            #     res = Response({'error': 1}, status=status.HTTP_404_NOT_FOUND)
            # if haseUser and isCreated:
            #     dic = {
            #         'user': user_id,
            #         'invited_id': user_id
            #     }
            #     ser = CreateConnectionSerializer(data=dic)
            #     if ser.is_valid():
            #         ser.save()
            #         res = Response(
            #             {'success': 1}, status=status.HTTP_201_CREATED)
            #     else:
            #         res = Response(
            #             {'error': 1}, status=status.HTTP_404_NOT_FOUND)
            # else:
            #     res = Response({'error': 1}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            res = Response({'error': 1, 'message': str(e)},
                           status=status.HTTP_400_BAD_REQUEST)
        return res

# class GetEvent(id):
#         print(id)
#         return id


class AdgendaAPI(APIView):
    permission_classes = (AllowAny,)
    res = None

    def get(self, req, id):
        qr = Q()
        q = Adgenda.objects
        try:
            qr = Q(pk=id)
            q = q.filter(qr)
            ser = AdgendaSerializer(q, many=True, context={'request': req})
            res = Response(ser.data)
        except Exception as e:
            res = Response({'error': 1, "message": str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res

    def delete(self, req, id):
        try:
            q = Adgenda.objects.get(pk=id)
            q.delete()
            res = Response({'message', 'success'}, status=status.HTTP_200_OK)
        except Exception as e:
            res = Response({'error': 1, "message": str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res

    def put(self, req, id):
        try:
            o = Adgenda.objects.get(pk=id)
            data = req.data
            o.title = data['title']
            o.address = data['address']
            o.notes = data['notes']
            o.start_time = data['start_time']
            o.start_date = data['start_date']
            o.user = req.user
            o.save()
            res = Response({'success': 1})
        except Exception as e:
            res = Response({'error': 1, "message": str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res

class getAgendaConnection(APIView):
    permission_classes = (AllowAny,)
    res = None
    def get(self, req, id):
        qr = Q()
        q = AdgendaInvites.objects
        try:
            arr = []
            qr = Q(adg_id=id)
            q = q.filter(qr)
            for s in q:
                o = UserProfile.objects.all().filter(pk=s.invite_id)
                arr.extend(o)
                ser = UserProfileSerializer(arr, many=True, context={'request': req})
                res = Response(ser.data)
        except Exception as e:
            res = Response({'error': 1, "message": str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res
class SortAdgenda(APIView):

    permission_classes = (AllowAny,)
    res = None
    def get(self, req):
        prm = req.GET['prm']
        qr = Q()
        q = Adgenda.objects
        try:
            qr = Q(start_date__month=prm)
            q = q.filter(qr)
            ser = AdgendaSerializer(q, many=True, context={'request': req})
            res = Response(ser.data)
        except Exception as e:
            res = Response({'error': 1, "message": str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res
    
class CreateAdgena(APIView):
    res = None
    haseUser = False

    def post(self, req):
        isSave = False
        try:
            dic = req.data
            obj = Adgenda(
                title=dic['title'],
                address=dic['address'],
                notes=dic['notes'],
                start_time=dic['start_time'],
                start_date=dic['start_date'],
                created_by=req.user,
                user=req.user
            )
            obj.save()
            adjId = obj.id
            invites = dic['invites']
            if invites not in (None, ''):
                for iv in invites:
                    ivId = iv['id']
                    # queryset= User.objects.filter(id=ivId)
                    # for qr in queryset:
                    invite_obj = AdgendaInvites(
                        # user=req.user,
                        invite_id=ivId,
                        status=0,
                        adg_id=adjId,  # Adgenda.objects.filter(pk=adjId),
                        created_by=req.user
                    )
                    invite_obj.save()
                    res = Response(
                        {'success': 1}, status=status.HTTP_201_CREATED)
        except Exception as e:
            res = Response({'error': 1, "message": str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res

    def get(self, req):
        res = None
        qr = Q()
        serializer = UserSerializer(req.user)
        user_id = serializer.data['id']
        q = Adgenda.objects
        try:
            qr = Q(user=user_id)
            q = q.filter(qr)
            ser = AdgendaSerializer(q, many=True, context={'request': req})
            res = Response(ser.data)
        except Exception as e:
            logger.exception(e)
            res = Response({'error': 1, 'message': str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res


class Connections(APIView):
    permission_classes = (AllowAny,)
    res = None

    def get(self, req):
        qr = Q()
        q = User.objects
        conList = Connection.objects.filter(user=req.user)
        try:
            arr = []
            for co in conList:
                o = User.objects.all().filter(pk=co.id)
                arr.extend(o)
            ser = UserSerializer(arr, many=True, context={'request': req})
            res = Response(ser.data)
        except Exception as e:
            logger.exception(e)
            res = Response({'error': 1, 'message': str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res

class SearchMarketPlace(APIView):
    res = None
    def get(self, req):
        qr = Q()
        q = MarketPlace.objects
        term = req.GET['term']
        try:
            if term not in [None, '']:
                qr = Q(item_name__icontains=term)
                q = q.filter(qr)
            else:
                q = MarketPlace.objects.all()
            ser = MarketPlaceSerializer(q, many=True, context={'request': req})
            res = Response(ser.data)
        except Exception as e:
            res = Response({'error', 1}, str(e))
        return res

class MarketPlaceAPIView(APIView):
    res = None

    def post(self, req):
        try:
            data = req.data
            obj = MarketPlace(
                item_name=data['item_name'],
                price=data['price'],
                qty=data['qty'],
                desc=data['desc'],
                user=req.user,
                picture=data['picture'],
                created_by=req.user
            )
            obj.save()
            # _uploadImge(obj.id, req)
            res = Response({'success': 1, 'id': obj.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            res = Response({'error': 1, 'message': str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res

    def get(self, req, id):
        print(id)
        res = None
        qr = Q()
        q = MarketPlace.objects
        try:
            qr = Q(pk=id)
            q = q.filter(qr)
            ser = MarketPlaceSerializer(q, many=True, context={'request': req})
            res = Response(ser.data)
        except Exception as e:
            logger.exception(e)
            res = Response({'error': 1, 'message': str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res

    def put(self, req, id):
        try:
            o = MarketPlace.objects.get(pk=id)
            data = req.data
            o.item_name = data['item_name']
            o.price = data['price']
            o.qty = data['qty']
            o.desc = data['desc']
            o.picture = data['picture']
            o.user = req.user
            o.created_by = req.user
            o.save()
            res = Response({'success': 1}, status=status.HTTP_200_OK)
        except Exception as e:
            res = Response({'error': 1, 'message': str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res

 
def _uploadImge(id, file):
    def put(self, req, id):
        try:
            if req.FILES.get('picture') is not None:
                print('has image')
            # o = MarketPlace.objects.get(pk=id)
            # data = req.data
            # o.item_name = data['item_name']
            # o.price = data['price']
            # o.qty = data['qty']
            # o.desc = data['desc']
            # o.picture = data['picture']
            # o.user = req.user
            # o.created_by = req.user
            # o.save()
            res = Response({'success': 1}, status=status.HTTP_200_OK)
        except Exception as e:
            res = Response({'error': 1, 'message': str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res

    def get(self, req, id):
        print(id)
        res = None
        qr = Q()
        q = MarketPlace.objects
        try:
            qr = Q(pk=id)
            q = q.filter(qr)
            ser = MarketPlaceSerializer(q, many=True, context={'request': req})
            res = Response(ser.data)
        except Exception as e:
            logger.exception(e)
            res = Response({'error': 1, 'message': str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res


class MarketPlaceList(APIView):
    permission_classes = (AllowAny,)

    def get(self, req):
        res = None
        qr = Q()
        serializer = MarketPlaceSerializer(req.user)
        user_id = serializer.data['id']
        q = MarketPlace.objects  # .values_list('id', flat=True).filter(user=d)
        try:
            qr = Q(user=user_id)
            q = q.filter(qr)
            ser = MarketPlaceSerializer(q, many=True, context={'request': req})
            res = Response(ser.data)
        except Exception as e:
            logger.exception(e)
            res = Response({'error': 1, 'message': str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res

class GlobalMarketPlaceList(APIView):
    permission_classes = (AllowAny,)

    def get(self, req):
        res = None
        try:
            queryset = MarketPlace.objects.all()
            ser = MarketPlaceSerializer(queryset, many=True, context={'request': req})
            res = Response(ser.data)
        except Exception as e:
            res = Response({'error': 1, 'message': str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res

class MarketPlaceUploadPicture(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (AllowAny,)
    res = None
    def post(self, req, id, format=None):
        res = None
        user = req.user
        try:
            # id = user.id
            _user = UserModel._default_manager.get_by_natural_key(user.username)
            if req.FILES.get('picture') is not None:
                # o = Event.objects.get(pk=3)
                self.upload_picture(req.FILES['picture'], _user, id)
                res = Response({ 'success': id })
            else:
                res = Response({'no picture': 1}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(e)
            res = Response({'error': 1, 'message': str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res

    def upload_picture(self, f, o, id):
        dic = {
            'picture': f
        }

        fname = f.name
        filepath = self.get_upload_path(o, fname, id)
        with open(filepath, 'wb+') as fp:
            for chunk in f.chunks():
                fp.write(chunk)
        t = MarketPlace.objects.get(pk=id)
        t.picture = filepath
        t.save()

    def remove_profile_pic(self, o):
        try:
            k = self.get_profile_pic_path(o)
            if k not in [None, ''] and os.path.exists(k):
                os.remove(k)     
        except Exception as e:
            raise e

    def get_upload_path(self, o, filename, id):
        r = None
        try:
            j = self.get_profile_pic_dir(o, id)
            self.ensure_dir(j)
            r = os.path.join(j, filename)

        except:
            raise

        return r

    def ensure_dir(self, f):
        if not os.path.exists(f):
            os.makedirs(f)

    def get_profile_pic_dir(self, o, id):
        j = None
        try:
            i = os.path.join(constants.MEDIA_PATH.MARKET_PLACE_MEDIA_PATH)
            j = os.path.join(i, '__{0}__'.format(id))
        except Exception as e:
            raise e

        return j

class UserProfilePictureUpload(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (AllowAny,)

    def post(self, req, id, format=None):
        res = None
        isExist = False
        try:
            if req.FILES['picture'] is not None:
                queryset = UserProfile.objects.filter(pk=id)
                for j in queryset:
                    imgPath = j.picture
                    if imgPath not in [None, '']:
                        k = str(j.picture).split('/')
                o = UserProfile.objects.get(pk=id)
                o.picture = req.FILES['picture']
                o.save()

                return Response({'success': 1}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            res = Response({'error': 1, 'message': str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res


def _delete_file(image):
    isDeleted = False
    path = str(constants.MEDIA_PATH.USER_PP_PATH+'/'+image)
    if os.path.isfile(path):
        os.remove(path)
        isDeleted = True
    else:
        # os.remove(path)
        isDeleted = False
    return isDeleted


class InviteConnections(APIView):
    res = None
    hasUser = False

    def post(self, req):
        try:
            if req.user not in [None, '']:
                for o in req.data:
                    ser = Connection(
                        user=req.user,
                        invited_id=o['id'],
                        modified_by=req.user
                    )
                    ser.save()
                res = Response({'success ': 1})
            else:
                res = Response(
                    {'error', 1}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            res = Response({'error': 1, 'message': str(e)},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res

class Calendar(APIView):
    res = None
    def get(self, req):
        con = connection.cursor()
        obj = []
        try:
            terms = req.GET['terms']
            con.callproc('g_search',[terms,])
            for o in con:
                print(o)
                obj = [
                    {
                        'id': o[0]
                    }
                ]
            res = Response({'err':1}, status=status.HTTP_200_OK)
        except Exception as e:
            res = Response({'error':1}, str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res

class Records(APIView):
    res = None
    def get(self, req):
        con = connection.cursor()
        obj = []
        try:
            con.callproc('count_records',[1,])
            for o in con:
                obj = [
                    {
                        'count_event': o[0],
                        'count_agenda': o[1],
                        'count_market_place': o[2]
                    }
                ]
                res = Response(obj, status=status.HTTP_200_OK)
        except Exception as e:
            res = Response({'error':1}, str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return res