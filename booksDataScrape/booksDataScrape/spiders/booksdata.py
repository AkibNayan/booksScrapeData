import scrapy


class BooksdataSpider(scrapy.Spider):
    name = "booksdata"
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        cards = response.css("article.product_pod")
        for card in cards:
            title = card.css("h3 > a::text").get()
            #print(title)
            rating = card.css("p.star-rating::attr(class)").get().split(" ")[-1]
            #print(rating)
            price = card.css("p.price_color::text").get()
            #print(price)
            availability = card.xpath("//p[@class='instock availability']").get()
            if len(availability) > 0:
                availability = "In Stock"
            else:
                availability = "Out of Stock"
            #print(availability)
            image = card.css("div.image_container > a > img::attr(src)").get().replace(
                "media", "https://books.toscrape.com/media")
            #print(image)
            yield {
                "title": title,
                "rating": rating,
                "price": price,
                "availability": availability,
                "image": image
            }
            next_page = response.css("li.next > a::attr(href)").get()
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)
