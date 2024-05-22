import os
import re
from bilibili_api import Credential, video
import asyncio
from bilibili_api import hot, sync, rank, comment, ass
import time


class Config:
    def __init__(self):
        self.cookie = {
            'nostalgia_conf': '-1',
            'buvid3': 'D816C5AD-7579-6363-F5C4-23125832926A90798infoc',
            'b_nut': '1688752190',
            '_uuid': '10E46C62F-137F-7DF2-A942-95CFA1D8EADA94011infoc',
            'buvid4': '25E17BC9-7291-30D8-E1D3-ACC353ADBD4693987-023070801-L6MWEtlHrdgqtFCeP9wSpA%3D%3D',
            'LIVE_BUVID': 'AUTO7316888360092435',
            'rpdid': "|(k|Rlu|uR)J0J'uYm|lJl~|l",
            'header_theme_version': 'CLOSE',
            'is-2022-channel': '1',
            'buvid_fp_plain': 'undefined',
            'enable_web_push': 'DISABLE',
            'CURRENT_BLACKGAP': '0',
            'fingerprint': '25d558c7cab255e6fa58253113306a8d',
            'SESSDATA': '9d786c7e%2C1716395537%2C35ab4%2Ab1CjAq28qVWwc9nnelEhccEVohWlob8aCZ1csPhBykIDeDihEJ-0nQYv_udKBFm1V3KRQSVmtMYjktcmtGekplYXBjOUo3dmhlVkhIUVRWQXE0R1g1QUJTVkQzUWtnaW5MbTZ3b2xYalRES1RZVktZdzJHWVJPbkZ4ek42YWhfYXBLS0dWbWRRX0tBIIEC',
            'bili_jct': '87b0c339499db109cd58260ba8d2b316',
            'DedeUserID': '1090496218',
            'DedeUserID__ckMd5': '8541e68102bf44c1',
            'CURRENT_QUALITY': '80',
            'CURRENT_FNVAL': '4048',
            'PVID': '1',
            'buvid_fp': '2a5c1651375f63e21c39a289bf7db36a',
            'bp_video_offset_1090496218': '919833818448265236',
            'FEED_LIVE_VERSION': 'V_DYN_LIVING_UP',
            'home_feed_column': '5',
            'browser_resolution': '1865-937',
            'bp_t_offset_1090496218': '923575628316278804',
            'b_lsid': '4C429376_18F13BE1C33',
            'bili_ticket': 'eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTQyODI0MjQsImlhdCI6MTcxNDAyMzE2NCwicGx0IjotMX0.0RuEXb3FVn4Im3rPONaRfyDKz9PgDyUhIQ_AybL3NEs',
            'bili_ticket_expires': '1714282364',
            'sid': '6xws2goi',
        }


class Bilibili:
    def __init__(self):
        self.cookies = Config()
        self.sessdata = self.cookies.cookie.get('SESSDATA')
        self.bili_jct = self.cookies.cookie.get('bili_jct')
        self.buvid3 = self.cookies.cookie.get('buvid3')
        self.dedeuserid = self.cookies.cookie.get('DedeUserID')
        if [self.sessdata, self.bili_jct, self.buvid3, self.dedeuserid]:
            self.credential = Credential(sessdata=self.sessdata, bili_jct=self.bili_jct, buvid3=self.buvid3,
                                         dedeuserid=self.dedeuserid)
            self.credential.get_cookies()

    async def video_(self, bvid: str = None):
        # 实例化 Credential 类
        credential = self.credential
        # 实例化 Video 类
        v = video.Video(bvid=bvid, credential=credential)
        # 获取视频信息
        info = await v.get_info()
        # 打印视频信息
        # print(info)
        # 给视频点赞
        await v.like(True)
        return v

    # 热门
    def get_hot_data(self, pn: int = 1):
        return sync(hot.get_hot_videos(pn=pn))

    # 排行榜100名
    def get_rank(self, field_type=rank.RankType.All):
        """
            All: 全部
            Bangumi: 番剧
            GuochuanAnime: 国产动画
            Guochuang: 国创相关
            Documentary: 纪录片
            Douga: 动画
            Music: 音乐
            Dance: 舞蹈
            Game: 游戏
            Knowledge: 知识
            Technology: 科技
            Sports: 运动
            Car: 汽车
            Life: 生活
            Food: 美食
            Animal: 动物圈
            Kitchen: 鬼畜
            Fashion: 时尚
            Ent: 娱乐
            Cinephile: 影视
            Movie: 电影
            TV: 电视剧
            Variety: 综艺
            Original: 原创
            Rookie: 新人
        :return:
        """
        return sync(rank.get_rank(type_=field_type))

    # 获取评论
    async def comment_(self, oid: int = None):
        # 存储评论
        comments = []
        # 页码
        page = 1
        # 当前已获取数量
        count = 0
        while True:
            # 获取评论
            c = await comment.get_comments(oid=oid, type_=comment.CommentResourceType.VIDEO, page_index=page,
                                           credential=self.credential)
            # 存储评论
            comments.extend(c['replies'])
            # 增加已获取数量
            count += c['page']['size']
            # 增加页码
            page += 1

            if count >= c['page']['count']:
                # 当前已获取数量已达到评论总数，跳出循环
                break

        # 打印评论
        # for cmt in comments:
        #     print(cmt)
        # print(f"{cmt['member']['uname']}: {cmt['content']['message']}")
        # 打印评论总数
        print(f"\n\n共有 {count} 条评论（不含子评论）")
        # print(comments)
        return comments

    def danmu_(self, bvid: str = None):
        v = video.Video(bvid=bvid, credential=self.credential)
        sync(ass.make_ass_file_danmakus_protobuf(
            credential=self.credential,
            obj=v,  # 生成弹幕文件的对象
            page=0,  # 哪一个分 P (从 0 开始)
            out=f"danmu/{bvid}.ass"  # 输出文件地址
        ))

        return 'result'

    def get_danmu(self, bvid: str = None):
        self.danmu_(bvid=bvid)

    def get_comment(self, oid: int = None):
        loop = asyncio.new_event_loop()
        comment = loop.run_until_complete(self.comment_(oid=oid))
        return comment

    # 视频点赞
    def get_video(self, bvid: str = None):
        data = asyncio.get_event_loop().run_until_complete(self.video_(bvid=bvid))
        return data


class Spider:
    def __init__(self):
        self.spider = Bilibili()
        self.fields = {
            'hot_list': '综合热门',
            'All': rank.RankType.All,
            'Bangumi': rank.RankType.Bangumi,
            'GuochuanAnime': rank.RankType.GuochuangAnime,
            'Guochuang': rank.RankType.Guochuang,
            'Documentary': rank.RankType.Documentary,
            'Douga': rank.RankType.Douga,
            'Music': rank.RankType.Music,
            'Dance': rank.RankType.Dance,
            'Game': rank.RankType.Game,
            'Knowledge': rank.RankType.Knowledge,
            'Technology': rank.RankType.Technology,
            'Sports': rank.RankType.Sports,
            'Car': rank.RankType.Car,
            'Life': rank.RankType.Life,
            'Food': rank.RankType.Food,
            'Animal': rank.RankType.Animal,
            'Kitchen': rank.RankType.Kichiku,
            'Fashion': rank.RankType.Fashion,
            'Ent': rank.RankType.Ent,
            'Cinephile': rank.RankType.Cinephile,
            'Movie': rank.RankType.Movie,
            'TV': rank.RankType.TV,
            'Variety': rank.RankType.Variety,
            'Original': rank.RankType.Original,
            'Rookie': rank.RankType.Rookie
        }

    def hot(self, page: int = 1):
        for i in range(page):
            hot_info = self.spider.get_hot_data(pn=i + 1)
            if hot_info['list']:
                for hot in hot_info['list']:
                    hot_ = {
                        'aid': hot['stat'].get('aid', 0),
                        'view': hot['stat'].get('view', 0),
                        'danmaku': hot['stat'].get('danmaku', 0),
                        'reply': hot['stat'].get('reply', 0),
                        'favorite': hot['stat'].get('favorite', 0),
                        'coin': hot['stat'].get('coin', 0),
                        'share': hot['stat'].get('share', 0),
                        'his_rank': hot['stat'].get('his_rank', 0),
                        'like': hot['stat'].get('like', 0),
                        'ctime': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(hot['ctime'])),
                        'pubdate': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(hot['pubdate'])),
                        'pub_location': hot.get('pub_location', '无'),
                        'title': hot.get('title', '无'),
                        'tname': hot.get('tname', '无'),
                        'owner_name': hot.get('owner', '无').get('name', '无'),
                        'desc': hot.get('desc', '无'),
                        'bvid': hot.get('bvid', '无'),
                        'category': 'hot_list',
                    }
                    yield hot_

    def rank(self, field: str = 'All'):
        obj = self.fields.get(field)
        if obj:
            data_ = self.spider.get_rank(field_type=obj)
            if data_.get('list'):
                for rank_data in data_['list']:
                    rank_info = {
                        'aid': rank_data['stat'].get('aid', 0),
                        'view': rank_data['stat'].get('view', 0),
                        'danmaku': rank_data['stat'].get('danmaku', 0),
                        'reply': rank_data['stat'].get('reply', 0),
                        'favorite': rank_data['stat'].get('favorite', 0),
                        'coin': rank_data['stat'].get('coin', 0),
                        'share': rank_data['stat'].get('share', 0),
                        'his_rank': rank_data['stat'].get('his_rank', 0),
                        'like': rank_data['stat'].get('like', 0),
                        'ctime': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(rank_data['ctime'])),
                        'pubdate': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(rank_data['pubdate'])),
                        'pub_location': rank_data.get('pub_location', '无'),
                        'title': rank_data.get('title', '无'),
                        'tname': rank_data.get('tname', '无'),
                        'owner_name': rank_data.get('owner', '无').get('name', '无'),
                        'desc': rank_data.get('desc', '无'),
                        'bvid': rank_data.get('bvid', '无'),
                        'category': field,
                    }
                    yield rank_info

    def comment(self, oid: int = None):
        info_ = self.spider.get_comment(oid=oid)
        for comment_ in info_:
            comment_data = {
                'aid_id': oid,
                'r_pid': comment_.get('rpid'),
                'content': comment_.get('content').get('message'),
                'mid': comment_.get('member').get('mid'),
                'referenceName': comment_.get('member').get('uname'),
                'referenceSex': comment_.get('member').get('sex'),
                'referenceTime': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(comment_['ctime'])),
                'location': comment_.get('reply_control').get('location', 'IP属地：无').split('：')[1],
            }
            yield comment_data

    def danmu(self, bvid: str = None):
        self.spider.get_danmu(bvid=bvid)
        return '弹幕采集成功'

    def run_spider(self, field: str = 'hot_list', page=None, oid: int = None, bvid: str = None):
        if page and field == 'hot_list':
            return self.hot(page=page)
        elif oid:
            return self.comment(oid=oid)
        elif bvid:
            return self.danmu(bvid=bvid)
        else:
            return self.rank(field=field)


class ReadDanmu:
    def __init__(self, file_name: str = None):
        file_path = 'danmu/'
        self.file_path = file_path + f'{file_name}.ass'

    def file_name(self) -> bool:
        result = os.path.exists(self.file_path)
        return result

    def read_ass(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            result = f.readlines()
        for res in result:
            danmu = re.findall(r'Dialogue:(.*)', res)
            if danmu:
                d_str = danmu[0].split(',')[-1].split('}')[-1]
                chinese = ''.join(re.findall('[\u4e00-\u9fa5]', d_str))
                if chinese:
                    yield chinese

    def danmu(self):
        file_name = self.file_name()
        if file_name:
            return self.read_ass()
        else:
            return file_name


if __name__ == '__main__':
    spider = Spider()
    data = spider.run_spider(oid=823886057)
    for info in data:
        print(info)
