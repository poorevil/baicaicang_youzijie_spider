#-*- coding:UTF-8 -*-
#!/usr/bin/env python

from __future__ import absolute_import

import sys    
reload(sys)
sys.setdefaultencoding('gb2312')  

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http.request import Request  
import json

from baicaicang_youzijie_spider.items import YouzijieItem


u'''

用于爬取柚子街客户端接口的爬虫~



catalog_id=0&group_id=1		服饰内衣
catalog_id=0&group_id=13	鞋包配饰
catalog_id=0&group_id=2		居家日用
catalog_id=0&group_id=3		护肤彩妆
catalog_id=8&group_id=4		美食保健
catalog_id=0&group_id=5		母婴用品
catalog_id=0&group_id=14	数码家电
catalog_id=0&group_id=15	图书文具
catalog_id=0&group_id=16	户外运动

类目：
http://api.youzibuy.com/brand_area_catalog/item_list?v=1.2.2&page=1&size=50&catalog_id=8&group_id=4

专场：
http://api.youzibuy.com/tae_item_list?v=1.2.2&brand_area_id=51272&page=1

首页：
http://api.youzibuy.com/tae_brand_list?v=1.2.2&app_id=7

'''

cate_array = [{'catalog_id':'0','group_id':'1','cate_title':u'服饰内衣'},
{'catalog_id':'0','group_id':'13','cate_title':u'鞋包配饰'},
{'catalog_id':'0','group_id':'2','cate_title':u'居家日用'},
{'catalog_id':'0','group_id':'3','cate_title':u'护肤彩妆'},
{'catalog_id':'8','group_id':'4','cate_title':u'美食保健'},
{'catalog_id':'0','group_id':'5','cate_title':u'母婴用品'},
{'catalog_id':'0','group_id':'14','cate_title':u'数码家电'},
{'catalog_id':'0','group_id':'15','cate_title':u'图书文具'},
{'catalog_id':'0','group_id':'16','cate_title':u'户外运动'}
]

#每api请求页数
load_page_count_per_api = 1


class YouzijieSpider (Spider):
	name = "youzijie"
	allowed_domains = ["api.youzibuy.com"]

	start_url_maps = []
	
	def __init__(self, request_type=None,*args, **kwargs):
		super(YouzijieSpider, self).__init__(*args, **kwargs)
		
	def start_requests(self):  
		
		for cate in cate_array :
			item_list_interface_url = u'http://api.youzibuy.com/brand_area_catalog/item_list?v=1.2.2&size=0&catalog_id=%s&group_id=%s'%(cate['catalog_id'],cate['group_id'])
	
			for i in xrange(1,load_page_count_per_api+1):
				request = Request('%s&page=%d'%(item_list_interface_url,i)) 
				request.meta['cate'] = cate

				# print '----------------------'+request.url
				yield request

	def parse(self, response):  
		try:

			cate = response.request.meta['cate']

			jsonObj = json.loads(response.body)

			if 'group_id' in cate:

				u'''
				{
					status: true,
					code: 200,
					msg: "",
					data: {
						list_style: 1,
						item_list: [
									{
										brand_area_id: 51526,
										name: "解决干枯毛躁静电香水护发精油80ml ",
										id: 212171,
										brand_id: 0,
										item_id: "AAHW6jHtAB3qoKkvnrPIrSyx",
										picture: "http://sc.seeyouyima.com/taobao/web_shopGuide5757f932125e1.png?imageView2/1/h/300/w/300/",
										start_at: "0000-00-00 00:00:00",
										end_at: "0000-00-00 00:00:00",
										redirect_type: "1",
										tag_icon: "0",
										promotion_ids: "5",
										coin_amount: 0,
										purchase_price: 0,
										is_active: "1",
										order_count: 2008,
										promotion_custom: "",
										shop_type: "1",
										redirect_brand_area_id: 51526,
										is_redirect_detail: "0",
										status: "0",
										tb_price: 8.8,
										vip_price: "8.8",
										original_price: 19.8,
										stock: -1,
										tb_stock: 1397177,
										open_id: "530844199508",
										specs: "",
										promotion_type: "0",
										jingqi_item_id: "AAHW6jHtAB3qoKkvnrPIrSyx",
										item_type: "2",
										tb_order_count: 1613,
										weekly_click_count: 3213,
										brand_area_is_active: "1",
										brand_area_start_at: "2016-06-23 09:50:00",
										brand_area_end_at: "2016-06-27 10:00:00",
										brand_area_name: "6.23个护美加分超级爆款精油",
										activity_id: 1,
										is_new: 0,
										sttag_text: "",
										sttag_type: 0,
										promotion_text_arr: [
										"包邮"
										],
										is_liked: 0,
										link_value: "AAHW6jHtAB3qoKkvnrPIrSyx",
										item_count_msg: "共5款",
										redirect_url: "",
										item_shop_type: "1",
										purchase_btn: "1613人已购"
										},
									],
						has_more: 0,
						page: 4
					}
				}
				'''

				if jsonObj['code'] == 200:
					itemList = jsonObj['data']['item_list']

					for item in itemList:
						yzjItem = YouzijieItem()

						# open_id = scrapy.Field()				#item_id
					 #    name = scrapy.Field()					#名称
					 #    picture = scrapy.Field()				#图片地址
					 #    vip_price = scrapy.Field()				#柚子街价格
					 #    original_price = scrapy.Field()			#原价
					 #    brand_area_start_at = scrapy.Field()	#开始时间
					 #    brand_area_end_at = scrapy.Field()		#结束时间
					 #    promotion_text_arr = scrapy.Field()		#包邮
					 #    redirect_brand_area_id = scrapy.Field()	#专题id，0：不是专题，1：专题id

					 	if item['redirect_brand_area_id'] != 0:
					 		request = Request('http://api.youzibuy.com/tae_item_list?v=1.2.2&brand_area_id=%d&page=1'%(item['redirect_brand_area_id'])) 
							request.meta['cate'] = {'cate_title':response.request.meta['cate']['cate_title'],'zhuanchang_title':item['brand_area_name']}

							print '---------redirect_brand_area_id-------------'+request.url
							yield request

						yzjItem['open_id'] = item['open_id']
						yzjItem['name'] = item['name']
						yzjItem['picture'] = item['picture']
						yzjItem['vip_price'] = item['vip_price']
						yzjItem['original_price'] = item['original_price']
						yzjItem['brand_area_start_at'] = item['brand_area_start_at']
						yzjItem['brand_area_end_at'] = item['brand_area_end_at']
						yzjItem['promotion_text_arr'] = item['promotion_text_arr']
						# yzjItem['redirect_brand_area_id'] = item['redirect_brand_area_id']
						yzjItem['cate_title'] = response.request.meta['cate']['cate_title']
						
						yield yzjItem
			else:

				u'''
				{
					items: [
						{
							id: 253570,
							activity_id: 0,
							brand_id: 0,
							name: "【4斤装】橙乐工坊 去渍护色洗衣液 薰衣草 植物萃取",
							sub_name: "",
							picture: "http://sc.seeyouyima.com/taobao/web_shopGuide574e99545a01d.jpg?imageView2/1/h/340/w/340/q/70",
							is_active: "1",
							start_at: "0000-00-00 00:00:00",
							end_at: "0000-00-00 00:00:00",
							item_id: "AAEj6jHtAB3qoKkvnrOV2mxE",
							open_id: "531597683361",
							tag_icon: "0",
							promotion_ids: "5",
							coin_amount: 0,
							purchase_price: 0,
							original_price: 58,
							tb_price: 9.9,
							vip_price: "9.9",
							stock: -1,
							tb_stock: 8624,
							redirect_type: 1,
							shop_type: "2",
							order_count: 5805,
							promotion_custom: "",
							item_type: "2",
							promotion_type: "1",
							tb_order_count: 11993,
							weekly_click_count: 16626,
							coin_item_id: 0,
							need_coin_amount: 0,
							is_new: 0,
							is_liked: 0,
							discount: "1.7折",
							type: "",
							purchase_btn: "11993人已购",
							sttag_text: "",
							sttag_type: 0,
							promotion_text_arr: [
							"包邮"
							],
							timer_type: 0,
							down_count: 0,
							redirect_url: "http://s.click.taobao.com/t?e=m%3D2%26s%3DZzl7loDkpGtw4vFB6t2Z2ueEDrYVVa64yK8Cckff7TVRAdhuF14FMfgiYRSZu9BIxq3IhSJN6GSLk%2FCwlqHEPqqpGup1lYQOf4Z34RdJ6Z1212Z80fy3Yylh0zaMR%2BtvpZO8DRG5kdtfoXZI%2BKguweVeUgohBJgZL0kmcwT7wQJW7G%2BuHCGx7VKqg7DMp65HuDGOcgei7q5aGPwzCpGZ2MYl7w3%2FA2kb&unid=meiyou123456"
							},
							...
					],
					toast: "",
					page: 1,
					name: "6.24橙乐工坊旗舰店秒杀专场",
					start_time: "2016-06-24 09:50:00",
					end_time: "2016-06-28 10:00:00",
					curr_time: "2016-06-27 14:38:11",
					list_style: 2,
					is_timer: 1,
					timer_type: "0",
					brand_area_id: 51272,
					top_tag: "",
					description: "",
					promotion_text: "",
					pay_error_message: "",
					has_more: 0,
					brand_picture: "",
					bp_link_type: 0,
					bp_link_value: "",
					bp_redirect_type: 1,
					bp_shop_type: 1,
					next_brand_area_id: 51955,
					next_brand_area_name: "诗恩服饰商城 牛仔专场",
					layer_tab: "1,2"
				}
				'''
				itemList = jsonObj['items']

				for item in itemList:
					yzjItem = YouzijieItem()

					#	 open_id = scrapy.Field()				#item_id
					#    name = scrapy.Field()					#名称
					#    picture = scrapy.Field()				#图片地址
					#    vip_price = scrapy.Field()				#柚子街价格
					#    original_price = scrapy.Field()			#原价
					#    brand_area_start_at = scrapy.Field()	#开始时间
					#    brand_area_end_at = scrapy.Field()		#结束时间
					#    promotion_text_arr = scrapy.Field()		#包邮
					#    redirect_brand_area_id = scrapy.Field()	#专题id，0：不是专题，1：专题id

					yzjItem['open_id'] = item['open_id']
					yzjItem['name'] = item['name']
					yzjItem['picture'] = item['picture']
					yzjItem['vip_price'] = item['vip_price']
					yzjItem['original_price'] = item['original_price']
					# yzjItem['brand_area_start_at'] = item['brand_area_start_at']
					# yzjItem['brand_area_end_at'] = item['brand_area_end_at']
					yzjItem['promotion_text_arr'] = item['promotion_text_arr']
					# yzjItem['redirect_brand_area_id'] = item['redirect_brand_area_id']
					yzjItem['zhuanchang_title'] = response.request.meta['cate']['zhuanchang_title']
					yzjItem['cate_title'] = response.request.meta['cate']['cate_title']
					
					yield yzjItem

		except Exception, what :
			print "-----------",what
			



	


