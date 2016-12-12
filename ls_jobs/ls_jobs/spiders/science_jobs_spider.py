import scrapy
from bs4 import BeautifulSoup

class ScienceJobSpider(scrapy.Spider):
    name = "science_jobs_spider.py"

    def start_requests(self):
        urls = ['http://jobs.sciencecareers.org/jobs/biochemistry',
                'http://jobs.sciencecareers.org/jobs/bioinformatics',
                'http://jobs.sciencecareers.org/jobs/biology',
                'http://jobs.sciencecareers.org/jobs/biomedical-sciences',
                'http://jobs.sciencecareers.org/jobs/biophysics',
                'http://jobs.sciencecareers.org/jobs/biotechnology',
                'http://jobs.sciencecareers.org/jobs/cancer-research',
                'http://jobs.sciencecareers.org/jobs/cell-biology',
                'http://jobs.sciencecareers.org/jobs/chemistry',
                'http://jobs.sciencecareers.org/jobs/genetics',
                'http://jobs.sciencecareers.org/jobs/genomics',
                'http://jobs.sciencecareers.org/jobs/health-sciences',
                'http://jobs.sciencecareers.org/jobs/immunology',
                'http://jobs.sciencecareers.org/jobs/life-sciences',
                'http://jobs.sciencecareers.org/jobs/microbiology',
                'http://jobs.sciencecareers.org/jobs/molecular-biology',
                'http://jobs.sciencecareers.org/jobs/neuroscience',
                'http://jobs.sciencecareers.org/jobs/virology']
        for urrl in urls:
            field = urrl.split('/')[-1]
            global field
            yield scrapy.Request(url=urrl, callback=self.get_jobs)

## jobs in field
    def get_jobs(self, response):
        visited = dict()
        for link in response.css('li.lister__item.cf.lister__item--display-logo-in-listing h3.lister__header a::attr(href)').extract():
            link = 'http://jobs.sciencecareers.org' + link 
            if not(link in visited):
                visited[link] = ''
                yield scrapy.Request(url=link, callback=self.parse)
    
        next_page = response.xpath('//a[contains(@title, "Next page")]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.get_jobs)

    def parse(self, response):
        yield {
            'employer': response.css('dd.grid-item.three-fifths.portable-one-whole.palm-one-half span::text').extract_first(),
            'location': response.css('dl.grid div.cf.margin-bottom-5 dd.grid-item.three-fifths.portable-one-whole.palm-one-half::text').extract()[2].strip('\r\n\t\t\t\t'),
            'salary': response.css('dl.grid div.cf.margin-bottom-5 dd.grid-item.three-fifths.portable-one-whole.palm-one-half::text').extract()[3].strip('\r\n\t\t\t\t'),
            'posted': response.css('dd.grid-item.three-fifths.portable-one-whole.palm-one-half span::text').extract()[1],
            'job_type': response.css('dd.grid-item.three-fifths.portable-one-whole.palm-one-half a::text').extract()[-1],
            'job_title': response.css('h1::text').extract_first(),
            'job_description': BeautifulSoup(response.css('div.block.fix-text').extract_first()).get_text().strip('\r\n\t\t\t\t\t\t') + ' ' + field
            }


