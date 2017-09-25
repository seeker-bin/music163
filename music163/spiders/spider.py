import scrapy
import requests
from scrapy import Selector
from ..items import Music163Item
from ..items import Music163SingerItem


class MusicSpider(scrapy.Spider):
    name = 'musicspider'
    allowed_domain = ['http://music.163.com']
    start_urls = 'http://music.163.com/discover/artist/cat?id={gid}&initial={initial}'
    group_ids = (1001, 1002, 1003, 2001, 2002, 2003, 6001, 6002, 6003, 7001, 7002, 7003, 4001, 4002, 4003)
    referer = 'http://music.163.com'
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
    headers = {'User-Agent': user_agent, 'Referer': referer}

    def start_requests(self):
        for gid in self.group_ids:
            for i in range(65, 91):
                yield scrapy.Request(url=self.start_urls.format(gid=gid, initial=i), headers=self.headers, method='GET', callback=self.parse)

    def parse(self, response):
        lists = response.selector.xpath('//*[@id="m-artist-box"]/li')
        for info in lists:
            item = Music163SingerItem()
            try:
                item['singer'] = info.xpath('p/a[1]/text()').extract()[0]
                item['info_url'] = 'http://music.163.com' + info.xpath('p/a[1]/@href').extract()[0].lstrip()
                item['headimg'] = info.xpath('div/img/@src').extract()[0]
            except Exception:
                item['singer'] = info.xpath('a[1]/text()').extract()[0]
                item['info_url'] = 'http://music.163.com' + info.xpath('a[1]/@href').extract()[0]
            yield scrapy.Request(url=item['info_url'], headers=self.headers, method='GET', callback=self.singer_parse)
            # yield item

    def singer_parse(self, response):
        lists = response.selector.xpath('//ul[@class="f-hide"]/li')
        for music in lists:
            music_url = 'http://music.163.com' + music.xpath('a/@href').extract()[0]
            yield scrapy.Request(url=music_url, headers=self.headers, method='GET', callback=self.music_parse)

    def music_parse(self, response):
        item = Music163Item()
        try:
            item['name'] = response.selector.xpath('//em[@class="f-ff2"]/text()').extract()[0]
            item['url'] = 'http://music.163.com/song?id=' + response.selector.xpath('//div[@id="content-operation"]/@data-rid').extract()[0]
            item['movie'] = 'http://music.163.com' + response.selector.xpath('//div[@class="tit"]/a/@href').extract()[0]
            item['singer'] = response.selector.xpath('//div[@class="cnt"]/p[1]/span/a/text()').extract()[0]
            item['album'] = response.selector.xpath('//div[@class="cnt"]/p[2]/a/text()').extract()[0]
            item['album_url'] = response.selector.xpath('//div[@class="cnt"]/p[2]/a/@href').extract()[0]
            item['comments'] = response.selector.xpath('//span[@class="sub s-fc3"]/span/text()').extract()[0]
        except Exception:
            item['name'] = response.selector.xpath('//em[@class="f-ff2"]/text()').extract()[0]
            item['url'] = 'http://music.163.com/#/song?id=' + response.selector.xpath('//div[@id="content-operation"]/@data-rid').extract()[0]
            item['singer'] = response.selector.xpath('//div[@class="cnt"]/p[1]/span/a/text()').extract()[0]
            item['album'] = response.selector.xpath('//div[@class="cnt"]/p[2]/a/text()').extract()[0]
            item['album_url'] = response.selector.xpath('//div[@class="cnt"]/p[2]/a/@href').extract()[0]
            item['comments'] = response.selector.xpath('//span[@class="sub s-fc3"]/span/text()').extract()[0]
        yield item