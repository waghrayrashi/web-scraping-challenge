# Converted the Jupyter Notebook code into Python code
# Dependencies and Setup
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import datetime as dt

# Set Executable Path & Initialize Chrome Browser
executable_path = {"executable_path": "./chromedriver.exe"}
browser = Browser("chrome", **executable_path)


# Scrape title and paragraph from NASA Mars News Site
def mars_news(browser):
    # Visit the NASA Mars News Site
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)

    # Get the first list item & wait half a second if not immediately present
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=0.5)
    
    news_html = browser.html
    news_soup = bs(news_html, "html.parser")

    # Parse Results HTML with BeautifulSoup
    # Find Everything Inside:
    #   <ul class="item_list">
    #     <li class="slide">
    try:
        slide_element = news_soup.select_one("ul.item_list li.slide")
        slide_element.find("div", class_="content_title")

        # Scrape the Latest News Title
        # Use Parent Element to Find First <a> Tag and Save it as news_title
        news_title = slide_element.find("div", class_="content_title").get_text()

        news_paragraph = slide_element.find("div", class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
    # Close the browser after scraping
    browser.quit()
    
    # Return results
    return news_title, news_paragraph

# Scrape the Featured Image from NASA JPL (Jet Propulsion Laboratory) Mars Space Images
def featured_image(browser):
    # Visit the NASA JPL website
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

    # Ask Splinter to: 1) Go to the website 2) Click the button with class name = full_image
    # <button class="full_image">Full Image</button>
    full_image_button = browser.find_by_id("full_image")
    full_image_button.click()

    # Find "More Info" button and click It
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_element = browser.find_link_by_partial_text("more info")
    more_info_element.click()

    # Parse results HTML with BeautifulSoup
    image_html = browser.html
    image_soup = bs(image_html, "html.parser")

    img = image_soup.select_one("figure.lede a img")
    try:
        img_url = img.get("src")
    except AttributeError:
        return None 
    # Use Base URL to Create Absolute URL
    featured_image_url = f"https://www.jpl.nasa.gov{img_url}"
    
    # Close the browser after scraping
    browser.quit()
    
    # Return results
    return featured_image_url

# Scrape Mars Weather Twitter Account
def twitter_weather(browser):
    # Visit the Mars Weather Twitter Account
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)
    
    # Parse Results HTML with BeautifulSoup
    twitter_html = browser.html
    twitter_soup = bs(twitter_html, "html.parser")
    
    # Find a Tweet with the data-name `Mars Weather`
    mars_weather_tweet = twitter_soup.find("div", 
                                       attrs={
                                           "class": "tweet", 
                                            "data-name": "Mars Weather"
                                        })
    # Search Within Tweet for <p> Tag Containing Tweet Text
    mars_weather = mars_weather_tweet.find("p", "tweet-text").get_text()
    
    # Close the browser after scraping
    browser.quit()
    
    # Return results
    return mars_weather

# Scrape Mars Facts
def mars_facts():
    # Visit the Mars Facts Site Using Pandas to Read
    try:
        mars_df = pd.read_html("https://space-facts.com/mars/")[0]
    except BaseException:
        return None
    mars_df.columns=["Description", "Value"]
    mars_df.set_index("Description", inplace=True)
    
    # Close the browser after scraping
    browser.quit()
    
    # Return results
    return mars_df.to_html(classes="table table-striped")

# Scrape Mars Hemispheres 
def hemisphere(browser):
    # Visit the USGS Astrogeology Science Center Site
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    # Create an empty list to store the image url's
    hemisphere_image_urls = []

    # Get a list of all the hemispheres
    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}
        
        # Find the element on each loop to avoid a stale element exception
        browser.find_by_css("a.product-item h3")[item].click()
        
        # Find the sample image anchor tag & extract <href>
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]
        
        # Get hemisphere title
        hemisphere["title"] = browser.find_by_css("h2.title").text
        
        # Append the hemisphere object to teh list of url's
        hemisphere_image_urls.append(hemisphere)
        
        # Navigate back
        browser.back()
    return hemisphere_image_urls

# Helper function
def scrape_hemisphere(html_text):
    hemisphere_soup = bs(html_text, "html.parser")
    try: 
        title_element = hemisphere_soup.find("h2", class_="title").get_text()
        sample_element = hemisphere_soup.find("a", text="Sample").get("href")
    except AttributeError:
        title_element = None
        sample_element = None 
    hemisphere = {
        "title": title_element,
        "img_url": sample_element
    }
    return hemisphere


# Main scraping function
def scrape_all():
    executable_path = {"executable_path": "./chromedriver"}
    browser = Browser("chrome", **executable_path)
    news_title, news_paragraph = mars_news(browser)
    featured_image_url = featured_image(browser)
    mars_weather = twitter_weather(browser)
    facts = mars_facts()
    hemisphere_image_urls = hemisphere(browser)
    timestamp = dt.datetime.now()

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image_url,
        "weather": mars_weather,
        "facts": facts,
        "hemispheres": hemisphere_image_urls,
        "last_modified": timestamp
    }
    browser.quit()
    return data 

if __name__ == "__main__":
    print(scrape_all())