# coding=utf-8
from TmallShop.logic import shopItem
from TmallShop.logic import itemDetail
all_item_ids = shopItem.get_shop_items()
item_detail_class = itemDetail.ItemDetail(all_item_ids)
result = item_detail_class.link_start()
print(result)

# from TmallShop.config import common
# import requests
# from scrapy.selector import Selector
# import re
#
# common.params['request_params']['itemId'] = 592152256742
# common.params['request_headers']['Connection'] = 'close'
# proxies = {'http': '81.201.60.130:80', 'https': '81.201.60.130:80'}
# item_detail_response = requests.get(url=common.params['ajax_item_detail'], headers=common.params['request_headers'], params=common.params['request_params'], proxies=proxies).json()
# print(item_detail_response)
# exit(1)