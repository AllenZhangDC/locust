import time, json, base64, random, string, logging, random,json, gevent, requests
from locust import HttpUser, task, run_single_user
from mylib import *
from Ggrequest import *
import xml.etree.ElementTree as ET
from locust import *
from locust.env import Environment

#gevent.monkey.patch_all()

jsonstr = '{"cid": "cid_BzanIxIY", "req_id": "req_OssjLsTY", "cnt_id": "cnt_CmpgXijc", "lang": "ja-JP", "nw_id": "hw_nRWEXUCl", "pub_id": "pub_RQBbzrAB", "more_info": false, "ad_units": [{"no": 1, "hrc": "hrc_FTdCiVYc", "code": "z_v_r_b_2", "dy_id": 5, "sizes": [{"w": 300, "h": 250}]}, {"no": 2, "hrc": "hrc_YBaLEncJ", "code": "z_a_c_2", "dy_id": 8, "sizes": [{"w": 900, "h": 112}]}, {"no": 3, "hrc": "hrc_bsJZrNVa", "code": "shorts", "dy_id": 5, "sizes": [{"w": 200, "h": 800}]}, {"no": 4, "hrc": "hrc_UthSHBPw", "code": "shorts", "dy_id": 6, "sizes": [{"w": 200, "h": 800}]}]}'
host_load = "https://loadtest.dev.ganjing.world/v1/cdkapi"
host_video_east = host_load #"https://fg.dev.ganjing.world/v1/cdkapi" #host_load
host_banner_east =  host_load #"https://bs.dev.ganjing.world/v1/cdkapi" #host_load



class VideoUser(FastHttpUser):
    host = host_video_east
    wait_time = constant_throughput(1)
    @task
    def get_one(self, name="01 Getone"):
        probability = 0.6
        with self.client.get(url="/getone", params={"cid":random_text(), "cnt_id":random_text(), "req_id":random_text(), "lang":random_lang(), "mockup_ip":mockupip()},  name=name, catch_response=True) as resp:
            code = resp.status_code
            if code == 200:
                json_data = json.loads(resp.text)
                if json_data["data"]["is_404"] == False:
                    xml = base64.b64decode(json_data["data"]["xml"])
                    self.Impression = ET.fromstring(xml).findall(".//Impression")[1].text
                    self.Skip = ET.fromstring(xml).findall(".//*[@event='skip']")[1].text
                    self.Progress = ET.fromstring(xml).findall(".//*[@event='progress']")[1].text
                    self.FirstQuartile = ET.fromstring(xml).findall(".//*[@event='firstQuartile']")[1].text
                    self.Midpoint = ET.fromstring(xml).findall(".//*[@event='midpoint']")[1].text
                    self.ThirdQuartile = ET.fromstring(xml).findall(".//*[@event='thirdQuartile']")[1].text
                    self.Complete = ET.fromstring(xml).findall(".//*[@event='complete']")[1].text
                    self.ClickTracking = ET.fromstring(xml).findall(".//ClickTracking")[0].text
                    if(decision(probability)):
                        requests.get(url=self.Impression)
                        if(decision(probability)):
                            gevent.sleep(5)
                            requests.get(url=self.Skip)
                            if(decision(probability)):
                                gevent.sleep(5)
                                requests.get(url=self.Progress)
                                if(decision(probability)):
                                    requests.get(url=self.FirstQuartile)
                                    if(decision(probability)):
                                        gevent.sleep(5)
                                        requests.get(url=self.Midpoint)
                                        if(decision(probability)):
                                            gevent.sleep(5)
                                            requests.get(url=self.ThirdQuartile)
                                            if(decision(probability)):
                                                gevent.sleep(5)
                                                requests.get(url=self.Complete)
                                                requests.get(url=self.ClickTracking)
                else:
                    resp.failure("is_404: True. NoAdsReason: " + json_data["data"]["no_ad_reason"])
            else:
                resp.failure("Return code: " + str(resp.status_code) + resp.url)

class BannerUser(FastHttpUser):
    host = host_banner_east
    wait_time = constant_throughput(1)
    
    @task
    def get_ggv2_banner(self, name="02 GetGGV2 Banner"):
        probability = 0.6
        json_body = generate_random_ggrequest_body_Banner()
        resp = self.client.post(url="/getggv2", json = json_body, name=name) 
        if resp.status_code == 200:  
            json_result = resp.json()
            for each in json_result["data"]:
                if(json_result["data"][each]["is_404"] == False):
                    if(json_result["data"][each]["impURL"] != ""):
                        requests.get(url=json_result["data"][each]["impURL"])
                        time.sleep(1)
                        if(decision(probability) and json_result["data"][each]["viewableImpURL"] != ""):
                            time.sleep(1)
                            requests.get(url=json_result["data"][each]["viewableImpURL"])
                            if(decision(probability) and json_result["data"][each]["clickURL"] != ""):
                                time.sleep(1)
                                requests.get(url=json_result["data"][each]["clickURL"])
                else:
                    resp.failure_message = json_result["data"][each]["no_ad_reason"]
        else:
            resp.failure_message = "Return code is: " + resp.status_code



class ShortsUser(FastHttpUser):
    host = host_banner_east
    wait_time = constant_throughput(1)
    @task
    def get_ggv2_shorts(self, name="03 GetGGV2 Shorts"):
        probability = 0.6
        json_body = generate_random_ggrequest_body_Shorts()
        resp = self.client.post(url="/getggv2", json = json_body, name=name) 
        if resp.status_code == 200:
            json_result = resp.json()
          
            for each in json_result["data"]:
                if(json_result["data"][each]["is_404"] == False):
                    # short banner ads
                    if(json_result["data"][each]["html"] != ""):
                        if("impURL" in json_result["data"][each]):
                            requests.get(url=json_result["data"][each]["impURL"])
                            if(decision(probability)):
                                requests.get(url=json_result["data"][each]["viewableImpURL"])
                                if(decision(probability)):
                                    click_url = json_result["data"][each]["clickURL"]
                                    requests.get(click_url)
                    # short video ads
                    else:
                        xml = base64.b64decode(json_result["data"][each]["xml"])
                        self.Impression = ET.fromstring(xml).findall(".//Impression")[1].text
                        self.Skip = ET.fromstring(xml).findall(".//*[@event='skip']")[1].text
                        self.Progress = ET.fromstring(xml).findall(".//*[@event='progress']")[1].text
                        self.FirstQuartile = ET.fromstring(xml).findall(".//*[@event='firstQuartile']")[1].text
                        self.Midpoint = ET.fromstring(xml).findall(".//*[@event='midpoint']")[1].text
                        self.ThirdQuartile = ET.fromstring(xml).findall(".//*[@event='thirdQuartile']")[1].text
                        self.Complete = ET.fromstring(xml).findall(".//*[@event='complete']")[1].text
                        self.ClickTracking = ET.fromstring(xml).findall(".//ClickTracking")[0].text
                        if(decision(probability)):
                            requests.get(url=self.Impression)
                            if(decision(probability)):
                                gevent.sleep(5)
                                requests.get(url=self.Skip)
                                if(decision(probability)):
                                    gevent.sleep(5)
                                    requests.get(url=self.Progress)
                                    if(decision(probability)):
                                        requests.get(url=self.FirstQuartile)
                                        if(decision(probability)):
                                            gevent.sleep(5)
                                            requests.get(url=self.Midpoint)
                                            if(decision(probability)):
                                                gevent.sleep(5)
                                                requests.get(url=self.ThirdQuartile)
                                                if(decision(probability)):
                                                    gevent.sleep(5)
                                                    requests.get(url=self.Complete)
                                                if(decision(random.random())):
                                                    requests.get(url=self.ClickTracking)
                else:
                    resp.failure_message = json_result["data"][each]["no_ad_reason"]



class VideoUser_Callback(FastHttpUser):
    host = host_video_east
    wait_time = constant_throughput(1)
    @task
    def get_one_with_callback(self, name="01 Getone"):
        probability = 0.6
        with self.client.get(url="/getone", params={"cid":random_text(), "cnt_id":random_text(), "req_id":random_text(), "lang":random_lang(), "mockup_ip":mockupip()},  name=name, catch_response=True) as resp:
            code = resp.status_code
            if code == 200:
                json_data = json.loads(resp.text)
                if json_data["data"]["is_404"] == False:
                    xml = base64.b64decode(json_data["data"]["xml"])
                    self.Impression = ET.fromstring(xml).findall(".//Impression")[1].text
                    self.Skip = ET.fromstring(xml).findall(".//*[@event='skip']")[1].text
                    self.Progress = ET.fromstring(xml).findall(".//*[@event='progress']")[1].text
                    self.FirstQuartile = ET.fromstring(xml).findall(".//*[@event='firstQuartile']")[1].text
                    self.Midpoint = ET.fromstring(xml).findall(".//*[@event='midpoint']")[1].text
                    self.ThirdQuartile = ET.fromstring(xml).findall(".//*[@event='thirdQuartile']")[1].text
                    self.Complete = ET.fromstring(xml).findall(".//*[@event='complete']")[1].text
                    self.ClickTracking = ET.fromstring(xml).findall(".//ClickTracking")[0].text
                    if(decision(probability)):
                        self.client.get(url=self.Impression, name= "01.1 Getone: Impression")
                        if(decision(probability)):
                            gevent.sleep(5)
                            self.client.get(url=self.Skip, name= "01.2 Getone: Skip")
                            if(decision(probability)):
                                gevent.sleep(5)
                                self.client.get(url=self.Progress, name="01.3 Getone: Progress")
                                if(decision(probability)):
                                    self.client.get(url=self.FirstQuartile, name="01.4 Getone: FirstQuartile")
                                    if(decision(probability)):
                                        gevent.sleep(5)
                                        self.client.get(url=self.Midpoint, name="01.5 Getone: Midpoint")
                                        if(decision(probability)):
                                            gevent.sleep(5)
                                            self.client.get(url=self.ThirdQuartile, name="01.6 Getone: ThirdQuartile")
                                            if(decision(probability)):
                                                gevent.sleep(5)
                                                self.client.get(url=self.Complete, name="01.7 Getone: Complete")
                                                self.client.get(url=self.ClickTracking, name="01.8 Getone: ClickTracking", allow_redirects=False)
                else:
                    resp.failure_message = "is_404: True. NoAdsReason: " + json_data["data"]["no_ad_reason"]
            else:
                resp.failure_message = "Return code: " + str(resp.status_code) + resp.url




class BannerUser_Callback(FastHttpUser):
    host = host_banner_east
    wait_time = constant_throughput(1) #between(0, 1)
    @task
    def get_ggv2(self, name="02 GetGGV2 Banner"):
        json_body = generate_random_ggrequest_body_Banner()
        jsonstr = json.dumps(json_body)
        resp = self.client.post(url="/getggv2", json = json_body, name=name) 
        if resp.status_code == 200:  
            json_result = resp.json()
            for each in json_result["data"]:
                if(json_result["data"][each]["is_404"] == False):
                    if(json_result["data"][each]["impURL"] != ""):
                        self.client.get(url=json_result["data"][each]["impURL"], name="02.1 Banner: Impression")
                        time.sleep(1)
                        if(decision(0.8) and json_result["data"][each]["viewableImpURL"] != ""):
                            time.sleep(1)
                            self.client.get(url=json_result["data"][each]["viewableImpURL"], name="02.2 Banner: Viewable Impression")
                            if(decision(random.random()) and json_result["data"][each]["clickURL"] != ""):
                                time.sleep(1)
                                self.client.get(url=json_result["data"][each]["clickURL"], name="02.3 Banner: Click", allow_redirects=False)
                else:
                    resp.failure_message = json_result["data"][each]["no_ad_reason"]
        else:
            resp.failure_message = "Return code is: " + str(resp.status_code) + resp.status_message + resp.url

            


class ShortsUser_Callback(FastHttpUser):
    host = host_load
    wait_time = constant_throughput(1)
    @task
    def get_ggv2(self, name="03 GetGGV2 Shorts"):
        probability = 0.6
        json_body = generate_random_ggrequest_body_Shorts()
        jsonstr = json.dumps(json_body)
        resp = self.client.post(url="/getggv2", json = json_body, name=name) 
        if resp.status_code == 200:
            json_result = resp.json()
          
            for each in json_result["data"]:
                if(json_result["data"][each]["is_404"] == False):
                    # short banner ads
                    if(json_result["data"][each]["html"] != ""):
                        if("impURL" in json_result["data"][each]):
                            self.client.get(url=json_result["data"][each]["impURL"], name="03.1.1 Shorts-Banner: Impression")
                            if(decision(probability)):
                                self.client.get(url=json_result["data"][each]["viewableImpURL"], name="03.1.2 Shorts-Banner: View")
                                if(decision(random.random())):
                                    click_url = json_result["data"][each]["clickURL"]
                                    self.client.get(click_url, name="03.1.3 Shorts-Banner: Click", allow_redirects=False)
                    # short video ads
                    else:
                        xml = base64.b64decode(json_result["data"][each]["xml"])
                        self.Impression = ET.fromstring(xml).findall(".//Impression")[1].text
                        self.Skip = ET.fromstring(xml).findall(".//*[@event='skip']")[1].text
                        self.Progress = ET.fromstring(xml).findall(".//*[@event='progress']")[1].text
                        self.FirstQuartile = ET.fromstring(xml).findall(".//*[@event='firstQuartile']")[1].text
                        self.Midpoint = ET.fromstring(xml).findall(".//*[@event='midpoint']")[1].text
                        self.ThirdQuartile = ET.fromstring(xml).findall(".//*[@event='thirdQuartile']")[1].text
                        self.Complete = ET.fromstring(xml).findall(".//*[@event='complete']")[1].text
                        self.ClickTracking = ET.fromstring(xml).findall(".//ClickTracking")[0].text
                        if(decision(probability)):
                            self.client.get(url=self.Impression, name= "03.2.1 Shorts-Video: Impression")
                            if(decision(probability)):
                                gevent.sleep(5)
                                self.client.get(url=self.Skip, name= "03.2.2 Shorts-Video: Skip")
                                if(decision(probability)):
                                    gevent.sleep(5)
                                    self.client.get(url=self.Progress, name="03.2.3 Shorts-Video: Progress")
                                    if(decision(probability)):
                                        self.client.get(url=self.FirstQuartile, name="03.2.4 Shorts-Video: FirstQuartile")
                                        if(decision(probability)):
                                            gevent.sleep(5)
                                            self.client.get(url=self.Midpoint, name="03.2.5 Shorts-Video: Midpoint")
                                            if(decision(probability)):
                                                gevent.sleep(5)
                                                self.client.get(url=self.ThirdQuartile, name="03.2.6 Shorts-Video: ThirdQuartile")
                                                if(decision(random.random())):
                                                    gevent.sleep(5)
                                                    self.client.get(url=self.Complete, name="03.2.7 Shorts-Video: Complete")
                                        if(decision(random.random())):
                                            self.client.get(url=self.ClickTracking, name="03.2.8 Shorts-Video: ClickTracking", allow_redirects=True)
                                                    
                else:
                    resp.failure_message = json_result["data"][each]["no_ad_reason"]


if __name__ == "__main__":
    # my_env = Environment(user_classes=[GetGGV2_Banner_East])
    # GetGGV2_Banner_East(my_env).run()
    run_single_user(BannerUser_Callback)


