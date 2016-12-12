import scrapy
from bs4 import BeautifulSoup

class NatureJobsSpider(scrapy.Spider):
    name = "nature_jobs_spider.py"
    visited = []
    
    def start_requests(self):
        
        urls = ['http://www.nature.com/naturejobs/science/jobs?']
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.get_job_ads)
            
    def get_job_ads(self, response):
        for link in response.css('div.search-results ul.jobs-list.regular li.job div.job-details h3 a::attr(href)').extract():
            url = 'http://www.nature.com' + link
            if not url in self.visited:
                self.visited.append(url)
                yield scrapy.Request(url=url, callback=self.parse)
            
        next_page = response.xpath('//a[contains(@class, "next_page")]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.get_job_ads)
            
    def parse(self, response):
        details = response.css('div#extranav dl.cleared')
        content = response.css('div#content.page-content')
        yield {
                'employer': details.xpath("dt[text()='Employer']/following::dd[1]/a/text()").extract_first(),
                'website': details.xpath("dt[text()='Website']/following::dd[1]/a/text()").extract_first(),
                'location': details.xpath("dt[text()='Location']/following::dd[1]/ul/li/text()").extract_first(),
                'posted': details.xpath("dt[text()='Posted']/following::dd[1]/text()").extract_first(),
                'expires': details.xpath("dt[text()='Expires']/following::dd[1]/text()").extract_first(),
                'job_type': details.xpath("dt[text()='Job type']/following::dd[1]/a/text()").extract_first(),
                'salary': details.xpath("dt[text()='Salary']/following::dd[1]/text()").extract_first(),
                'qualifications': details.xpath("dt[text()='Qualifications']/following::dd[1]/a/text()").extract_first(),
                'employment_type': details.xpath("dt[text()='Employment type']/following::dd[1]/a/text()").extract_first(),
                'job_hours': details.xpath("dt[text()='Job hours']/following::dd[1]/a/text()").extract_first(),
                'job_title': content.css("h1.job-title.heading::text").extract_first().strip('\n '),
                'job_description': BeautifulSoup(content.xpath("//div[contains(@class, 'job-description')]").extract()[0], 'lxml').get_text()
            }
            
