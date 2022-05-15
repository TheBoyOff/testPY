import json
import random
import re
import threading
import time
#pip3 install requests
import requests
from urllib import parse

#凌晨场？
isnight = 1
starttime = 1652367598000  #开始时间戳 13位 网址：https://tool.lu/timestamp/  59:59
starttime = 1652544000000
#   2022-05-13 21:59:59
frontime =  0 if isnight else 120000      #提前多久获取urlbody
sleeptime = 0.055       #   55ms        #每个ck两次抢券的间隔
robsum = 1 if isnight else 4             #每个号生成n个api
flag_start = True if isnight else False  #是否开抢
cookies = [
    ##'pin=jsd_RaIgpFtXPrGd;wskey=AAJiVEmgAECZcNJZ11SNKWzbi65E8R8nQB-_3xAoyY1Ri9v6ZaR4obO6_z1DtUqpQrI9ttLG8bhHZA--7EM9viM5MTipNKpu;whwswswws=JD012145b9HdSnKp6iJs165235561754405BTcDhuGe7FmWdlZ1v6zsKabmjlTD76Vs10BfnztIvUBoLySAQjkMYfRhcbrRUkoypxC98UwKuuU6qfqJMcJF4O8hJFEgGJCWJw5rleUClJw1skogks~aareLFuggvJSyd3OQhRrJOTbIudoaZwYGQamHVzAsQ-Caw8vuGCUMyJ9FPEh7z03oxboda7S-Ooq-S8_Oa3ZYmmAUyg6Xkevn7ShUt4Ar64q_KLS9uG0fAcUIpury1FnyZr4h0kbl2jYOAa_qFblEzTrxqz22_q5XmAeL3RMlmJA;unionwsws={"devicefinger":"eidA88eb8120d6sen30D3jl2Q5SHkpYKfMxtTp99BV06h2tYb7ap4vMdQAS++Bj\/0gZ1hWQ1F+p9D1Z8mUV6DVai53msyVsGqYFPqvZOkbLMKSec8mZ6","jmafinger":"JD012145b9HdSnKp6iJs165235561754405BTcDhuGe7FmWdlZ1v6zsKabmjlTD76Vs10BfnztIvUBoLySAQjkMYfRhcbrRUkoypxC98UwKuuU6qfqJMcJF4O8hJFEgGJCWJw5rleUClJw1skogks~aareLFuggvJSyd3OQhRrJOTbIudoaZwYGQamHVzAsQ-Caw8vuGCUMyJ9FPEh7z03oxboda7S-Ooq-S8_Oa3ZYmmAUyg6Xkevn7ShUt4Ar64q_KLS9uG0fAcUIpury1FnyZr4h0kbl2jYOAa_qFblEzTrxqz22_q5XmAeL3RMlmJA"};',
    'pin=jd_BaiCQgoAsEpr;wskey=AAJiYh-FAEAm3GrxQkf8zdE5V3CpoEVesOtH9OtSP65zy3f9PScU8NZe9wn35O4HPQibDG1EpiRT_PBJpqy66Uc5CohNoKZG;whwswswws=JD012145b9rTdfiRnRz11652355735186040HLowZPHlkIi3iA7cZ59Qtk5QF4nkLrwdvf3sLk3B8GgPapNcF9Ip9VQ_nxGVI_XkglDmmnDwu1l7dYFKzWiP9ODfQ-Eye5ZSJXi8IHetvo1s25k1e~dxCzfQKSCjb8MK6NOdQuCoUpqq109mm0dQ5q_ap87hlwr2_JrninUPaKNZdnAn0sRNw84uAR1PyaWUOhFixZI6phLImHTHteNd97s3wrziA08iS9n7Ea0mC9DRB1iSFyYjr_Fazl6RwIe7-HSn_3K6wfsxp53QEYpVpHCI34ycV4;unionwsws={"devicefinger":"eidA2a048122aesbDpgxjB3zT5CUxwtzQQJT7g6YMwqsr3h+FcA3ZZydSToXNvuhJtL1wFVOakWSWtCZLJCox4uwqDQ9OXE8SL0s+23+SoQ67VuTAnpk","jmafinger":"JD012145b9rTdfiRnRz11652355735186040HLowZPHlkIi3iA7cZ59Qtk5QF4nkLrwdvf3sLk3B8GgPapNcF9Ip9VQ_nxGVI_XkglDmmnDwu1l7dYFKzWiP9ODfQ-Eye5ZSJXi8IHetvo1s25k1e~dxCzfQKSCjb8MK6NOdQuCoUpqq109mm0dQ5q_ap87hlwr2_JrninUPaKNZdnAn0sRNw84uAR1PyaWUOhFixZI6phLImHTHteNd97s3wrziA08iS9n7Ea0mC9DRB1iSFyYjr_Fazl6RwIe7-HSn_3K6wfsxp53QEYpVpHCI34ycV4"};',
    'pin=jd_XlEUWWCeDSnP;wskey=AAJiB60kAEAxruIoM7u4uvGOdvKPBorWZpW6emFKxEVvggCcLN1vFOPi5GiLRvC76L7CEKothijg_tPDc8o2HKzNKoH3pZ3q;whwswswws=JD012145b9xtx4Lay6oM165223249904404EAPMqSlqCTtcWn2HK9TD63Pho_xnv0p0FMguIj2BFfePY1UoTP4g7pKa-judMdW5J8yfCnVzFJ023haG-e5P043GXMrKSyvqL0ZXcsfpPMg0bvy58o~x7dXxKevBCYWqFD3bVOO2pHfap8hcMq7xQYemprTAcJih6A3BpE9FhsiUCCwTQPneWXWLWH-LrcfANMROBqP1R7UFPui8ww0SKnQvFv_0mnKpc2QDS-I5TP92aRYU0-AmYjuAAMMlpjxhfV5ECRAdz_KWlR0QwtDEoJ6L9cHytUs;unionwsws={"devicefinger":"eidA1da181231as8UWXhDOlOR321RoVnxAzyRFFl4ouTfyqUkNWedWipDlLzvIvR4Wuigk9K38pO7IlXqx+F5\/aZUpv1dGw5e68iDUkTQxbjineCS2s1","jmafinger":"JD012145b9xtx4Lay6oM165223249904404EAPMqSlqCTtcWn2HK9TD63Pho_xnv0p0FMguIj2BFfePY1UoTP4g7pKa-judMdW5J8yfCnVzFJ023haG-e5P043GXMrKSyvqL0ZXcsfpPMg0bvy58o~x7dXxKevBCYWqFD3bVOO2pHfap8hcMq7xQYemprTAcJih6A3BpE9FhsiUCCwTQPneWXWLWH-LrcfANMROBqP1R7UFPui8ww0SKnQvFv_0mnKpc2QDS-I5TP92aRYU0-AmYjuAAMMlpjxhfV5ECRAdz_KWlR0QwtDEoJ6L9cHytUs"};',
    'pin=jd_dpzGe34dfyARZ4T;wskey=AAJidPeIAFCdHC-Pnw_ybDnwVnvw6AhllvPuDCFLXEjt3U2wrmVRcMCYRQG8hCTWH32eXkF0hqWKla920QujCrtA5ssayxaEC3rQ_YW3I_ahAScPsrApDQ;whwswswws=JD012145b9Oikrxb7h3l165223276579901iM-oK5a3KfvKGr9eHAuLqXwk9gB4780nDJwS1g2dYB3diTf_Gxb2N722W2YwijcuIt5mf_gLbCpkaURnTWAsBiK2UVAg4JJF196qmz8~repWfb4Y4mwwjWAGNQaLuMEqtQ-R6j3CSvvx7wD1Hi5N1GxE5i9icXNOdmHO_mLMWJcbRb4NBaPCXkUS8CgmkyLqdN5Viwskxp__b25YrAC0bZahF3nyJgB4CncjlHhtMroPIaEjg0CeqQ50ZgGd62IkEcrGweGfpxrSYi4k-8wo;unionwsws={"devicefinger":"eidAdfb7812259sedUO3Do31RH+bdMFiqKrsJHVDuI2qcQ+Nys20n5lIgnx1KMbVWRunq3UwiKy++SsWWOJQaVTyQxifROPaVy6Zuho5CCU2bA0gnpR6","jmafinger":"JD012145b9Oikrxb7h3l165223276579901iM-oK5a3KfvKGr9eHAuLqXwk9gB4780nDJwS1g2dYB3diTf_Gxb2N722W2YwijcuIt5mf_gLbCpkaURnTWAsBiK2UVAg4JJF196qmz8~repWfb4Y4mwwjWAGNQaLuMEqtQ-R6j3CSvvx7wD1Hi5N1GxE5i9icXNOdmHO_mLMWJcbRb4NBaPCXkUS8CgmkyLqdN5Viwskxp__b25YrAC0bZahF3nyJgB4CncjlHhtMroPIaEjg0CeqQ50ZgGd62IkEcrGweGfpxrSYi4k-8wo"};',
    ## ,'pin=jd_OD0UTIhTUyYrjcA;wskey=AAJiB6oBAFA8JqSyCuA7-lcm1_zBD4x7deeP-XlhgblpqeeLfahL-BrHk3jc9s4pXdkvVw_ciHN_9sIGBVUSOGHgijJ9CZ5RJHsmEAr15faOtHG8DheYOA;whwswswws=JD012145b9VrFq3BXdg116522329494020414d6QQK21Kv_ZAOdzVsNH3v48ynaZGPw6c3vRYuK5mPa1pf_pdr9qXTmtvfNzDtFCUOpIErdyPmjE8ZkbaXfgUshHTpRHfkdKSXPQlZhOdM1pfke0p~etPa9A7mDKlRlyiJseEL1LnOOPlaNVzeo4j2Oekn6kqOMN82HITlWg4QfzlzMZjNZ9j-GMx1Ei1iqhhe6ieWyxPayCazINYoUhAOGjFVQGgb2Ps66sIbjMwcCMjCHOem8yDGZfiM3-G6NNPq2zztihv51ZRROKAFVZ86YF5B9YeU;unionwsws={"devicefinger":"eidA04f7812352sfXD5XeRPPRBizo93H0ytOp1w+WPfCN0\/Jiajm73BpioMTXuTsUkgcPmlJxLrwdbyyICa4RRKymwem+jWLiX+WYTZ2PfIkUYbzxgE1","jmafinger":"JD012145b9VrFq3BXdg116522329494020414d6QQK21Kv_ZAOdzVsNH3v48ynaZGPw6c3vRYuK5mPa1pf_pdr9qXTmtvfNzDtFCUOpIErdyPmjE8ZkbaXfgUshHTpRHfkdKSXPQlZhOdM1pfke0p~etPa9A7mDKlRlyiJseEL1LnOOPlaNVzeo4j2Oekn6kqOMN82HITlWg4QfzlzMZjNZ9j-GMx1Ei1iqhhe6ieWyxPayCazINYoUhAOGjFVQGgb2Ps66sIbjMwcCMjCHOem8yDGZfiM3-G6NNPq2zztihv51ZRROKAFVZ86YF5B9YeU"};',
    'pin=jd_POroHDc7rJBXXPY;wskey=AAJiI1AgAFDeArRzOQn1kiYP90boNpeX8s2OxsjIcA48W_sT_yJWKSNEOMTws7arwYGy0dAjBJrNTffryTTD-kzjllBbRx3ktsD9oiR9s96P-r4ySEFbyA;whwswswws=JD012145b9sMCOwot7wg165223313799003ly__pcBsedioKiPs0FKM4d_wObfslgC_7Cw0IkPp9L0qkJymtM_ZyJtOgRL4-Shs41lmXpsDlW1GxJHeRENFQ9u4XTzxIwRU08t3r49~gychDacs-_9k8u4M-OyYvkxdUlPwwE_VMJTBcNXUfzwDRVp0NOCNeCCJQV0tXtoI0r0pycgXLi01y8u1ICbQEFE0mEGRFoX2cbzQHXZVvIUM-nov_u8k4fTEkD_7P6AdMDu-kpT7uMoSDwZz0igYOwoyIprkM08BAwn2YIyQP6lo;unionwsws={"devicefinger":"eidA8586812099sehDiAvHVgQ6aYh+ciX++Q7IQ4gjsj6R+DEJy2E47n5+iCAgW057g4IU5pR9jLe8TUmUkYaLuJ1jOOvry0UHtPyNDWo2NSSZ5tIx91","jmafinger":"JD012145b9sMCOwot7wg165223313799003ly__pcBsedioKiPs0FKM4d_wObfslgC_7Cw0IkPp9L0qkJymtM_ZyJtOgRL4-Shs41lmXpsDlW1GxJHeRENFQ9u4XTzxIwRU08t3r49~gychDacs-_9k8u4M-OyYvkxdUlPwwE_VMJTBcNXUfzwDRVp0NOCNeCCJQV0tXtoI0r0pycgXLi01y8u1ICbQEFE0mEGRFoX2cbzQHXZVvIUM-nov_u8k4fTEkD_7P6AdMDu-kpT7uMoSDwZz0igYOwoyIprkM08BAwn2YIyQP6lo"};',
    ## ,'pin=wdABUJoQxZIOtZ;wskey=AAJiBn1_AECmG6jSHSsOVdWkhVjzqhFibUIIs313Jq9ZTRNv2eBR9b_7kTJvdZa9fREAaGVNmjc-dg2bbK6zsDs-lRO8EARw;whwswswws=JD012145b9YRLw1DzkYh165223331969603NcOAZw7Y-FZTesLoCIY1Egb-8ZKDD2HZEnvdpyS6NlQDg0TjTZ5WLqx91Q2mAFdcKYqbnEADzk_OTX42g3i0Ee0M4hU9OrCu14dbycc~zSAwDGfkrAoZeTeo_Yp9TrSFrX9uoH9uWHFMSr1CVx1eTIQ-pEd9kFBk99mPfxxh-YzsvOaC2fxj4InL2XmLWsFTsk4odZf9VLuobe6QajaaW58JQXSuFJQTEX3zsIT9TVLZ68lJkESuvatSS9M1L2uqix80mhS8l3z-M_13-G-k;unionwsws={"devicefinger":"eidAcc718121ecsex8c\/s27OQ8SWLOBryjoY+MfHQTJYJ3pllF2jqpEJQq+a\/z4\/LS18Szk4qCmw1yVm5ZjdxXcWVKtess+l9BWGBq5Q38XJMQspexV0","jmafinger":"JD012145b9YRLw1DzkYh165223331969603NcOAZw7Y-FZTesLoCIY1Egb-8ZKDD2HZEnvdpyS6NlQDg0TjTZ5WLqx91Q2mAFdcKYqbnEADzk_OTX42g3i0Ee0M4hU9OrCu14dbycc~zSAwDGfkrAoZeTeo_Yp9TrSFrX9uoH9uWHFMSr1CVx1eTIQ-pEd9kFBk99mPfxxh-YzsvOaC2fxj4InL2XmLWsFTsk4odZf9VLuobe6QajaaW58JQXSuFJQTEX3zsIT9TVLZ68lJkESuvatSS9M1L2uqix80mhS8l3z-M_13-G-k"};',
    'pin=jd_gudwJiduRibe;wskey=AAJiB63YAEA4Ho8IpRVbydGAGDq2Ci1jWzzCPfCYxEmmyS_18G4aq6-FHNK8aESogCBrVjTI6H6NYgmKNUmXJZbyXARWN81b;whwswswws=JD012145b9BIJe8cSCZ7165223349343002pYg9hzTBWMR6q5fFI4qvKY6K8_W1CMlUSYnhAIVhmuZesclHwnul472KuptmmNu5MLXraWEmzvWD3VjN7X1OyxBaUkLickkr12nk4eg~zHNzDJfs-WLSY-gLZcNoHNns72YTWXKG4bu95nVptc0AnRg9gpG1tt9x6y1ZPp5pVE1GDnSya9h-ZdjNA0efgFQXIMJeA4Q5Fr88lbJ4ZnLBJuDj5pKAmCy0SNDgaKD9uTWbjI4l3776Yn-t_A49VgFs8h-5VOaYocD7TzJ6spn8;unionwsws={"devicefinger":"eidAb8df8120eas8bg+VWwAzTS21UUZPLHdLR24PltmrPg0C3wjbKQha7e4aiCnBJFZbnDNR0zFpWuITr3xI3HvB1OzA6fJ9SL3XjNH+s8RHOCzK2RRO","jmafinger":"JD012145b9BIJe8cSCZ7165223349343002pYg9hzTBWMR6q5fFI4qvKY6K8_W1CMlUSYnhAIVhmuZesclHwnul472KuptmmNu5MLXraWEmzvWD3VjN7X1OyxBaUkLickkr12nk4eg~zHNzDJfs-WLSY-gLZcNoHNns72YTWXKG4bu95nVptc0AnRg9gpG1tt9x6y1ZPp5pVE1GDnSya9h-ZdjNA0efgFQXIMJeA4Q5Fr88lbJ4ZnLBJuDj5pKAmCy0SNDgaKD9uTWbjI4l3776Yn-t_A49VgFs8h-5VOaYocD7TzJ6spn8"};',
]
re_ck = re.compile(r'pin=.*?;')
OKSS=[]
bodyuuu = '%7B%22monitorSource%22%3A%22ccfeed_android_index_feed%22%2C%22eid%22%3A%22qaajjysff0vv5w55%22%2C%22monitorRefer%22%3A%22appClient%22%2C%22globalLat%22%3A%22%22%2C%22lng%22%3A%22%22%2C%22pageSize%22%3A%2220%22%2C%22pageClickKey%22%3A%22Coupons_GetCenter%22%2C%22pageNum%22%3A%221%22%2C%22childActivityUrl%22%3A%22openapp.jdmobile%3A%2F%2Fvirtual%3Fparams%3D%7B%5C%22category%5C%22%3A%5C%22jump%5C%22%2C%5C%22des%5C%22%3A%5C%22couponCenter%5C%22%7D%22%2C%22shshshfpb%22%3A%22%22%2C%22globalLng%22%3A%22%22%2C%22categoryId%22%3A%22118%22%2C%22lat%22%3A%22%22%7D'
def randomString(e, flag=False):
    t = "0123456789abcdef"
    if flag: t = t.upper()
    n = [random.choice(t) for _ in range(e)]
    return ''.join(n)
#xxxx

def jdtime():
    url = 'http://api.m.jd.com/client.action?functionId=queryMaterialProducts&client=wh5'
    headers = {
        "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    }
    try:
        res = requests.get(url=url, headers=headers, timeout=1).json()
        return int(res['currentTime2'])
    except:
        return 0
#xxxx

def get_sign_api_location(functionId, bodyuuu):
    sign_api = f'http://localhost:8080/myserver?functionId={functionId}&body={bodyuuu}'
    try :
        res = requests.post(url=sign_api, timeout=30)
        return res.text.replace('\n','')        #return sign字符串
    except:
        print('errer get_sign_api_location')
        return -1
#xxxx

def getCcFeedInfo(cookie):  #return receiveKey
    functionId = 'getCcFeedInfo'
    body = {
        "categoryId": 118,
        "childActivityUrl": "openapp.jdmobile://virtual?params={\"category\":\"jump\",\"des\":\"couponCenter\"}",
        "eid": randomString(16),
        "globalLat": "",
        "globalLng": "",
        "lat": "",
        "lng": "",
        "monitorRefer": "appClient",
        "monitorSource": "ccfeed_android_index_feed",
        "pageClickKey": "Coupons_GetCenter",
        "pageNum": 1,
        "pageSize": 20,
        "shshshfpb": ""
    }
    bodyuuu = str(body).replace(' ','').replace('"','\\"').replace("'",'"')
    bodyuuu = parse.quote(str(bodyuuu))
    if isnight == 0:
        print('body:',bodyuuu)
    sign = get_sign_api_location(functionId, bodyuuu) #st sv sign
    if sign == -1:
        return -1
    else:
        url = f'https://api.m.jd.com?functionId={functionId}&{sign}&body={bodyuuu}'
        if isnight == 0:
            print('url:',url)
        headers = {
            "Host": "api.m.jd.com",
            "cookie": cookie,
            "charset": "UTF-8",
            "user-agent": "okhttp/3.12.1;jdmall;android;version/10.1.4;build/90060;screen/720x1464;os/7.1.2;network/wifi;",
            "accept-encoding": "br,gzip,deflate",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            # "content-length": str(len(body)),
        }   #ck
        res = requests.post(url=url, headers=headers, timeout=30).json()
        try :
            # print('receiveKey:',res['result']['couponList'][0]['receiveKey'])
            # return res['result']['couponList'][0]['receiveKey']
            for coupon in res['result']['couponList']:
                if coupon['title'] != None and '每周可领一次' in coupon['title']:
                    receiveKey = coupon['receiveKey']
                    return receiveKey
            print('没有找到59-20券的receiveKey')
            return -1
        except :
            print('没有找到59-20券的receiveKey\n    ',res)
            return -1
#get_sign_api('getCcFeedInfo', body)-----return receiveKey

def get_receiveNecklaceCoupon_sign(receiveKey):#return [url, body]
    functionId = 'receiveNecklaceCoupon'
    body = {"channel": "领券中心",
            "childActivityUrl": "openapp.jdmobile://virtual?params={\"category\":\"jump\",\"des\":\"couponCenter\"}",
            "couponSource": "manual",
            "couponSourceDetail": "",
            "eid": randomString(16),
            "extend": receiveKey,
            "lat": "",
            "lng": "",
            "pageClickKey": "Coupons_GetCenter",
            "rcType": "4",
            "riskFlag": 1,
            "shshshfpb": "",
            "source": "couponCenter_app",
            "subChannel": "feeds流"
            }       #Key
    bodyuuu = str(body).replace(' ','').replace('"','\\"').replace("'",'"')
    bodyuuu = parse.quote(str(bodyuuu))
    sign = get_sign_api_location(functionId, bodyuuu)
    if sign == -1:
        return -1
    else:
        urlbody = f'https://api.m.jd.com?functionId={functionId}&{sign}&body={bodyuuu}'
        return urlbody
#get_sign_api('receiveNecklaceCoupon', body)-----return urlbody

def text():
    cookie = cookies[0]
    Key = getCcFeedInfo(cookie)
    urlbody = get_receiveNecklaceCoupon_sign(Key)
    headers = {
        "Host": "api.m.jd.com",
        "cookie": cookie,
        "charset": "UTF-8",
        "user-agent": "okhttp/3.12.1;jdmall;android;version/10.1.4;build/90060;screen/720x1464;os/7.1.2;network/wifi;",
        "accept-encoding": "br,gzip,deflate",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    }
    print(urlbody)
    req = requests.post(url=urlbody, headers=headers)
    print(req.text)

def rob( cookie ):
    #先获取url
    global flag_start
    urls = []
    for i in range(robsum):     #获取robsum条url&body
        Key = getCcFeedInfo(cookie)
        urlbody = get_receiveNecklaceCoupon_sign(Key)
        urls.append(urlbody)
    # 一直卡到开始
    while flag_start == False:
        if jdtime() >= starttime:
            flag_start = True
    ret = '\n' + re_ck.findall(cookie)[0] + '\n'     #总输出结果
    k = 0
    while k < 3:              #运行3轮url+body
        k += 1
        for i in range(len(urls)):  #每轮从头到尾遍历urls
            headers = {
                "Host": "api.m.jd.com",
                "cookie": cookie,
                "charset": "UTF-8",
                "user-agent": "okhttp/3.12.1;jdmall;android;version/10.1.4;build/90060;screen/720x1464;os/7.1.2;network/wifi;",
                "accept-encoding": "br,gzip,deflate",
                "cache-control": "no-cache",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                # "content-length": str(len(bodys[i]))
            }
            res = requests.post(url=urls[i], headers=headers)
            try :
                ret += res.json()['result']['desc'] +'\n'
            except:
                ret += res.text.replace('\n','') + '\n'

            if '领券成功' in res or '领券成功' == res or '您已经兑换过' in res:
                OKSS.append(re_ck.findall(cookie)[0])
                k=4
                break
            time.sleep(sleeptime)
    print(ret)

def robs():
    tasks = list()      #多线程
    for i in range(len(cookies)):
        tasks.append(threading.Thread(target=rob, args=(cookies[i],)))
        print(f'线程{i}准备完毕！')
    while True:
        jdt = jdtime()
        if jdt + frontime >= starttime:
            print(f'开始抢券！--{jdt}')
            for task in tasks:
                task.start()
                time.sleep(sleeptime/len(cookies))
            for task in tasks:
                task.join()
            break
    print(f'抢券结束！--{jdtime()}')

robs()






