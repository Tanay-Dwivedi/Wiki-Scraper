import wikipedia as wp

query = "Hand_scraper"
wp_page = wp.page(query)
list_img_urls = wp_page.images
print(list_img_urls)