# Scrapy settings for homecenter_tracker project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import os

from dotenv import load_dotenv

load_dotenv(override=True)

## Env vars:

DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PW = os.environ.get("DB_PW")
DB_NAME = os.environ.get("DB_NAME")
PROXY_USER = os.environ.get("PROXY_USER")
PROXY_PASS = os.environ.get("PROXY_PASS")
PROXY_ENDPOINT = os.environ.get("PROXY_ENDPOINT")
PROXY_PORT = os.environ.get("PROXY_PORT")
SCRAPEOPS_API_KEY = os.environ.get("SCRAPEOPS_API_KEY")
SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT = "https://headers.scrapeops.io/v1/user-agents"
SCRAPEOPS_FAKE_HEADERS_ENDPOINT = "https://headers.scrapeops.io/v1/browser-headers"

BOT_NAME = "homecenter_tracker"

SPIDER_MODULES = ["homecenter_tracker.spiders"]
NEWSPIDER_MODULE = "homecenter_tracker.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "homecenter_tracker (+http://www.yourdomain.com)"
SCRAPEOPS_FAKE_USER_AGENT_ENABLED = True
SCRAPEOPS_FAKE_BROWSER_HEADER_ENABLED = True
SCRAPEOPS_NUM_RESULTS = 5


# PROXY_USER = "spa0wxxak4"
# PROXY_PASS = "3vCzdCEiB57mmhy1~x"
# PROXY_ENDPOINT = "http://gate.smartproxy.com"
# PROXY_PORT = "7000"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "homecenter_tracker.middlewares.ScrapeOpsFakeUserAgentMiddleware": 540,
    "homecenter_tracker.middlewares.ScrapeOpsFakeBrowserHeaderAgentMiddleware": 543,
    "homecenter_tracker.middlewares.ProxyMiddleware": 350,
    "scrapeops_scrapy.middleware.retry.RetryMiddleware": 550,
    "scrapy.downloadermiddlewares.retry.RetryMiddleware": None,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    "homecenter_tracker.middlewares.HomecenterTrackerDownloaderMiddleware": 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
    "scrapeops_scrapy.extension.ScrapeOpsMonitor": 500,
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "homecenter_tracker.pipelines.HomecenterTrackerPipeline": 300,
    "homecenter_tracker.pipelines.SaveToPostgresPipeline": 310,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
# CLOSESPIDER_PAGECOUNT = 3
