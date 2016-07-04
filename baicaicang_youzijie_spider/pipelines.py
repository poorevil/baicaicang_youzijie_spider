#-*- coding:UTF-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BaicaicangYouzijieSpiderPipeline(object):
	def process_item(self, item, spider):
		return item

from scrapy import signals
import scrapy
import json
from datetime import datetime
from datetime import date

import urllib  
import urllib2

import datetime
import md5


#处理结果 扩展
class HandleResult(object):

	resultDict = {}		#结果集合map

	@classmethod
	def from_crawler(cls, crawler):
		# if not crawler.settings.getbool('MYEXT_ENABLED'):
		# 	raise NotConfigured

		# # get the number of items from settings

		# item_count = crawler.settings.getint('MYEXT_ITEMCOUNT', 1000)

		# instantiate the extension object

		ext = cls()

		# connect the extension object to signals
		crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
		crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
		crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)

		return ext

	def spider_opened(self, spider):
		print '============HandleResult===========spider_opened==================================='+spider.name

	def item_scraped(self, item, spider):
		
		print "-------item_scraped-------%s"%item

		if item['cate_title'] not in self.resultDict:
			self.resultDict[item['cate_title']] = []
			
		self.resultDict[item['cate_title']].append(item)


	def spider_closed(self, spider):
		print '============HandleResult===========spider_closed==================================='+spider.name

		for key in self.resultDict.keys():
			api_response = self.postResult(key,json.dumps(self.resultDict[key], cls=CJsonEncoder))
			# print "----------api_response------%s"%api_response

  
	def postResult(self,cate,jsonStr):
		secret = '67mmazghttZGwI8u'
		m1 = md5.new()
		m1.update('%s%s'%(secret,datetime.datetime.now().strftime('%Y/%m/%d')))
		key = m1.hexdigest()

		req = urllib2.Request('http://www.xxxxx.cn/index.php?g=api&m=goods&a=insertItems')
		data = {"appid":"20002","key":key,"cate":cate.encode('utf-8'),"data":jsonStr}
		data = urllib.urlencode(data)
		#enable cookie
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
		response = opener.open(req, data)
		return response.read()



class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        # if isinstance(obj, datetime):
        #     return obj.strftime('%Y-%m-%d %H:%M:%S')
        # elif isinstance(obj, date):
        #     return obj.strftime('%Y-%m-%d')
        # el

        if isinstance(obj, scrapy.item.Item):
            return dict(obj)
        else:
            return json.JSONEncoder.default(self, obj)



