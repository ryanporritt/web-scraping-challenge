from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

# Set Executable Path & Initialize Chrome Browser
def init_browser():
    executable_path = {"executable_path": "C:/chromedrv/chromedriver.exe"}
    return Browser('chrome', **executable_path, headless=False)

browser = init_browser()

def mars_news(browser):
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    #let the browser load
    time.sleep(1)

    # Get first list item and wait half a second if not immediately present
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=0.5)


    html = browser.html
    news_soup = bs(html, 'html.parser')
    
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        news_title = slide_elem.find("div", class_="content_title").get_text()
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()
    except AttributeError:
        return "Opps Couldn't find what you were looking for.", None
    return news_title, news_p

def featured_image(browser):
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    #let the browser load
    time.sleep(1)
    
    #since we are pulling from a external source use a try and except
    try:
        full_image_elem = browser.find_by_id('full_image')
        full_image_elem.click()
        browser.is_element_present_by_text('more info', wait_time=1)
        more_info_element = browser.find_link_by_partial_text('more info')
        more_info_element.click()
    except:
        return "Opps Couldn't find what you were looking for."

    html = browser.html
    img_soup = bs(html, "html.parser")

    #now we are on the right page scrape for image
    try:
        img_url_rel = img_soup.select_one('figure.lede a img').get('src')
        image_url = 'https://www.jpl.nasa.gov' + img_url_rel
    except:
        return "Opps Couldn't find what you were looking for."
    
    #return the results
    return image_url


def weather(browser):
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    html = browser.html
    mars_weather_soup = bs(html, "html.parser")

    try:
        mars_weather_tweet = mars_weather_soup.find('div', attrs={"class": "tweet", "data-name" : "Mars Weather"})
        mars_weather = mars_weather_tweet.find('p', 'tweet-text').get_text()    
    except:
        return "Opps Couldn't find what you were looking for."
    return mars_weather

def concatenate_list_data(list):
        result= ''
        for element in list:
            result += str(element)
        return result

"""
def mars_facts(browser):
    url = "https://space-facts.com/mars/"
    browser.visit(url)

    html = browser.html
    mars_facts_soup = bs(html, "html.parser")

    try:
        sidebar = mars_facts_soup.find('div', class_='entry-content clearfix')
        categories = sidebar.find_all('li')    
    except:
        return "Opps Couldn't find what you were looking for."
    
    content = []
    titles = []

    for category in categories:
        title = category.find('strong')
        titles.append(title)
        content.append(category.find('a'))

    tables = pd.read_html(url)
    df = tables[0]

    df.columns = ['Mars', 'Measurements']
    html_table = df.to_html()
    html_table = html_table.split(" ")
    html_table[-1]
    html_end = html_table[-1].split("\n")
    html_end = html_end[0]
    html_table = [html_table[i] for i in range(3,301)]
    
    html_table = concatenate_list_data(html_table)
    html_table = html_table + html_end

    html_table.replace('\n', '')
    return html_table
"""



def hemisphere(browser):
    list_hemispheres = ['Cerberus Hemisphere Enhanced', 'Schiaparelli Hemisphere Enhanced', 'Syrtis Major Hemisphere Enhanced', 'Valles Marineris Hemisphere Enhanced']
    titles = []
    imgs = []

    for element in list_hemispheres:
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        
        #let the browser load
        time.sleep(1)
        html = browser.html
        mars_hemispheres_soup = bs(html, 'html.parser')

        try:
            browser.click_link_by_partial_text(element)
        
        except:
            return "Opps Couldn't find what you were looking for."
            
        html = browser.html
        mars_hemispheres_soup = bs(html, 'html.parser')

        try:
            current_mars_hemisphere_title = mars_hemispheres_soup.find('h2', class_='title')
            current_mars_hemisphere_title = current_mars_hemisphere_title.get_text()
            
        except:
            return "Opps Couldn't find what you were looking for."

        current_mars_hemisphere_title = current_mars_hemisphere_title.split(" ")
        current_mars_hemisphere_title = current_mars_hemisphere_title[0] + " " + current_mars_hemisphere_title[1]
        
        ## current_mars_hemisphere_title ->
        titles.append(current_mars_hemisphere_title)
        try:
            current_mars_hemisphere_image = mars_hemispheres_soup.find('li')
            
        except:
            return "Opps Couldn't find what you were looking for." 
        
        current_mars_hemisphere_image = str(current_mars_hemisphere_image.prettify())
        current_mars_hemisphere_image = current_mars_hemisphere_image.split(" ")
        current_mars_hemisphere_href = current_mars_hemisphere_image[2]
        current_mars_hemisphere_img = current_mars_hemisphere_href.split("=")
        current_mars_hemisphere_img = current_mars_hemisphere_img[1]
        jpg_range = len(current_mars_hemisphere_img)
        current_mars_hemisphere_img = [current_mars_hemisphere_img[i] for i in range(1, (jpg_range - 1))]
        current_mars_hemisphere_img = concatenate_list_data(current_mars_hemisphere_img)

        ## current_mars_hemisphere_href ->
        imgs.append(current_mars_hemisphere_img)

    hemisphere_image_urls = []
    hemisphere_dict = {}

    for i in range(4):
        hemisphere_dict = {'title' : titles[i], 'img_url' : imgs[i]}
        hemisphere_image_urls.append(hemisphere_dict)

    return hemisphere_image_urls


def scrape_all():
    browser = init_browser()

    news_title, news_p = mars_news(browser)
    featured_img = featured_image(browser)
    mars_weather = weather(browser)
    #facts = mars_facts(browser)
    hemisphere_image_urls = hemisphere(browser)

    #split the dictionary here jinja having trouble
    first_hemisphere_title = hemisphere_image_urls[0]["title"]
    first_hemisphere_img = hemisphere_image_urls[0]['img_url']

    second_hemisphere_title = hemisphere_image_urls[1]["title"]
    second_hemisphere_img = hemisphere_image_urls[1]['img_url']

    third_hemisphere_title = hemisphere_image_urls[2]["title"]
    third_hemisphere_img = hemisphere_image_urls[2]['img_url']

    fourth_hemisphere_title = hemisphere_image_urls[3]["title"]
    fourth_hemisphere_img = hemisphere_image_urls[3]['img_url']


    #timestamp = dt.datetime.now()

    #close the browser
    browser.quit()

    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_img": featured_img,
        "weather": mars_weather,
        #"facts": facts,
        "first_hemisphere_title": first_hemisphere_title,
        "first_hemisphere_img": first_hemisphere_img,
        "second_hemisphere_title": second_hemisphere_title,
        "second_hemisphere_img": second_hemisphere_img,
        "third_hemisphere_title": third_hemisphere_title,
        "third_hemisphere_img": third_hemisphere_img,
        "fourth_hemisphere_title": fourth_hemisphere_title,
        "fourth_hemisphere_img": fourth_hemisphere_img,

        #"last_modified": timestamp
    }
    return mars_data 



if __name__ == "__main__":
    print(scrape_all())