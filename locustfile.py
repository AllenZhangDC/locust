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
        wait_time = constant_throughput(1)
        probability = 0.6
        cid = random_text()
        cnt_id = random_text()
        req_id = random_text()
        lang = random_lang()
        mockup_ip = mockupip()
        with self.client.get(url="/getone", params={"cid":cid, "cnt_id":cnt_id, "req_id":req_id, "lang":lang, "mockup_ip":mockup_ip},  name=name, catch_response=True) as resp:
            code = resp.status_code
            if code == 200:
                logging.info("01 Getone: " + str(code) + " cid:" + cid + " cnt_id:" + cnt_id + " req_id:"+req_id+" lang:"+lang+" mockup_ip:"+mockup_ip)
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
                    gevent.sleep(1)
                    self.client.get(url=self.Impression, name="01.1 Getone: Impression")
                    logging.info("01Getone1: Impression "+self.Impression)
                    if(decision(probability)):
                        gevent.sleep(4)
                        self.client.get(url=self.Skip, name="01.2 Getone: Skip")
                        logging.info("01Getone2: Skip "+self.Skip)
                        if(decision(probability)):
                            gevent.sleep(7)
                            self.client.get(url=self.FirstQuartile, name="01.4 Getone: FirstQuartile")
                            logging.info("01Getone4: FirstQuartile "+self.FirstQuart)
                            gevent.sleep(3)
                            self.client.get(url=self.Progress, name="01.3 Getone: Progress")
                            logging.info("01Getone3: Progress "+self.Progress)  
                            if(decision(probability)):
                                gevent.sleep(7)
                                self.client.get(url=self.Midpoint, name = "01.5 Getone: Midpoint")
                                logging.info("01Getone5: Midpoint "+self.Midpoint)
                                if(decision(probability)):
                                    gevent.sleep(7)
                                    self.client.get(url=self.ThirdQuartile, name = "01.6 Getone: ThirdQuartile")
                                    logging.info("01Getone6: ThirdQuartile "+self.ThirdQuart)
                                    if(decision(probability)):
                                        gevent.sleep(7)
                                        self.client.get(url=self.Complete, name = "01.7 Getone: Complete")
                                        logging.info("01Getone7: Complete "+self.Complete)
                                        self.client.get(url=self.ClickTracking, name = "01.8 Getone: ClickTracking", allow_redirects=False)
                                        logging.info("01Getone8: ClickTracking " + self.ClickTracking)
                else:
                    resp.failure("is_404: True. NoAdsReason: " + json_data["data"]["no_ad_reason"])
                    logging.warning("Getone: " + str(code) + " cid:" + cid + " cnt_id:" + cnt_id + " req_id:"+req_id+" lang:"+lang+" mockup_ip:"+mockup_ip + "is_404: True. NoAdsReason: " + json_data["data"]["no_ad_reason"])
            else:
                resp.failure("Return code: " + str(resp.status_code) + resp.url)
        logging.info("Getone: Done")

class BannerUser(FastHttpUser):
    host = host_banner_east
    wait_time = constant_throughput(1)
    
    @task
    def get_ggv2_banner(self, name="02 GetGGV2 Banner"):
        probability = 0.6
        json_body = generate_random_ggrequest_body_Banner()
        resp = self.client.post(url="/getggv2", json = json_body, name=name) 
        logging.info("02 Banner: " + str(resp.status_code) + " req: " + str(json_body))
        if resp.status_code == 200:  
            json_result = resp.json()
            for each in json_result["data"]:
                if(json_result["data"][each]["is_404"] == False):
                    if(json_result["data"][each]["impURL"] != ""):
                        # Banner is 100% Impression. Frontend do Impression callbacks once it received response.
                        self.client.get(url=json_result["data"][each]["impURL"], name="02.1 Banner: Impression")
                        logging.info("02 Banner: Impression " + json_result["data"][each]["impURL"])
                        time.sleep(1)
                        if(decision(probability) and json_result["data"][each]["viewableImpURL"] != ""):
                            time.sleep(1)
                            self.client.get(url=json_result["data"][each]["viewableImpURL"], name="02.2 Banner: Viewable")
                            logging.info("02 Banner: Viewable " + json_result["data"][each]["viewableImpURL"])
                            if(decision(probability) and json_result["data"][each]["clickURL"] != ""):
                                time.sleep(1)
                                self.client.get(url=json_result["data"][each]["clickURL"], name="02.3 Banner: Click", allow_redirects=False)
                                logging.info("02 Banner: Click " + json_result["data"][each]["clickURL"])
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
                    # short banner ads, 100% impression
                    if(json_result["data"][each]["html"] != ""):
                        if("impURL" in json_result["data"][each]):
                            self.client.get(url=json_result["data"][each]["impURL"], name= "03.1.1 Shorts-Banner: Impression")
                            if(decision(probability)):
                                self.client.get(url=json_result["data"][each]["viewableImpURL"], name= "03.1.2 Shorts-Banner: Viewable")
                                if(decision(probability)):
                                    click_url = json_result["data"][each]["clickURL"]
                                    self.client.get(click_url, name = "03.1.3 Shorts-Banner: Click", allow_redirects=False)
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
                            gevent.sleep(1)
                            self.client.get(url=self.Impression, name="03.2.1 Shorts: Impression")
                            if(decision(probability)):
                                gevent.sleep(4)
                                self.client.get(url=self.Skip, name="03.2.2 Shorts: Skip")
                                if(decision(probability)):
                                    gevent.sleep(10)
                                    self.client.get(url=self.Progress, name="03.2.3 Shorts:Progress")
                                    self.client.get(url=self.FirstQuartile, name="03.2.4 Shorts:FirstQuartile")
                                    if(decision(probability)):
                                        gevent.sleep(15)
                                        self.client.get(url=self.Midpoint, name="03.2.5 Shorts:Midpoint")
                                        if(decision(probability)):
                                            gevent.sleep(10)
                                            self.client.get(url=self.ThirdQuartile, name="03.2.6 Shorts:ThirdQuartile")
                                            if(decision(probability)):
                                                gevent.sleep(15)
                                                self.client.get(url=self.Complete, name="03.2.7 Shorts:Complete")
                                                self.client.get(url=self.ClickTracking, name="03.2.8 Shorts:Clicck")
                else:
                    resp.failure_message = json_result["data"][each]["no_ad_reason"]


if __name__ == "__main__":
    # my_env = Environment(user_classes=[GetGGV2_Banner_East])
    # GetGGV2_Banner_East(my_env).run()
    run_single_user(BannerUser)


