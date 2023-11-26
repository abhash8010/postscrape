import scrapy
import os


class MySpider(scrapy.Spider):
    name = 'my_spider'
    start_urls = [
        "https://support.vanguard.com/tutorials/automatic-investments",
        "https://support.vanguard.com/tutorials/change-of-address",
        "https://support.vanguard.com/tutorials/add-beneficiary",
        "https://support.vanguard.com/tutorials/authenticate-bank"
    ]

    custom_settings = {
        'FEED_URI': 'output.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def __init__(self, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        if os.path.exists('output.json'):
            os.remove('output.json')

    def parse(self, response):
        main_content = response.css('main')
        title = response.css('h1::text').get()
        elements = main_content.css('h2, p')
        current_h2 = None
        current_p_texts = []

        for element in elements:
            if element.root.tag == 'h2':
                if current_h2 is not None:
                    # Yield the previous section when a new h2 is encountered
                    yield {
                        'h1_text': title,
                        'h2_text': current_h2,
                        'p_texts': current_p_texts
                    }
                    current_p_texts = []  # Reset for the next section

                current_h2 = element.css('::text').get()

            elif element.root.tag == 'p':
                text_parts = element.css('*::text').getall()
                full_text = ' '.join(text_parts).strip()
                current_p_texts.append(full_text)

        # Yield the last section after the loop
        if current_h2 is not None:
            yield {
                'h1_text': title,
                'h2_text': current_h2,
                'p_texts': current_p_texts
            }
