#coding=utf8
HEADERS = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate, sdch",
    "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36"
}

HTT_QUERY = [
u"黄婷婷",
u"SNH48黄婷婷",
u"卡黄",
u"卡黄大法好",
u"撸黄",
u"黄顶顶",
u"阔太太",
u"W婷",
u"黄婷婷 SNH48",
u"粤黄",
u"婷鞠",
u"卡黄一生推",
u"黄様探侦社",
u"百变婷婷",
u"婷婷桑",
u"卡黄夜蝶",
u"黄婷婷生诞",
u"鞠婷",
u"撸黄大法好",
u"李艺彤X黄婷婷",
u"卡黄大法",
u"HTT",
u"snh48黄婷婷",
u"婷朵",
u"李芳",
u"李艺彤黄婷婷",
u"黄婷婷0908生日快乐",
u"w婷",
u"芬芳大法好",
u"SNH黄婷婷",
u"黄奉贤",
u"阿黄",
u"HTT48",
u"爱生活 爱卡黄",
u"笑颜一番黄婷婷",
u"黄宇直",
u"卡黄应援会",
u"黃婷婷",
u"kotete",
u"小黄歌",
u"snh黄婷婷",
u"婷婷我爱你！",
u"黄糖大法好",
u"曾艳芳生诞祭",
u"婷婷不哭",
u"黄宇直做受好开心啊",
u"陆黄",
u"糖黄",
u"灵魂歌姬黄婷婷",
u"芳华绝代",
u"芳婷",
u"黄婷婷你要负责",
u"靠脸吃饭的黄婷婷",
u"芬芳",
u"黄婷婷为什么那么可爱",
u"熊婷",
u"忘了说这是婷鞠应援会扒的档!",
u"黄卡络",
u"超绝可爱黄婷婷！",
u"辣黄",
u"卡黄使我快乐",
u"SNH48婷鞠",
u"阔太太娶我",
u"世界上最偏袒的就是黄婷婷拉!",
u"真娜娜说发卡看了婷婷篇",
u"阿黄唱歌真好看",
u"w队长",
u"强行卡黄",
u"黄豆豆",
u"婷婷那么可爱把她吃掉！",
u"黄婷婷 夜蝶CUT",
u"w队",
u"鞠卡黄",
u"婷婷桑的笑颜由我来守护",
u"想婷婷",
u"黄战队",
u"向全世界安利黄婷婷",
u"谁说卡黄不能HE！",
u"贤婷",
u"婷婷心里苦",
u"最喜欢黄婷婷了",
u"熊婷年",
u"我是ALL黄党",
u"卡黄 越人歌 爱情",
u"大黄",
u"婷婷",
u"撸黄之歌",
u"黄鹤",
u"鹿黄",
u"黄婷婷的性格魅力",
]

XML_DIR = '../xml_dir'

METADATA_DIR = '../metadata_dir'

COMMNETS_DIR = '../comments_dir'

APPKEY = 'f3bb208b3d081dc8'

SECRETKEY_MINILOADER = '1c15888dc316e05a15fdd0a02ed6584f'

DEFAULT_SQL = """
CREATE DATABASE IF NOT EXISTS XFS_DB charset=utf8;

CREATE TABLE IF NOT EXISTS XFS_DB.query_table(
    aid int primary key,
    query_word char(100) not null, 
    page_num int,
    video_url varchar(1000),
    crawler_time int,
    video_matrix varchar(10000)
) charset=utf8;

CREATE TABLE IF NOT EXISTS XFS_DB.need_crawl_url(
    aid int primary key,
    url varchar(1000),
    create_time int,
    finished_time int default 0
)charset=utf8;
m
"""