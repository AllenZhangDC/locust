import time, json, base64, random, string, logging, random,json, gevent.monkey
from mylib import *
from Ggrequest import *
import xml.etree.ElementTree as ET
from locust import *
from locust.env import Environment

gevent.monkey.patch_all()

jsonstr = '{"cid": "cid_BzanIxIY", "req_id": "req_OssjLsTY", "cnt_id": "cnt_CmpgXijc", "lang": "ja-JP", "nw_id": "hw_nRWEXUCl", "pub_id": "pub_RQBbzrAB", "more_info": false, "ad_units": [{"no": 1, "hrc": "hrc_FTdCiVYc", "code": "z_v_r_b_2", "dy_id": 5, "sizes": [{"w": 300, "h": 250}]}, {"no": 2, "hrc": "hrc_YBaLEncJ", "code": "z_a_c_2", "dy_id": 8, "sizes": [{"w": 900, "h": 112}]}, {"no": 3, "hrc": "hrc_bsJZrNVa", "code": "shorts", "dy_id": 5, "sizes": [{"w": 200, "h": 800}]}, {"no": 4, "hrc": "hrc_UthSHBPw", "code": "shorts", "dy_id": 6, "sizes": [{"w": 200, "h": 800}]}]}'

class Single_Getone(HttpUser):
    host = "https://loadtest.dev.ganjing.world/v1/cdkapi"
    wait_time = between(5, 10)
    probability = 0.6
    @task
    def get_onev2(self):
        with self.client.get(url="/getone", params={"cid":random_text(), "cnt_id":random_text(), "req_id":random_text(), "lang":random_lang(), "mockup_ip":mockupip()}, catch_response=True, name="Single_Getone_get") as resp:
            code = resp.status_code
            if code == 200:
                json_data = json.loads(resp.text)
                if json_data["data"]["is_404"] == True:
                    resp.failure("is_404: True. NoAdsReason: " + json_data["data"]["no_ad_reason"])
                else:
                    pass
                    # xml = base64.b64decode(json_data["data"]["xml"])
                    # self.Impression = ET.fromstring(xml).findall(".//Impression")[1].text
            else:
                resp.failure("Return code: " + resp.status_code + resp.url)
        

class Single_GetGGV2_Post(HttpUser):
    host = "https://loadtest.dev.ganjing.world/v1/cdkapi"
    wait_time = between(1, 10)
    @task
    def get_ggv2(self):
        json_body = generate_random_ggrequest_body()
        resp = self.client.post(url="http://loadtest.dev.ganjing.world/v1/cdkapi/getggv2", json = json_body, name="Single_Getggv2_post")
        if resp.status_code == 200:
            json_var = resp.json()

class Getone_With_Callback(HttpUser):
    host = "https://loadtest.dev.ganjing.world/v1/cdkapi"
    wait_time = between(5, 10)
    @task
    def get_onev2(self):
        probability = 1.0
        with self.client.get(url="/getone", params={"cid":random_text(), "cnt_id":random_text(), "req_id":random_text(), "lang":random_lang(), "mockup_ip":mockupip()},  name="Single_Getone_get",catch_response=True) as resp:
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
                        self.client.get(url=self.Impression, name="Getone callback: Impression")
                        if(decision(probability)):
                            self.client.get(url=self.Skip, name="Getone callback: Skip")
                            if(decision(probability)):
                                self.client.get(url=self.Progress, name="Getone callback: Progress")
                                if(decision(probability)):
                                    self.client.get(url=self.FirstQuartile, name="Getone callback: FirstQuartile")
                                    if(decision(probability)):
                                        self.client.get(url=self.Midpoint, name="Getone callback: Midpoint")
                                        if(decision(probability)):
                                            self.client.get(url=self.ThirdQuartile, name="Getone callback: ThirdQuartile")
                                            if(decision(probability)):
                                                self.client.get(url=self.Complete, name="Getone callback: ThirdQuartile")
                                                if(decision(probability)):
                                                    self.client.get(url=self.Complete, name="Getone callback: Complete")
                                                    self.client.get(url=self.ClickTracking, name="Getone callback: ClickTracking")
                else:
                    resp.failure("is_404: True. NoAdsReason: " + json_data["data"]["no_ad_reason"])
 
class GetGGV2_With_Callback(HttpUser):
    host = "https://loadtest.dev.ganjing.world/v1/cdkapi"
    wait_time = between(1, 10)
    @task
    def get_ggv2(self):
        json_body = generate_random_ggrequest_body2()
        jsonstr = json.dumps(json_body)
        resp = self.client.post(url="http://loadtest.dev.ganjing.world/v1/cdkapi/getggv2", json = json_body, name="Single_Getggv2_post")
        if resp.status_code == 200:
            json_result = resp.json()
            implist = list()
            viewlist = list()

            imp01 = json_result["data"]["gjw-0-1"]["impURL"]
            if(imp01 == ""):
                resp.failure_message = json_result["data"]["gjw-0-1"]["no_ad_reason"]
            else:
                implist.append(imp01)
            
            imp02 = json_result["data"]["gjw-0-2"]["impURL"]
            if(imp02 == ""):
                resp.failure_message = json_result["data"]["gjw-0-2"]["no_ad_reason"]
            else:
                implist.append(imp02)

            imp03 = json_result["data"]["gjw-0-3"]["impURL"]
            if(imp03 == ""):
                resp.failure_message = json_result["data"]["gjw-0-3"]["no_ad_reason"]
            else:
                implist.append(imp03)

            imp04 = json_result["data"]["gjw-0-4"]["impURL"]
            if(imp04 == ""):
                resp.failure_message = json_result["data"]["gjw-0-4"]["no_ad_reason"]
            else:
                implist.append(imp04)

            imp05 = json_result["data"]["gjw-0-5"]["impURL"]
            if(imp05 == ""):
                resp.failure_message = json_result["data"]["gjw-0-5"]["no_ad_reason"]
            else:
                implist.append(imp05)

            view1 = json_result["data"]["gjw-0-1"]["viewableImpURL"]
            if(view1 == ""):
                resp.failure_message = json_result["data"]["gjw-0-1"]["no_ad_reason"]
            else:
                viewlist.append(view1)

            view2 = json_result["data"]["gjw-0-3"]["viewableImpURL"]
            if(view2 == ""):
                resp.failure_message = json_result["data"]["gjw-0-3"]["no_ad_reason"]
            else:
                viewlist.append(view2)
            click1 = json_result["data"]["gjw-0-3"]["clickURL"]
            if(click1 == ""):
                resp.failure_message = json_result["data"]["gjw-0-3"]["no_ad_reason"]
            else:
                self.client.get(click1, name="Getggv2 callback: Click")
            
            self.make_call_backs(implist,   "Getggv2 callback: Impression")
            self.make_call_backs(viewlist,  "Getggv2 callback: View")
            
    def make_call_backs(self, callbacklist, name):
        for url in callbacklist:
                resp = self.client.get(url, name=name)
                if resp.status_code == 200:
                    json_data = json.loads(resp.text)
                    if json_data["status"] != 200:
                        resp.failure(json_data)
                    else:
                        pass
                else:
                    pass



if __name__ == "__main__":
    my_env = Environment(user_classes=[Getone_With_Callback])
    Getone_With_Callback(my_env).run()
