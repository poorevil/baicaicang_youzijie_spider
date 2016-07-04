# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YouzijieItem(scrapy.Item):
    open_id = scrapy.Field()				#item_id
    name = scrapy.Field()					#名称
    picture = scrapy.Field()				#图片地址
    vip_price = scrapy.Field()				#柚子街价格
    original_price = scrapy.Field()			#原价
    brand_area_start_at = scrapy.Field()	#开始时间
    brand_area_end_at = scrapy.Field()		#结束时间
    promotion_text_arr = scrapy.Field()		#包邮
    # redirect_brand_area_id = scrapy.Field()	#专题id，0：不是专题，1：专题id
    cate_title = scrapy.Field()				#类目名称
    zhuanchang_title = scrapy.Field()       #专场名称


    
