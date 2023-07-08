import time, json, base64, random, string, logging, random,json
from urllib import response
from mylib import *
from Ggrequest import *
import xml.etree.ElementTree as ET
from locust import *
from locust.env import Environment


class AdsServer(HttpUser):
    host = "https://loadtest.dev.ganjing.world/v1/cdkapi"
    wait_time = between(0, 1)
    @task
    def get_onev2(self):
        with self.client.get(url="/getonev2", params={"cid":random_text(), "cnt_id":random_text(), "req_id":random_text(), "lang":random_lang()}, catch_response=True) as resp:
            code = resp.status_code
            if code == 200:
                json_data = json.loads(resp.text)
                if json_data["data"]["is_404"] == True:
                    resp.failure("is_404: True. NoAdsReason: " + json_data["data"]["no_ad_reason"])

            # xml = base64.b64decode(json_data["data"]["xml"])
            # self.Impression = ET.fromstring(xml).findall(".//Impression")[1].text
            # self.Skip = ET.fromstring(xml).findall(".//*[@event='skip']")[1].text
            # self.Progress = ET.fromstring(xml).findall(".//*[@event='progress']")[1].text
            # self.FirstQuartile = ET.fromstring(xml).findall(".//*[@event='firstQuartile']")[1].text
            # self.Midpoint = ET.fromstring(xml).findall(".//*[@event='midpoint']")[1].text
            # self.ThirdQuartile = ET.fromstring(xml).findall(".//*[@event='thirdQuartile']")[1].text
            # self.Complete = ET.fromstring(xml).findall(".//*[@event='complete']")[1].text
            # self.ClickTracking = ET.fromstring(xml).findall(".//ClickTracking")[0].text
            #self.random_callback(probability=0.6)

    # @task
    # def get_gg(self):
    #     json_body = generate_random_ggrequest_body()
    #     resp2 = self.client.post(url="/getggv2", json= json_body)
    #     if resp2.status_code == 200:
    #         json_var = resp2.json()
    #         #logging.info(json.loads(resp2.text))


    # def random_callback(self, probability=0.6):
    #     if(decision(probability)):
    #         self.client.get(url=self.Impression)
    #         if(decision(probability)):
    #             self.client.get(url=self.Skip)
    #             if(decision(probability)):
    #                 self.client.get(url=self.Progress)
    #                 if(decision(probability)):
    #                     self.client.get(url=self.FirstQuartile)
    #                     if(decision(probability)):
    #                         self.client.get(url=self.Midpoint)
    #                         if(decision(probability)):
    #                             self.client.get(url=self.ThirdQuartile)
    #                             if(decision(probability)):
    #                                 self.client.get(url=self.Complete)
    #                                 if(decision(probability)):
    #                                     self.client.get(url=self.ClickTracking)
 


if __name__ == "__main__":
    my_env = Environment(user_classes=[AdsServer])
    AdsServer(my_env).run()
