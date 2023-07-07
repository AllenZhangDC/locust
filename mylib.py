import json
import random
import string

def random_text(prefix=''):
    letters = string.ascii_letters
    result = ''.join(random.choice(letters) for _ in range(8))
    return prefix+result

def random_lang():
    return random.choice(['zh-CN', 'zh-TW', 'ja-JP', 'ko-KR', 'de-DE', 'es-ES', 'fr-FR', 'it-IT', 'ru-RU', 'vi-VN'])

def random_zone():
    return random.choice(['z_v_r_r_1', 'z_v_r_b_2', 'z_a_b_1', 'z_a_c_1', 'z_a_c_2'])

def decision(probability):
    return random.random() < probability

def random_int():
    return random.randint(1, 4)

def random_position():
    return random.randint(4, 8)
