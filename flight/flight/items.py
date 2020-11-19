# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FlightItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ScheduleItem(scrapy.Item):
    dcityname = scrapy.Field()
    dcity = scrapy.Field()
    acityname = scrapy.Field()
    acity = scrapy.Field()


class Airline(scrapy.Item):
    name = scrapy.Field()
    logo = scrapy.Field()


class LowestPrice(scrapy.Item):
    # airlineName = scrapy.Field()
    flightNumber = scrapy.Field()
    # flightId = scrapy.Field()

    acity = scrapy.Field()
    acityName = scrapy.Field()
    arrivalDate = scrapy.Field()
    aairport = scrapy.Field()
    dcity = scrapy.Field()
    dcityName = scrapy.Field()
    departureDate = scrapy.Field()
    dairport = scrapy.Field()

    price = scrapy.Field()
    rate = scrapy.Field()

    url = scrapy.Field()
