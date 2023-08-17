import time, json, base64, json, gevent
from locust import HttpUser, task, run_single_user
from mylib import *
from Ggrequest import *
import xml.etree.ElementTree as ET
from locust import *


host_load = "https://loadtest.dev.ganjing.world/v1/cdkapi"
host_prod = "https://fg2.dev.ganjing.world/v1/cdkapi" #host_load
host_load = host_load
    
class Video(FastHttpUser):
    host = host_load
    wait_time = constant_throughput(1)
    @task
    def get_video(self):
        with self.client.get(url="/getone", params={"cid":random_text(), "cnt_id":random_text(), "req_id":random_text(), "lang":random_lang(), "mockupip":mockupip()},  name="01 Video", catch_response=True) as resp:
            if resp.status_code == 200:
                json_data = json.loads(resp.text)
                if(json_data["data"]["is_404"] == True):
                    resp.failure("is_404: True. NoAdsReason: " + json_data["data"]["no_ad_reason"])
            # No need to catch exceptions, system will do it.
            # else:
            #     resp.failure("Bad code: " + str(resp.status_code) + resp.url)



class VideoCallbackStress(FastHttpUser):
    host = host_load
    wait_time = constant_throughput(1)
    @task
    def get_one(self, name="01 Video"):
        with self.client.get(url="/getone", params={"cid":random_text(), "cnt_id":random_text(), "req_id":random_text(), "lang":random_lang(), "mockupip":mockupip()},  name=name, catch_response=True) as resp:
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
                    self.client.get(url=self.Impression, name="01.1 Getone: Impression")
                    if(decision(0.6)):
                        self.client.get(url=self.Skip, name="01.2 Getone: Skip")
                        if(decision(0.46)):
                            self.client.get(url=self.Progress, name="01.3 Getone: Progress")
                        if(decision(0.71)):
                            self.client.get(url=self.FirstQuartile, name="01.4 Getone: FirstQuartile")
                            if(decision(0.63)):
                                self.client.get(url=self.Midpoint, name = "01.5 Getone: Midpoint")
                                if(decision(0.83)):
                                    self.client.get(url=self.ThirdQuartile, name = "01.6 Getone: ThirdQuartile")
                                    if(decision(0.87)):
                                        self.client.get(url=self.Complete, name = "01.7 Getone: Complete")
                    if(decision(0.08)):
                        self.client.get(url=self.ClickTracking, name = "01.8 Getone: ClickTracking", allow_redirects=False)
                else:
                    resp.failure("is_404: True. NoAdsReason: " + json_data["data"]["no_ad_reason"])
            # System will do below exceptions
            # else:
            #     resp.failure("Return code: " + str(resp.status_code) + resp.url)

class VideoCallbackReal(FastHttpUser):
    host = host_load
    wait_time = constant_throughput(1)
    @task
    def get_one(self, name="01 Video"):
        with self.client.get(url="/getone", params={"cid":random_text(), "cnt_id":random_text(), "req_id":random_text(), "lang":random_lang(), "mockupip":mockupip()},  name=name, catch_response=True) as resp:
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
                    gevent.sleep(1)
                    self.client.get(url=self.Impression, name="01.1 Getone: Impression")
                    if(decision(0.6)):
                        gevent.sleep(4)
                        self.client.get(url=self.Skip, name="01.2 Getone: Skip")
                        if(decision(0.46)):
                            gevent.sleep(7)
                            self.client.get(url=self.Progress, name="01.3 Getone: Progress")
                        if(decision(0.71)):
                            self.client.get(url=self.FirstQuartile, name="01.4 Getone: FirstQuartile")
                            gevent.sleep(3)
                            if(decision(0.63)):
                                gevent.sleep(7)
                                self.client.get(url=self.Midpoint, name = "01.5 Getone: Midpoint")
                                if(decision(0.83)):
                                    gevent.sleep(7)
                                    self.client.get(url=self.ThirdQuartile, name = "01.6 Getone: ThirdQuartile")
                                    if(decision(0.87)):
                                        gevent.sleep(7)
                                        self.client.get(url=self.Complete, name = "01.7 Getone: Complete")
                    if(decision(0.08)):
                        self.client.get(url=self.ClickTracking, name = "01.8 Getone: ClickTracking", allow_redirects=False)
                else:
                    resp.failure("is_404: True. NoAdsReason: " + json_data["data"]["no_ad_reason"])

class Banner(FastHttpUser):
    host = host_load
    wait_time = constant_throughput(1)
    @task
    def get_ggv2_banner(self, name="02 Banner"):
        probability = 0.6
        json_body = generate_random_ggrequest_body_Banner()
        with self.client.post(url="/getggv2", json = json_body, name=name,  catch_response=True) as resp:
            if resp.status_code == 200:  
                json_result = resp.json()
                for each in json_result["data"]:
                    if(json_result["data"][each]["is_404"] == True):
                        resp.failure("is_404: True. NoAdsReason: " + json_result["data"][each]["no_ad_reason"])


class BannerCallback(FastHttpUser):
    host = host_load
    wait_time = constant_throughput(1)
    
    @task
    def get_ggv2_banner(self, name="02 Banner"):
        json_body = generate_random_ggrequest_body_Banner()
        with self.client.post(url="/getggv2", json = json_body, name=name,  catch_response=True) as resp:
            if resp.status_code == 200:  
                json_result = resp.json()
                for each in json_result["data"]:
                    if(json_result["data"][each]["is_404"] == False):
                        if(json_result["data"][each]["impURL"] != ""):
                            self.client.get(url=json_result["data"][each]["impURL"], name="02.1 Banner: Impression")
                            if(decision(0.33) and json_result["data"][each]["viewableImpURL"] != ""):
                                self.client.get(url=json_result["data"][each]["viewableImpURL"], name="02.2 Banner: Viewable")
                                if(decision(0.007) and json_result["data"][each]["clickURL"] != ""):
                                    self.client.get(url=json_result["data"][each]["clickURL"], name="02.3 Banner: Click", allow_redirects=False)
                    else:
                        resp.failure("is_404: True. NoAdsReason: " + json_result["data"][each]["no_ad_reason"])


class BannerCallbackReal(FastHttpUser):
    host = host_load
    wait_time = constant_throughput(1)
    
    @task
    def get_ggv2_banner(self, name="02 Banner"):
        probability = 0.6
        json_body = generate_random_ggrequest_body_Banner()
        with self.client.post(url="/getggv2", json = json_body, name=name,  catch_response=True) as resp:
            if resp.status_code == 200:  
                json_result = resp.json()
                for each in json_result["data"]:
                    if(json_result["data"][each]["is_404"] == False):
                        if(json_result["data"][each]["impURL"] != ""):
                            self.client.get(url=json_result["data"][each]["impURL"], name="02.1 Banner: Impression")
                            if(decision(0.33) and json_result["data"][each]["viewableImpURL"] != ""):
                                time.sleep(1)
                                self.client.get(url=json_result["data"][each]["viewableImpURL"], name="02.2 Banner: Viewable")
                                if(decision(0.007) and json_result["data"][each]["clickURL"] != ""):
                                    time.sleep(5)
                                    self.client.get(url=json_result["data"][each]["clickURL"], name="02.3 Banner: Click", allow_redirects=False)
                    else:
                        resp.failure("is_404: True. NoAdsReason: " + json_result["data"][each]["no_ad_reason"])



class Shorts(FastHttpUser):
    host = host_load
    wait_time = constant_throughput(1)
    @task
    def get_ggv2_shorts(self, name="03 Shorts"):
        json_body = generate_random_ggrequest_body_Shorts()
        with self.client.post(url="/getggv2", json = json_body, name=name, catch_response=True) as resp:
            if resp.status_code == 200:
                json_result = resp.json()
                for each in json_result["data"]:
                    if(json_result["data"][each]["is_404"] == True):
                        resp.failure("is_404: True. NoAdsReason: " + json_result["data"][each]["no_ad_reason"])

          


class ShortsCallback(FastHttpUser):
    host = host_load
    wait_time = constant_throughput(1)
    @task
    def get_ggv2_shorts(self, name="03 Shorts"):
        probability = 0.6
        json_body = generate_random_ggrequest_body_Shorts()
        with self.client.post(url="/getggv2", json = json_body, name=name, catch_response=True) as resp:
            if resp.status_code == 200:
                json_result = resp.json()
                
                for each in json_result["data"]:
                    if(json_result["data"][each]["is_404"] == False):
                        if(json_result["data"][each]["html"] != ""):
                            if("impURL" in json_result["data"][each]):
                                self.client.get(url=json_result["data"][each]["impURL"], name= "03.1.1 Shorts-Banner: Impression")
                                if(decision(0.33)):
                                    self.client.get(url=json_result["data"][each]["viewableImpURL"], name= "03.1.2 Shorts-Banner: Viewable")
                                    if(decision(0.007)):
                                        click_url = json_result["data"][each]["clickURL"]
                                        self.client.get(click_url, name = "03.1.3 Shorts-Banner: Click", allow_redirects=False)
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
                            if(decision(0.6)):
                                self.client.get(url=self.Skip, name="01.2 Getone: Skip")
                                if(decision(0.46)):
                                    self.client.get(url=self.Progress, name="01.3 Getone: Progress")
                                if(decision(0.71)):
                                    self.client.get(url=self.FirstQuartile, name="01.4 Getone: FirstQuartile")
                                    if(decision(0.63)):
                                        self.client.get(url=self.Midpoint, name = "01.5 Getone: Midpoint")
                                        if(decision(0.83)):
                                            self.client.get(url=self.ThirdQuartile, name = "01.6 Getone: ThirdQuartile")
                                            if(decision(0.87)):
                                                self.client.get(url=self.Complete, name = "01.7 Getone: Complete")
                            if(decision(0.08)):
                                self.client.get(url=self.ClickTracking, name = "01.8 Getone: ClickTracking", allow_redirects=False)
                    else:
                        resp.failure("is_404: True. NoAdsReason: " + json_result["data"][each]["no_ad_reason"] )



class ShortsCallbackReal(FastHttpUser):
    host = host_load
    wait_time = constant_throughput(1)
    @task
    def get_ggv2_shorts(self, name="03 Shorts"):
        probability = 0.6
        json_body = generate_random_ggrequest_body_Shorts()
        with self.client.post(url="/getggv2", json = json_body, name=name, catch_response=True) as resp:
            if resp.status_code == 200:
                json_result = resp.json()
                
                for each in json_result["data"]:
                    if(json_result["data"][each]["is_404"] == False):
                        if(json_result["data"][each]["html"] != ""):
                            if("impURL" in json_result["data"][each]):
                                self.client.get(url=json_result["data"][each]["impURL"], name= "03.1.1 Shorts-Banner: Impression")
                                if(decision(0.33)):
                                    self.client.get(url=json_result["data"][each]["viewableImpURL"], name= "03.1.2 Shorts-Banner: Viewable")
                                    if(decision(0.007)):
                                        click_url = json_result["data"][each]["clickURL"]
                                        self.client.get(click_url, name = "03.1.3 Shorts-Banner: Click", allow_redirects=False)
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
                            gevent.sleep(1)
                            self.client.get(url=self.Impression, name="01.1 Getone: Impression")
                            if(decision(0.6)):
                                gevent.sleep(4)
                                self.client.get(url=self.Skip, name="01.2 Getone: Skip")
                                if(decision(0.46)):
                                    gevent.sleep(7)
                                    self.client.get(url=self.Progress, name="01.3 Getone: Progress")
                                if(decision(0.71)):
                                    self.client.get(url=self.FirstQuartile, name="01.4 Getone: FirstQuartile")
                                    gevent.sleep(3)
                                    if(decision(0.63)):
                                        gevent.sleep(7)
                                        self.client.get(url=self.Midpoint, name = "01.5 Getone: Midpoint")
                                        if(decision(0.83)):
                                            gevent.sleep(7)
                                            self.client.get(url=self.ThirdQuartile, name = "01.6 Getone: ThirdQuartile")
                                            if(decision(0.87)):
                                                gevent.sleep(7)
                                                self.client.get(url=self.Complete, name = "01.7 Getone: Complete")
                            if(decision(0.08)):
                                self.client.get(url=self.ClickTracking, name = "01.8 Getone: ClickTracking", allow_redirects=False)
                    else:
                        resp.failure("is_404: True. NoAdsReason: " + json_result["data"][each]["no_ad_reason"] )


if __name__ == "__main__":
    run_single_user(Shorts)
