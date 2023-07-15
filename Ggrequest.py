import random
import json
from mylib import *
import csv

class Size:
    def __init__(self, w, h):
        self.w = w
        self.h = h

class Ad_Unit:
    def __init__(self, no, hrc, code, sizes):
        self.no = no
        self.hrc = hrc
        self.code = code
        self.dy_id = random_position()
        self.sizes = sizes

class Ad_Unit_Video:
    def __init__(self, no, hrc):
        self.no = no
        self.hrc = hrc
        self.code = 'shorts'
        self.dy_id = random_position()
        self.sizes = [Size(200, 800)]

class Ggrequests:
    def __init__(self, cid, req_id, cnt_id, lang, mockup_ip, nw_id, pub_id, more_info, ad_units):
        self.cid = cid
        self.req_id = req_id
        self.cnt_id = cnt_id
        self.lang = lang
        self.mockup_ip = mockup_ip
        self.nw_id = nw_id
        self.pub_id = pub_id
        self.more_info = more_info
        self.ad_units = ad_units

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Size):
            return {'w': obj.w, 'h': obj.h}
        elif isinstance(obj, Ad_Unit):
            return {
                'no': obj.no,
                'hrc': obj.hrc,
                'code': obj.code,
                'dy_id': obj.dy_id,
                'sizes': [self.default(size) for size in obj.sizes]  # 序列化列表中的每个元素
            }
        elif isinstance(obj, Ad_Unit_Video):
            return {
                'no': obj.no,
                'hrc': obj.hrc,
                'code': obj.code,
                'dy_id': obj.dy_id,
                'sizes': [self.default(size) for size in obj.sizes]
            }
        elif isinstance(obj, Ggrequests):
            return {
                'cid': obj.cid,
                'req_id': obj.req_id,
                'cnt_id': obj.cnt_id,
                'lang': obj.lang,
                'nw_id': obj.nw_id,
                'pub_id': obj.pub_id,
                'more_info': obj.more_info,
                'ad_units': [self.default(ad_unit) for ad_unit in obj.ad_units]  # 序列化列表中的每个元素
            }
        return super().default(obj)
    
def random_size():
    return random.choice([Size(200, 200), Size(300, 600), Size(300, 250), Size(540, 450), Size(450, 180), Size(728, 90), Size(900, 112)])


def random_sizes():
    sizes = list()
    sizes.append(random_size())
    return sizes

def random_Ad_Unit(num):
    return Ad_Unit(num, random_text('hrc_'), random_zone(), random_sizes())


def random_Ad_Unit_Video(num):
    return Ad_Unit_Video(num, random_text('hrc_'))

def random_Ad_Units():
    ads_units = list()
    num = 1
    range1 = random.randint(1, 4)
    for i in range(range1):
        ads_units.append(random_Ad_Unit(num + i))  
    num = num + range1
    for i in range(random.randint(1, 2)):
        ads_units.append(random_Ad_Unit_Video(num + i))
    return ads_units

def fixed_Ad_Units():
    ads_units = list()
    ads_units.append(Ad_Unit(1, "Basketball", "z_a_c_1", sizes=[Size(900, 112)]))
    ads_units.append(Ad_Unit(2, "Football", "z_a_c_2", sizes=[Size(540, 450), Size(300,600)]))
    ads_units.append(Ad_Unit(3, "Tennis", "z_v_r_r_1", sizes=[Size(450, 180)]))
    ads_units.append(Ad_Unit(4, "Soccer", "z_v_r_b_2", sizes=[Size(300, 250)]))
    ads_units.append(Ad_Unit(5, "Golf", "z_a_b_1", sizes=[Size(728, 90)]))

    return ads_units

def generate_random_ggrequest_body():
    tmp = Ggrequests(random_text('cid_'), random_text('req_'), random_text('cnt_'), random_lang(), mockupip(), random_text('hw_'), random_text('pub_'), False, random_Ad_Units())
    result = json.loads(json.dumps(tmp, cls=CustomEncoder))
    return result

def generate_random_ggrequest_body2():
    tmp = Ggrequests(random_text('cid_'), random_text('req_'), random_text('cnt_'), random_lang(), mockupip(), random_text('hw_'), random_text('pub_'), False, fixed_Ad_Units())
    result = json.loads(json.dumps(tmp, cls=CustomEncoder))
    return result

current_line = 0

def mockupip():    
    global current_line

    with open("/mnt/locust/geoip.csv", mode='r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        lines = list(reader)

        if current_line < len(lines):
            next_line = lines[current_line][0]
            current_line += 1
            return str(next_line)
        else:
            return None
        

if __name__ == '__main__':
    # 创建对象示例
    # size1 = Size(300, 250)
    # size2 = Size(728, 90)
    # ad_unit1 = Ad_Unit(1, True, 'ad_code_1', [size1, size2])
    # ad_unit2 = Ad_Unit(2, False, 'ad_code_2', [size1])
    # gg_request = Ggrequests(random_text(), random_text(), random_text(), random_lang(), random_text(), random_text(), random_text(), [ad_unit1, ad_unit2])
    # ads = generate_random_ggrequest_body()

    # json = json.dumps(ads, cls=CustomEncoder)
    # print(json)

    # 将对象转换为 JSON 字符串
    ip = mockupip()
    ip2 = mockupip()
    print(ip, ip2)