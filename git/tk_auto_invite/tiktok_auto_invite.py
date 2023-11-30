import requests
from selenium import webdriver
import time
import tkinter as tk
from tkinter import messagebox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from datetime import datetime


def alert_(name):
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    messagebox.showinfo(f"继续", f"登陆{name}成功后再点击OK")

def get_text(txtfile):
    with open(txtfile, 'r') as file:
        r=file.read()
    r=[i for i in r.split("\n") if i]
    return r
def get_json(jsonfile):
    with open(jsonfile, 'r') as file:
        data = json.load(file)
    return data


class GETCOOKIES():
    def __init__(self, users):
        self.cookies = {}
        self.users = users


    def login(self):
        # 创建多个Chrome实例，并为每个实例设置不同的用户数据目录
        for profile in self.users:
            options = webdriver.ChromeOptions()
            options.add_argument(f"user-data-dir=profiles/{profile['name']}")
            driver = webdriver.Chrome(options=options)
            # 打开登陆界面插件页面
            driver.get("https://affiliate-us.tiktok.com/platform/homepage?shop_region=US")
            try:
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, "//*[text()='Affiliate Center']"))
                )
                self.cookies[profile['name']] = self.get_cookie(drivers=driver)
                continue
            except:
                print(f"{profile['name']}未登陆,请登陆。")
            driver.find_element(by=By.XPATH, value="//input[@id='TikTok_Ads_SSO_Login_Email_Input']").send_keys(
                profile["name"])
            driver.find_element(by=By.XPATH, value="//*[text()='Affiliate Center']")
            driver.find_element(by=By.XPATH, value="//input[@id='TikTok_Ads_SSO_Login_Pwd_Input']").send_keys(
                profile["password"])
            driver.find_element(by=By.XPATH, value="//button[@id='TikTok_Ads_SSO_Login_Btn']").click()
            alert_()
            self.cookies[profile['name']] = self.get_cookie(drivers=driver)

    def get_cookie(self, drivers):
        selenium_cookies = drivers.get_cookies()
        cookies = {}
        for cookie in selenium_cookies:
            cookies[cookie['name']] = cookie['value']
        drivers.quit()
        return cookies

    def write_cookie(self):
        with open('account.json', "w", encoding="utf-8") as f:
            json.dump(self.cookies, f)


    def run(self):
        self.login()
        # self.write_cookie()


class GETCREATEID():
    def __init__(self, cookies):
        self.cookies = cookies
        self.products = {}
        self.init_headers()
        self.hs=hs


    def init_headers(self):
        self.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "content-length": "172",
            "content-type": "application/json",
            # "cookie": "cookie-consent={%22ga%22:true%2C%22af%22:true%2C%22fbp%22:true%2C%22lip%22:true%2C%22bing%22:true%2C%22ttads%22:true%2C%22reddit%22:true%2C%22criteo%22:true%2C%22version%22:%22v9%22}; sid_guard=edbd7bee139d3e4f56837a00932f8e85%7C1683538826%7C15552000%7CSat%2C+04-Nov-2023+09%3A40%3A26+GMT; _m4b_theme_=new; passport_csrf_token=2dd3373f66a6bad97f29ae0207319a9c; passport_csrf_token_default=2dd3373f66a6bad97f29ae0207319a9c; _ga=GA1.1.637479335.1700718455; _fbp=fb.1.1700718461433.1331967344; _tt_enable_cookie=1; d_ticket_ads=d1b9b2a88b70d54d5cb2400b5d9feaa499043; sso_auth_status_ads=23d8f4a2d4b00b991fbbde6c9f3cb683; sso_auth_status_ss_ads=23d8f4a2d4b00b991fbbde6c9f3cb683; sso_uid_tt_ads=68c8ba05e2ce4039416ccbcf9b9d616a971bccf5c62f967c98df6ffb0ce31e2b; sso_uid_tt_ss_ads=68c8ba05e2ce4039416ccbcf9b9d616a971bccf5c62f967c98df6ffb0ce31e2b; sso_user_ads=3943bcdb0b6bd1ef598d15eff4573b93; sso_user_ss_ads=3943bcdb0b6bd1ef598d15eff4573b93; sid_ucp_sso_v1_ads=1.0.0-KDcxNDZkMDMzMDA5NzAxOThiMDNiZGU0OGJmMzE2Y2E4ZThhZjI4YjcKIAiFiOLI1-6ZkWUQ-8_7qgYY5B8gDDCWz4mpBjgBQOsHEAMaA3NnMSIgMzk0M2JjZGIwYjZiZDFlZjU5OGQxNWVmZjQ1NzNiOTM; ssid_ucp_sso_v1_ads=1.0.0-KDcxNDZkMDMzMDA5NzAxOThiMDNiZGU0OGJmMzE2Y2E4ZThhZjI4YjcKIAiFiOLI1-6ZkWUQ-8_7qgYY5B8gDDCWz4mpBjgBQOsHEAMaA3NnMSIgMzk0M2JjZGIwYjZiZDFlZjU5OGQxNWVmZjQ1NzNiOTM; sid_guard_tiktokseller=8b71f445c040834b72e06540c59d35c1%7C1700718588%7C863998%7CSun%2C+03-Dec-2023+05%3A49%3A46+GMT; uid_tt_tiktokseller=65369c170ac74dd19cca635bc5e09800a9ab2a87c8842dc954416da2d3e7c9ce; uid_tt_ss_tiktokseller=65369c170ac74dd19cca635bc5e09800a9ab2a87c8842dc954416da2d3e7c9ce; sid_tt_tiktokseller=8b71f445c040834b72e06540c59d35c1; sessionid_tiktokseller=8b71f445c040834b72e06540c59d35c1; sessionid_ss_tiktokseller=8b71f445c040834b72e06540c59d35c1; sid_ucp_v1_tiktokseller=1.0.0-KDNiNjRjZGNjNDNlYzcwMWU3ZjdlOTk2YTg4MDRjYTJlMDk0NWNlNDAKGgiFiOLI1-6ZkWUQ_M_7qgYY5B8gDDgBQOsHEAMaA3NnMSIgOGI3MWY0NDVjMDQwODM0YjcyZTA2NTQwYzU5ZDM1YzE; ssid_ucp_v1_tiktokseller=1.0.0-KDNiNjRjZGNjNDNlYzcwMWU3ZjdlOTk2YTg4MDRjYTJlMDk0NWNlNDAKGgiFiOLI1-6ZkWUQ_M_7qgYY5B8gDDgBQOsHEAMaA3NnMSIgOGI3MWY0NDVjMDQwODM0YjcyZTA2NTQwYzU5ZDM1YzE; store-idc=useast5; store-country-code=us; store-country-code-src=uid; _ga_BZBQ2QHQSP=GS1.1.1700718454.1.1.1700718589.0.0.0; SHOP_ID=7287490570413736235; s_v_web_id=verify_lpas0kur_o3gFvU7J_wHaP_44W1_8FtL_JSYFZoRrevWJ; i18next=en; csrf_session_id=bf0484527811481a44860e7f19ec23e1; _ttp=2YeEosQdMVdlJdn3hWqPiwSBOUe; user_oec_info=0a53a59f97b32b103f52e4d6855ea7cc14aa201b50aa9e2842599dc0f1e0cb2b76bbd76639243488b19aa3d9dc49b52af85fd0a668e538bd3d8c021d9cad76fa6360f1c060ee458e8ff57f4649ee70f42150010cfd1a490a3c4b0ccbd0e224d905d4ed17c9e1d4842aad78f4b05ebd02f73866388a184d6b7339342d72b5e940f5576de363bbc482dece92cfc541346c290eacb69b10b3c7c20d1886d2f6f20d220104ee0b248d; ttwid=1%7CljckUrx8KLuRgbyS9-_n9_TvYf2AZgvnUcdIx6LHK1g%7C1701219890%7Cfe55f3019c0c6eddecd38bba32110a6c4de86d93767c2108219dd55b2b6d6a0f; odin_tt=b14512253d0f5a908a6035d607069b65e0fd3fb7eefb2c657a12d2901e2e1b8db27a740ba1db855fa26f043bd6bb3c6cc79464f9f6f462879bcc9660ffe457ee; gd_worker_v2_random_1261=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDE4MjQ3NzYsImlhdCI6MTcwMTIxOTk3NiwibWF0Y2giOmZhbHNlLCJuYmYiOjE3MDEyMTk5NzYsInBhdGgiOiIvIiwicGVyY2VudCI6MC45NDMxOTk0MzQ1OTY3NDc3fQ.AtYboFuG6WY1Re4kX5ykRnkJ6f2l3MMwdlX1g9cyy_c; msToken=U0-xH3zjg2bCpNMz_ss1rEZXv4L3uoCWSK1W9zSGLiHpsEj4-fGb7mA50ILQrWYuCKjiCuFxjWoXxCCWjaTYdo-FE4yxdiBONZuTX2j0sdpr_UbDg4gK",
            "origin": "https://affiliate-us.tiktok.com",
            "pragma": "no-cache",
            # "referer": "https://affiliate-us.tiktok.com/connection/creator?shop_region=US&enter_from=affiliate_home_page",
            "sec-ch-ua": "\"Chromium\";v=\"112\", \"Google Chrome\";v=\"112\", \"Not:A-Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
        }

    def get_product(self):
        url = "https://seller-us.tiktok.com/api/v1/product/local/products/list?locale=en&language=en&aid=4068&app_name=i18n_ecom_shop&device_id=0&fp=verify_lpj6riek_u9HDrggc_2dzp_4FHD_8fyU_uab710skNwxC&device_platform=web&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=MacIntel&browser_name=Mozilla&browser_version=5.0%20%28Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F112.0.0.0%20Safari%2F537.36&browser_online=true&timezone_name=Asia%2FShanghai&tab_id=1&page_number=1&page_size=100&sku_number=1&product_sort_fields=3&product_sort_types=0&msToken=&X-Bogus=11&_signature=1"
        for key,value in self.cookies.items():
            resp = requests.get(url, headers=self.headers, cookies=value)
            shops = []
            for value in resp.json()['data']['products']:
                if value['total_available_stock'] and value['visible_status']['is_visible']:
                    shops.append(value['product_id'])
            self.products[key] = [{"product_id": i, "target_commission": 7000} for i in shops]
        print(f"产品信息：")
        print(self.products)

    def get_ids(self,searchlist):
        url = "https://affiliate-us.tiktok.com/api/v1/oec/affiliate/creator/marketplace/search?user_language=en&aid=4331&app_name=i18n_ecom_alliance&device_id=0&fp=verify_lpki981m_o0fGPIaW_pK7b_4fwJ_BgV9_HGihMtsVPwpz&device_platform=web&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=MacIntel&browser_name=Mozilla&browser_version=5.0+(Macintosh%3B+Intel+Mac+OS+X+10_15_7)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F112.0.0.0+Safari%2F537.36&browser_online=true&timezone_name=Asia%2FShanghai&shop_region=US"
        self.users_list = []
        for j in searchlist:
            init_len = 0
            search_key = ""
            print(f"搜索词:{j}")
            for i in range(0, 50):
                try:
                    data = {"request": {"follower_genders": [], "follower_age_groups": [], "managed_by_agency": [],
                                        "pagination": {"size": 20, "page": i,
                                                       "search_key": search_key},
                                        "creator_score_range": [], "content_preference_range": [], "algorithm": 1,
                                        "query": j,
                                        "query_type": 1}}
                    init_len = len(self.users_list)
                    resp = requests.post(url, headers=self.headers, json=data, cookies=self.cookies[list(self.cookies.keys())[0]])
                    if resp.json()['code'] != 0:
                        break
                    search_key = resp.json()['data']['next_pagination']['search_key']
                    [self.users_list.append(i) for i in list(set(resp.json()['data']['shop_invite_info'].keys())) if
                     i not in self.users_list]
                    if init_len == len(self.users_list):
                        break
                    print(len(self.users_list))
                except Exception as e:
                    print(e)
        # print(self.users_list)
    def invite(self):
        url = "https://affiliate-us.tiktok.com/api/v1/oec/affiliate/seller/invitation_group/create?user_language=en&aid=4331&app_name=i18n_ecom_alliance&device_id=0&fp=verify_lpj35ejl_G0NCZgfv_4kJf_4hKL_9wGg_ECNiGuwacP8O&device_platform=web&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=MacIntel&browser_name=Mozilla&browser_version=5.0+(Macintosh%3B+Intel+Mac+OS+X+10_15_7)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F112.0.0.0+Safari%2F537.36&browser_online=true&timezone_name=Asia%2FShanghai&shop_region=US"
        group_size = 50
        groups = [self.users_list[i:i + group_size] for i in range(0, len(self.users_list), group_size)]
        max_limit=[]
        for id in groups:
            id = [{i: {'base_info': {'creator_id': '', 'nick_name': '', 'creator_oec_id': i}}} for i in id]
            for key,value in self.cookies.items():
                if key in max_limit:
                    continue
                for _ in range(2):
                    data = {"invitation_group": {"name": f"20%/70% {time.strftime('%Y%d%m')} K",
                                                 "message": self.hs[key]['邀请话语'],
                                                 "contacts_info": [
                                                     {"title": "", "field": 7, "value": self.hs[key]['邀请邮箱'],
                                                      "country_code": ""},
                                                     {"title": "", "field": 46, "value": "", "country_code": "US#1"}],
                                                 "has_free_sample": False, "end_time": self.hs[key]['日期'],
                                                 "product_list":self.products[key],
                                                 "creator_id_list":[list(i.values())[0] for i in id]}}
                    resp = requests.post(url, headers=self.headers, json=data, cookies=value)
                    if resp.json()['code']==98001004:
                        max_limit.append(key)
                        print(f"{key}已经超出了最大邀请限制，请删除后再重新邀请。")
                    try:
                        if resp.json()['data'].get("invitation"):
                            print(resp.json())
                            break
                        else:
                            confilict_list_ids=list(set([i['creator_id_list'][0]['base_info']['creator_oec_id'] for i in resp.json()['data']['conflict_list']]))
                            id=[i for i in id if list(i.keys())[0] not in confilict_list_ids]
                    except Exception as e:
                        print(e)
                        if resp.status_code==200:
                            print(resp.json())

    def run(self):
        self.get_product()
        self.get_ids(searchlist=searck_key)
        self.invite()
searck_key=get_text('search_keyword.txt')
metamask_profiles=get_json('account.json')
hs={}
for i in metamask_profiles:

    time_obj = datetime.strptime(i['日期'], "%Y-%m-%d %H:%M:%S")
    timestamp = time.mktime(time_obj.timetuple())
    i['日期'] =str(int(timestamp*1000))
    hs[i['name']] = i

get_ck = GETCOOKIES(users=metamask_profiles)
get_ck.run()
gr=GETCREATEID(cookies=get_ck.cookies)
gr.run()
#print("")