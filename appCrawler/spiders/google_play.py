# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from appCrawler.items import GooglePlayItem
import re
id_regex = re.compile("id=([A-Za-z0-9._]*)")

class GooglePlaySpider(CrawlSpider):
    name = "google_play"
    allowed_domains = ["play.google.com"]
    start_urls = (
        'https://play.google.com/store/apps',
    )
    rules = (
        Rule(LinkExtractor(allow=('/store/apps/details\?')), follow=True, callback="parse_app"),
        Rule(LinkExtractor(allow=('/store/apps')), follow=True)
    )

    def parse_app(self, response):
        selector = Selector(response)
        item = GooglePlayItem()
        item["id"] = id_regex.findall(response.url)[0]
        item["url"] = response.url
        item["item_name"] = selector.xpath('//*[@class="document-title"]/div/text()').extract_first()
        item["updated"] = selector.xpath('//*[@itemprop="datePublished"]/text()').extract_first()
        item["author"] = selector.xpath('//*[@itemprop="author"]/a/span/text()').extract_first()
        item["file_size"] = selector.xpath('//*[@itemprop="fileSize"]/text()').extract_first()
        item["downloads"] = selector.xpath('//*[@itemprop="numDownloads"]/text()').extract_first()
        item["version"] = selector.xpath('//*[@itemprop="softwareVersion"]/text()').extract_first()
        item["compatibility"] = selector.xpath('//*[@itemprop="softwareVersion"]/text()').extract_first()
        item["content_rating"] = selector.xpath('//*[@itemprop="contentRating"]/text()').extract_first()
        item["author_link"] = selector.xpath('//*[@class="dev-link"]/@href').extract_first()
        item["genre"] = selector.xpath('//*[@itemprop="genre"]/text()').extract_first()
        item["price"] = selector.xpath('//*[@class="price buy id-track-click"]/span[2]/text()').extract_first()
        item["rating_value"] = selector.xpath('//*[@class="score"]/text()').extract_first()
        item["review_count"] = selector.xpath('//*[@class="reviews-num"]/text()').extract_first()
        item["description"] = selector.xpath('//*[@class="id-app-orig-desc"]//text()').extract_first()
        item["iap"] = selector.xpath('//*[@class="inapp-msg"]/text()').extract_first()
        item["developer_badge"] = selector.xpath('//*[@class="badge-title"]//text()').extract_first()
        item["address"] = selector.xpath('//*[@class="content physical-address"]/text()').extract_first()
        item["video_url"] = selector.xpath('//*[@class="play-action-container"]/@data-video-url').extract_first()
        item["developer_id"] = selector.xpath('//*[@itemprop="author"]/a/@href').extract_first()
        yield item
