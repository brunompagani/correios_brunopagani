from pathlib import Path

# Scrapy settings for correios project

BOT_NAME = 'correios'

# Spider Gen
SPIDER_MODULES = ['correios.spiders']
NEWSPIDER_MODULE = 'correios.spiders'

#Caminhos
ROOT_PATH = Path()
OUTPUT_PATH = ROOT_PATH / 'output'
LOG_PATH = ROOT_PATH / 'logs'
if not LOG_PATH.exists() or not LOG_PATH.is_dir():
   LOG_PATH.mkdir()

# Logs
LOG_ENABLED = True
LOG_FILE = LOG_PATH / 'log_spiders.txt'
LOG_LEVEL = 'INFO'
LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Downloader Middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'correios.middlewares.RotateUserAgentMiddleware': 530,
   'correios.middlewares.CorreiosDownloaderMiddleware': 543,
}

# Item Pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'correios.pipelines.DuplicatesPipeline': 200,
   'correios.pipelines.LogsPipeline': 250,
   'correios.pipelines.UniqueKeyPipeline': 300,
   'correios.pipelines.ScrapedDatePipeline': 400,
   'correios.pipelines.MyOverwritePipeline': 450,
}

# User Agents para rotacionar
MY_USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; Trident/5.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0; MDDCJS)',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ',
]