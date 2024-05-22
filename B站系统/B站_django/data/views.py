import random
import time
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from .clearning import Clearing
from .models import *
from .serializers import *
from .spider import Spider


# Create your views here.
class RegisterView(ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        user_name = data.get('username', {})
        user = UserModel.objects.filter(username=user_name).first()
        password = data.get('password', {})
        encrypt_password = make_password(password=str(password))
        if not user:
            request.data['password'] = encrypt_password
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=201, data=serializer.data, template_name=HTTP_201_CREATED)
        return Response(template_name=HTTP_400_BAD_REQUEST, status=401, data={'msg': '该用户已存在'})


class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if username and password:
            user = UserModel.objects.get(username=username)
            refresh = RefreshToken.for_user(user)
            access_token = 'Bearer ' + str(refresh.access_token)
            data = {
                'token': access_token,
                'refresh': str(refresh),
                'user_id': str(user.id),
                'user_name': str(user.username),
                'is_active': str(user.is_active),
            }
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserImageView(ModelViewSet):
    queryset = UserImage.objects.all()
    serializer_class = UserImageSerializer

    def list(self, request, *args, **kwargs):
        uid = request.query_params.get('uid')
        image = UserImage.objects.filter(user_id=uid).first()
        if image:
            image_url = image.image
            data = f'http://127.0.0.1:8000/media/{image_url}'
            return Response({'code': 200, 'msg': '查询成功', 'data': data})
        data = '/static/images/users/avatar.jpg'
        return Response({'code': 200, 'msg': '无头像信息', 'data': data})

    def create(self, request, *args, **kwargs):
        file = request.data.get('file')
        uid = request.data.get('uid')
        print(uid)
        if file:
            image = UserImage.objects.filter(user_id=uid).first()
            if image:
                image.delete()
                instance = UserImage.objects.update_or_create(image=file, user_id=uid)
                data = self.get_serializer(instance).data
                return Response({'code': 201, 'msg': '上传成功', 'data': data})
            instance = UserImage.objects.create(image=file, user_id=uid)
            data = self.get_serializer(instance).data
            return Response({'code': 201, 'msg': '上传成功', 'data': data})
        return Response({'code': 200, 'msg': '更新成功', 'data': 'file'})


class UserProfile(ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class ChangePassword(ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        data = request.user
        info = request.data
        old_password = info.get('old_password', {})
        password1 = info.get('password1', {})
        password2 = info.get('password2', {})
        user = UserModel.objects.filter(id=data.id).first()
        result = check_password(old_password, user.password)
        if result:
            if password1:
                sys_password = user.password
                if make_password(str(password1)) != sys_password:
                    if password1 == password2:
                        UserModel.objects.update(password=make_password(str(password2)))
                        return Response({'code': 204, 'msg': '密码修改成功'})
                    return Response({'code': 502, 'msg': '两次密码输入不相同'})
                return Response({'code': 501, 'msg': '新密码不能和旧密码相同'})
            return Response({'code': 400, 'msg': '密码不能为空'})
        return Response({'code': 400, 'msg': '旧密码不正确'})


class ChangeUser(ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = ChangeUserSerializer
    permission_classes = [AllowAny, ]


class SpiderView(ModelViewSet):
    from django.core.cache import cache
    cache.clear()
    queryset = SpiderModel.objects.all()
    serializer_class = SpiderSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        info = SpiderSerializer(queryset, many=True)
        spider_info = info.data
        data = []
        for spider_data in spider_info:
            info = {
                'id': spider_data.get('id'),
                'spider_field': spider_data.get('spider_field'),
                'name': spider_data.get('spider_name'),
                'create': spider_data.get('create_time'),
                'schedule': spider_data.get('spider_states'),
                'run_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                'states': spider_data.get('spider_states'),
            }
            data.append(info)
        filed = {'field':
                     {'hot_list': '综合热门',
                      'All': '全部',
                      'Bangumi': '番剧',
                      'GuochuanAnime': '国产动画',
                      'Guochuang': '国创相关',
                      'Documentary': '纪录片',
                      'Douga': '动画',
                      'Music': '音乐',
                      'Dance': '舞蹈',
                      'Game': '游戏',
                      'Knowledge': '知识',
                      'Technology': '科技',
                      'Sports': '运动',
                      'Car': '汽车',
                      'Life': '生活',
                      'Food': '美食',
                      'Animal': '动物圈',
                      'Kitchen': '鬼畜',
                      'Fashion': '时尚',
                      'Ent': '娱乐',
                      'Cinephile': '影视',
                      'Movie': '电影',
                      'TV': '电视剧',
                      'Variety': '综艺',
                      'Original': '原创',
                      'Rookie': '新人'}
                 }
        return Response({'code': 200, 'msg': '获取成功', 'data': data, 'field': filed})


class CommentView(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        ser_data = self.get_serializer(queryset, many=True).data
        count = self.queryset.count()
        return Response({'code': 200, 'msg': '数据获取成功', 'count': count, 'data': ser_data})

    def create(self, request, *args, **kwargs):
        oid = request.data.get('oid', {})
        bvid = request.data.get('bvid', {})
        print(bvid)
        if oid:
            spider = Spider()
            aid = HotListModel.objects.filter(aid=oid).first()
            comments = spider.run_spider(oid=oid)
            try:
                for comment in comments:
                    try:
                        comment['aid_id'] = aid.aid
                        comment['create_user'] = request.user.id
                        Comment.objects.update_or_create(**comment)
                        print(comment)
                    except Exception as e:
                        return Response({'code': 405, 'msg': f'{e}'})
                return Response({'code': 201, 'msg': f'用户ID为{oid}评论采集成功'})

            except Exception as e:
                print('数据异常------------->', e)
                return Response({'code': 405, 'msg': f'{e}'})
        if bvid:
            try:
                spider = Spider()
                result = spider.run_spider(bvid=bvid)
                print(result)
                return Response({'code': 201, 'msg': 'ok'})
            except Exception as e:
                return Response({'code': 405, 'msg': f'{e}'})


class Chart(ModelViewSet):
    queryset = HotListModel.objects.all()
    serializer_class = HotListSerializer

    def list(self, request, *args, **kwargs):
        data = self.queryset
        word = request.query_params
        print(word.get('key'))
        if word.get('key') == 'city':
            info = self.get_serializer(data, many=True).data
            chart_info = Clearing(data=info)
            df = [chart_info.city()]
            return Response({'code': 200, 'msg': '数据获取成功', 'data': df})
        elif word.get('key') == 'score':
            info = self.get_serializer(data, many=True).data
            chart_info = Clearing(data=info)
            df = chart_info.score()
            all_count = sum(df.values())
            info = []
            for key, value in df.items():
                score = [key, round(value / all_count * 100, 2)]
                info.append(score)
            return Response({'code': 200, 'msg': '数据获取成功', 'data': info})
        elif word.get('key') == 'word':
            info = self.get_serializer(data, many=True).data
            chart_info = Clearing(data=info)
            data = chart_info.categories_count()
            return Response({'code': 200, 'msg': '数据获取成功', 'data': data})
        elif word.get('key') == 'date':
            info = self.get_serializer(data, many=True).data
            chart_info = Clearing(data=info)
            data = chart_info.date()
            return Response({'code': 200, 'msg': '数据获取成功', 'data': data})
        elif word.get('key') == 'cloud':
            queryset = Comment.objects.all()
            info = CommentSerializer(queryset, many=True).data
            chart_info = Clearing(data=info)
            data = chart_info.cloud()
            return Response(status=200, data={'data': data})
        elif word.get('key') == 'aero':
            info = self.get_serializer(data, many=True).data
            chart_info = Clearing(data=info)
            data = chart_info.aero()
            return Response(status=200, data={'data': data})
        elif word.get('key') == 'three':
            info = self.get_serializer(data, many=True).data
            chart_info = Clearing(data=info)
            data = chart_info.three()
            return Response(status=200, data={'data': data})


class HotListView(ModelViewSet):
    queryset = HotListModel.objects.all()
    serializer_class = HotListSerializer

    def list(self, request, *args, **kwargs):
        params = request.query_params.get('key', 'undefined')
        if params == 'undefined':
            data = self.queryset
            ser_data = self.get_serializer(data, many=True).data
            return Response({'code': 200, 'msg': '数据获取成功', 'data': ser_data})
        data = self.queryset.filter(category=params).all()
        ser_data = self.get_serializer(data, many=True).data
        return Response({'code': 200, 'msg': '数据获取成功', 'data': ser_data})

    def create(self, request, *args, **kwargs):
        field = request.data.get('field', 'hot_list')
        spider = Spider()
        hot_spider = SpiderModel.objects.filter(spider_field=field).first()
        spider_id = hot_spider.id
        print(spider_id)
        if field == 'hot_list':
            page = hot_spider.spider_page
            data_ = spider.run_spider(field=field, page=page)
            try:
                for data in data_:
                    try:
                        data['spider_id'] = spider_id
                        data['create_user'] = request.user.id
                        HotListModel.objects.update_or_create(**data)
                        print(data)
                    except Exception as e:
                        print('数据已存在')
                SpiderModel.objects.filter(id=spider_id).update(spider_states=True)
            except Exception as e:
                print('数据已存在')
        else:
            data_ = spider.run_spider(field=field)
            try:
                for data in data_:
                    try:
                        data['spider_id'] = spider_id
                        data['create_user'] = request.user.id
                        HotListModel.objects.update_or_create(**data)
                        print(data)
                    except Exception as e:
                        print('数据已存在')
                SpiderModel.objects.filter(id=spider_id).update(spider_states=True)
            except Exception as e:
                print('数据已存在')

        return Response({'code': 201, 'msg': '爬取成功', 'data': 'data'})


class Screen(ModelViewSet):
    queryset = HotListModel.objects.all()
    serializer_class = HotListSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        status = {'code': 200, 'msg': '请求成功', 'data': 'data'}
        key = request.query_params.get('key', {})
        data = self.queryset
        if key == 'time':
            data = self.get_serializer(data, many=True).data
            chart_info = Clearing(data=data)
            info = {'category': [],
                    'value': []}
            for key, value in chart_info.s_word_count().items():
                info['category'].append(key[5:])
                info['value'].append(value)
            status['data'] = info
            return Response(status)
        if key == 'category':
            data = self.get_serializer(data, many=True).data
            chart_info = Clearing(data=data)
            info = {'category': [],
                    'value': []}
            for key, value in chart_info.s_city().items():
                info['category'].append(key)
                info['value'].append(value)
            status['data'] = info
            return Response(status)
        if key == 'aero':
            data = self.get_serializer(data, many=True).data
            chart_info = Clearing(data=data)
            data_ = []
            info_ = []
            for key, value in chart_info.s_score().items():
                data_.append(key)
                info_.append({'value': value, 'name': key})
            data_info = {
                'data': data_,
                'info': info_
            }
            status['data'] = data_info
            return Response(status)
        if key == 'm_date':
            data = self.get_serializer(data, many=True).data
            chart_info = Clearing(data=data)
            data_ = []
            info_ = []
            for key, value in chart_info.s_score().items():
                data_.append(key)
                info_.append({'value': value, 'name': key})
            data_info = {
                'data': data_,
                'info': info_
            }
            status['data'] = data_info
            return Response(status)
        if key == 'date':
            data = self.get_serializer(data, many=True).data
            chart_info = Clearing(data=data)
            data_ = []
            info_ = []
            for key, value in chart_info.s_date().items():
                data_.append(key)
                info_.append({'value': value, 'name': key})
            data_info = {
                'data': data_,
                'info': info_
            }
            status['data'] = data_info
            return Response(status)
        if key == 'video':
            spider = HotListModel.objects.all()
            video_data = HotListSerializer(spider, many=True)
            chart_info = Clearing(data=video_data.data)
            info = {'category': [],
                    'value': []}
            for key, value in chart_info.video().items():
                info['category'].append(key)
                info['value'].append(value)
            status['data'] = info
            return Response(status)
        if key == 'video_overview':
            spider = HotListModel.objects.all()
            video_data = HotListSerializer(spider, many=True)
            chart_info = Clearing(data=video_data.data)
            info = {
                'category': list(chart_info.video_overview().get('title').values()),
                'view': list(chart_info.video_overview().get('view').values()),
                'reply': list(chart_info.video_overview().get('reply').values()),
                'danmaku': list(chart_info.video_overview().get('danmaku').values()),
                'coin': list(chart_info.video_overview().get('coin').values()),
            }
            status['data'] = info
            return Response(status)
        if key == 's_comment':
            data = self.get_serializer(data, many=True).data
            chart_info = Clearing(data=data)
            data_ = []
            info_ = []
            for key, value in chart_info.s_comment().items():
                data_.append(key)
                info_.append({'value': value, 'name': key})
            data_info = {
                'data': data_,
                'info': info_
            }
            status['data'] = data_info
            return Response(status)
        if key == 'video_city':
            spider = HotListModel.objects.all()
            video_data = HotListSerializer(spider, many=True)
            chart_info = Clearing(data=video_data.data)
            info = []
            for key, value in chart_info.video_city().items():
                info.append({
                    'name': key,
                    'value': value
                })
            status['data'] = info
            return Response(status)
        if key == 'title':
            spider = HotListModel.objects.all()
            video_data = HotListSerializer(spider, many=True)
            chart_info = Clearing(data=video_data.data)
            data = chart_info.screen()
            print(data)
            # info = {'category': [],
            #         'value': []}
            # for key, value in chart_info.video().items():
            #     info['category'].append(key)
            #     info['value'].append(value)
            status['data'] = data
            return Response(status)
        if key == 'hour':
            spider = HotListModel.objects.all()
            video_data = HotListSerializer(spider, many=True)
            chart_info = Clearing(data=video_data.data)
            info = []
            chart_info.hour()
            val = 0
            for value in chart_info.hour().values():
                val += value
            for key, value in chart_info.hour().items():
                info.append({
                    'name': f'{key}时',
                    'value': round((value / val) * 100, 2)
                })
            status['data'] = info
            return Response(status)
        return Response(status)
