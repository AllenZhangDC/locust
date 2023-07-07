import time
from locust import HttpUser, task, between


client = HttpUser()
client.host = "https://loadtest.dev.ganjing.world"
resp = client.client.get(url="/v1/cdkapi/getonev2", params={"cid":"afasf", "cnt_id":"afasf", "req_id":"afasf", "lang":"zh-CN"})

