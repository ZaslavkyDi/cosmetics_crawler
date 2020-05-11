from scrapy import cmdline

spider_name = 'cosmetic_com_ua'


def run():
    cmdline.execute(f"scrapy crawl {spider_name}".split())


if __name__ == '__main__':
    run()
