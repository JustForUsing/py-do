# coding=utf-8
import re

from TmallShop.config import common
from TmallShop.config import ips
from TmallShop.common import functions_file
from scrapy.selector import Selector
import requests
import json
import time
import random


class ItemDetail:
    def __init__(self, item_ids):
        # 初始化数据
        self.item_ids = item_ids
        # Ajax请求头
        self.request_headers = common.params['request_headers']
        # Ajax请求参数
        self.request_params = common.params['request_params']
        # 待处理数据
        self.from_sku = []
        # 返回数据
        self.result_data = {}

        # 全局设置request
        requests.packages.urllib3.disable_warnings()
        self.request_obj = requests.session()
        self.request_obj.keep_alive = False

    def link_start(self):
        return self.get_all_detail()

    def get_all_detail(self, operation="item"):
        # 判断是爬新商品，还是处理SKU
        item_ids = self.item_ids if operation == 'item' else self.from_sku

        # 记录浏览器的UA下标
        browser_ua_index = -1
        # 记录代理IP轮换的下标
        proxy_ips_index = -1

        # 开始
        for item_id in item_ids:
            # 换UA
            if browser_ua_index < len(common.params['browser_uas']) - 1:
                browser_ua_index += 1
            else:
                browser_ua_index = 0

            # 强类型语言必须先初始化key
            self.result_data[item_id] = {}

            # 为了避免请求出现BadStatusLine,request的keep_alive设为false,轮换UA，请求头断连
            page_header = {
                'User-Agent': common.params['browser_uas'][browser_ua_index],
                'Connection': 'close'
            }
            # 模拟访问页面
            print(str(item_id) + ' : curl start')
            page_item_detail_response = self.try_request(common.params['page_item_detail'] + str(item_id), page_header)
            if page_item_detail_response is None:
                functions_file.debug_log(common.params['page_item_detail'] + str(item_id))
                print(str(item_id) + ' : get page info failed !')
                continue
            else:
                page_item_detail_html = page_item_detail_response.text
                print(str(item_id) + ' : get page info success')

            # 商品名称
            self.result_data[item_id]['name'] = Selector(text=page_item_detail_html).xpath('//div[@class="tb-detail-hd"]/h1/text()').extract_first().strip('\t\r\n ')

            # 商品轮播图
            item_banner = Selector(text=page_item_detail_html).xpath('//ul[@id="J_UlThumb"]/li/a/img/@src').extract()
            for ebk, ebv in enumerate(item_banner):
                item_banner[ebk] = ebv.replace("60x60", "430x430").strip('/')
            self.result_data[item_id]['banners'] = item_banner

            # 商品缩略图
            self.result_data[item_id]['thumb'] = item_banner[0].replace("430x430", "240x240")

            # 商品二级标题
            self.result_data[item_id]['second_title'] = Selector(text=page_item_detail_html).xpath(
                '//div[@class="tb-detail-hd"]/p/text()').extract_first().strip('\r\n\t ')

            # 商品参数
            goods_params = Selector(text=page_item_detail_html).xpath('//ul[@id="J_AttrUL"]/li/text()').extract()
            dic_goods_params = {}
            for each_params in goods_params:
                # Python没有isset()判断,可以每次初始化 temp_list = ['','']
                if each_params.find(':') == -1:
                    continue
                temp_list = each_params.split(":")
                dic_goods_params[temp_list[0]] = temp_list[1]
            self.result_data[item_id]['goods_params'] = dic_goods_params

            # 商品描述详情
            desc_requset_url = 'https://' + re.findall(r'descnew.*?(?=\")', page_item_detail_html)[0]
            desc_response = self.try_request(desc_requset_url, common.params['desc_request_header'])
            if desc_response is None:
                functions_file.debug_log(desc_requset_url)
                print(str(item_id) + ' : get desc info failed !')
                continue
            else:
                self.result_data[item_id]['desc'] = desc_response.text.strip(r'var desc=;')
                print(str(item_id) + ' : get desc info success')

            # Ajax商品
            self.request_params['itemId'] = item_id
            # self.request_params['itemId'] = 592152256742
            # item_detail_response = self.request_obj.get(url=common.params['ajax_item_detail'], headers=common.params['request_headers'], params=self.request_params).json()

            self.request_headers['User-Agent'] = common.params['browser_uas'][browser_ua_index]
            self.request_headers['Connection'] = 'close'

            # 轮换代理ip
            if proxy_ips_index < len(ips.params) - 1:
                proxy_ips_index += 1
            else:
                proxy_ips_index = 0
            proxies = {'http': ips.params[proxy_ips_index], 'https': ips.params[proxy_ips_index]}
            print(proxies)
            item_detail_response = self.try_request(common.params['ajax_item_detail'], self.request_headers, self.request_params, proxies, 30)
            if item_detail_response is None:
                print(str(item_id) + ' : get item detail failed !')
                continue
            else:
                print(str(item_id) + ' : get item detail success')
                item_detail_response = item_detail_response.json()

            # 库存
            self.result_data[item_id]['goods_number'] = item_detail_response['defaultModel']['inventoryDO']['icTotalQuantity']

            # 获取价格
            item_price_key = list(item_detail_response['defaultModel']['itemPriceResultDO']['priceInfo'].keys())
            # 在售价格
            self.result_data[item_id]['price'] = item_detail_response['defaultModel']['itemPriceResultDO']['priceInfo'][item_price_key[0]]['promotionList'][0]['price']
            # 老价格
            self.result_data[item_id]['old_price'] = item_detail_response['defaultModel']['itemPriceResultDO']['priceInfo'][item_price_key[0]]['price']

            # 如果不是从SKU来的就获取SKU
            if operation == 'item':
                if 'relatedAuctionsDO' in item_detail_response['defaultModel']:
                    for each_sku in item_detail_response['defaultModel']['relatedAuctionsDO']['relatedAuctions']:
                        self.from_sku.append(each_sku['itemId'])

            # 随机随眠40S~60S
            print('wait random sleep.....')
            time.sleep(random.randint(40, 60))
            if browser_ua_index == 3:
                print(self.result_data)
                break
                exit(1)

        # 判断sku商品是否为0，不为0的话再爬一遍SKU商品
        if len(self.from_sku) != 0 and operation == 'item':
            self.get_all_detail('sku')
        return self.result_data

    # 仿照retry函数
    def try_request(self, url, header='', param='', proxies='', max_time=1, try_num=3):
        print(str(try_num) + '    ' + str(url))
        if try_num == -1:
            functions_file.debug_log(url)
            # with open('./debug/' + datetime.datetime.now().strftime('%Y%m%d%H') + '.log', 'a') as f:
            #     f.write('\n' + str(url))
            return
        try:
            return self.request_obj.get(url, headers=header, params=param, proxies=proxies, timeout=max_time)
        except IOError as e:
            print(e)
            time.sleep(60)
            # 代理端口打不通就用本地ip
            if try_num == 1:
                proxies = ''
            print('try proxies: ' + str(proxies))
            self.try_request(url, header, param, proxies, max_time, try_num - 1)


