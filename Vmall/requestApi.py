import requests
import json
import time

request_obj = requests.session()
request_obj.keep_alive = False


request_url = 'https://buy.vmall.com/order/create.json'

request_headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '712',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': '',
    'Host': 'buy.vmall.com',
    'Origin': 'https://buy.vmall.com',
    'Referer': 'https://buy.vmall.com/submit_order.html?nowTime=2020-10-29%2018:08:10&skuId=10086777012110&skuIds=10086777012110&activityId=860120201026154&backUrl=https%3A%2F%2Fwww.vmall.com%2Fproduct%2F10086998928105.html%2310086777012110&rushbuy_js_version=55eb97dc-e977-4d5b-a820-85a8fa675eb4&backto=https%3A%2F%2Fwww.vmall.com%2Fproduct%2F10086998928105.html%2310086777012110',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

request_params = {
    'duid': '',
    'uid': '',
    'skuIds': '',
    'quantity': '',
    'diyPackCodeArr': '',
    'diyPackSkus': '',
    'orderSign': '',
    'activityId': '',
    'streetId': '',
    'street': '',
    'districtId': '',
    'district': '',
    'cityId': '',
    'city': '',
    'provinceId': '',
    'province': '',
    'consignee': '',
    'address': '',
    'mobile': '',
    'phone': '',
    'zipCode': '',
    'custName': '',
    'titleType': '',
    'invoiceTitle': '',
    'taxpayerIdentityNum': '',
    'orderSource': '1',
    'activityUid': '',
    'nickName': '',
}

