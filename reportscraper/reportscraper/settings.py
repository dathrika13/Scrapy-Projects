# Scrapy settings for reportscraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "reportscraper"

SPIDER_MODULES = ["reportscraper.spiders"]
NEWSPIDER_MODULE = "reportscraper.spiders"

# Don't obey robots.txt rules
ROBOTSTXT_OBEY = False

# Enable cookies if needed
COOKIES_ENABLED = True

# -------------------------
# SPIDER MIDDLEWARES
# -------------------------
SPIDER_MIDDLEWARES = {
   "reportscraper.middlewares.ReportscraperSpiderMiddleware": 543,
   # Remove Splash deduplication middleware (disabled)
   # 'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

# Use the default dupe filter (instead of SplashAwareDupeFilter)
DUPEFILTER_CLASS = 'scrapy.dupefilters.RFPDupeFilter'

# -------------------------
# DOWNLOADER MIDDLEWARES
# -------------------------
DOWNLOADER_MIDDLEWARES = {
    # Disable HTTP compression middleware if needed (optional)
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': None,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 120,
    # Remove Splash middlewares (disabled)
    # 'scrapy_splash.SplashCookiesMiddleware': 723,
    # 'scrapy_splash.SplashMiddleware': 725,
    # 'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

# If you are using a proxy, set it up here:
HTTP_PROXY = 'http://<proxy_address>:<port>'

# -------------------------
# DOWNLOAD & CONCURRENCY SETTINGS
# -------------------------
DOWNLOAD_DELAY = 2
DEPTH_LIMIT = 15  # Allow deeper crawling
LOG_LEVEL = 'DEBUG'  # Enable detailed logging

# -------------------------
# AUTOTHROTTLE SETTINGS
# -------------------------
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1    # Initial delay
AUTOTHROTTLE_MAX_DELAY = 10     # Maximum delay
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0  # Average number of requests in parallel
AUTOTHROTTLE_DEBUG = False

# -------------------------
# REMOVED SPLASH SETTINGS
# -------------------------
# Comment out or remove the following Splash-related settings:
# SPLASH_URL = 'http://localhost:8050'
# DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
# HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

# Other settings remain as needed:
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
