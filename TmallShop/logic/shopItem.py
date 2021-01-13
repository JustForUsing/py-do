# coding=utf-8
from TmallShop.config import common
from scrapy.selector import Selector
import requests


def get_shop_items():
    html = requests.get(common.params['shop_all_item_url']).text
    all_item_ids = []

    # all_item_html = Selector(text=html).xpath('//dl[@class="item   "]').extract()
    all_item_html = Selector(text=html).xpath('//dl[contains(@class,"item")]').extract()

    for each_item_html in all_item_html:
        each_item_id = Selector(text=each_item_html).xpath('//dt/a/@href').re(r'\w*\d')[0]
        # 不在店铺主页爬取数据了，只要商品id
        # if all_item_data.has_key(each_item_id):
        #     continue
        # all_item_data[each_item_id] = {
        #     'thumb': Selector(text=each_item_html).xpath('//dt/a/img/@data-ks-lazyload').extract_first(),
        #     'price': Selector(text=each_item_html).xpath('//span[@class="c-price"]/text()').extract_first(),
        #     'name': Selector(text=each_item_html).xpath('//a[@class="item-name"]/text()').extract_first()
        # }
        if each_item_id in all_item_ids:
            continue
        all_item_ids.append(each_item_id)

    return all_item_ids
