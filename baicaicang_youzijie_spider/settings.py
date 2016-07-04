# -*- coding: utf-8 -*-

# Scrapy settings for baicaicang_youzijie_spider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'baicaicang_youzijie_spider'

SPIDER_MODULES = ['baicaicang_youzijie_spider.spiders']
NEWSPIDER_MODULE = 'baicaicang_youzijie_spider.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'baicaicang_youzijie_spider (+http://www.yourdomain.com)'

# ITEM_PIPELINES = {
#     'baicaicang_youzijie_spider.pipelines.HandleResult': 300,
# }

EXTENSIONS = {
    'baicaicang_youzijie_spider.pipelines.HandleResult': 300,
}