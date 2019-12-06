titles = []
imgs = []
list_hemispheres = ['Cerberus Hemisphere Enhanced', 'Schiaparelli Hemisphere Enhanced', 'Syrtis Major Hemisphere Enhanced', 'Valles Marineris Hemisphere Enhanced']


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