import requests
r = requests.post( 'http://loadtest.dev.ganjing.world/v1/cdkapi/getggv2', json={
"cid": "cid_BzanIxIY", "req_id": "req_OssjLsTY", "cnt_id": "cnt_CmpgXijc", "lang": "ja-JP", "nw_id": "hw_nRWEXUCl", "pub_id": "pub_RQBbzrAB", "more_info": False, "ad_units": [{"no": 1, "hrc": "hrc_FTdCiVYc", "code": "z_v_r_b_2", "dy_id": 5, "sizes": [{"w": 300, "h": 250}]}, {"no": 2, "hrc": "hrc_YBaLEncJ", "code": "z_a_c_2", "dy_id": 8, "sizes": [{"w": 900, "h": 112}]}, {"no": 3, "hrc": "hrc_bsJZrNVa", "code": "shorts", "dy_id": 5, "sizes": [{"w": 200, "h": 800}]}, {"no": 4, "hrc": "hrc_UthSHBPw", "code": "shorts", "dy_id": 6, "sizes": [{"w": 200, "h": 800}]}]}
)
print(f"Status Code: {r.status_code}, Response: {r.json()}")