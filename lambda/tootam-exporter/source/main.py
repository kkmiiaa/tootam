# encoding: utf-8

import json
import requests
    
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from scrape import Target, ScrapeSite, ScrapedItem

def lambda_handler(event, context):
    target = Target('./credential.json', '1eaFg_FPp6kT5pbLZS7jDgjQtXL8Uw8HFpV4aOUybuoI')

    for site in target.sites:
        print(site.site_name + ': ' + site.site_url)
        if (not site.enabled): 
            print(site.site_name + ' is disabled.')
        driver = setup_driver()
        login(driver, site)
        items = parse_site(driver, site)
        driver.quit()

        message = create_messages(site, items)
        post_line(message)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def setup_driver():
    service=Service(executable_path=ChromeDriverManager().install())
    driver=webdriver.Chrome(service=service)
    driver.implicitly_wait(30)
    return driver


def login(driver, site): 
    if site.login_url is None: 
        return None
    
    driver.get(site.login_url)
    id_input_tag = driver.find_element(By.CSS_SELECTOR, site.login_id_css)
    id_input_tag.send_keys(site.login_id)
    
    pass_input_tag = driver.find_element(By.CSS_SELECTOR, site.login_pass_css)
    pass_input_tag.send_keys(site.login_pass)

    submit_button_tag = driver.find_element(By.CSS_SELECTOR, site.submit_button_css)
    submit_button_tag.click()


def parse_site(driver, site):
    driver.get(site.site_url)

    list_el = driver.find_element(By.CSS_SELECTOR, site.list_css)
    items_el = list_el.find_elements(By.CSS_SELECTOR, site.item_css)[:site.item_count]

    scraped_items = []
    for item_el in items_el:
        url_el = item_el.find_element(By.CSS_SELECTOR, site.url_css)
        title_el = item_el.find_element(By.CSS_SELECTOR, site.title_css)
        scraped_items.append(ScrapedItem(title = title_el.text, url = url_el.get_attribute('href')))

    return scraped_items

def create_messages(site, items):

    contents = []
    for item in items:
        content = {
            "type": "text",
            "text": item.title,
            "action": {
                "type": "uri",
                "label": "action",
                "uri": item.url
            },
            "size": "xs",
            "wrap": True,
            "style": "normal",
            "weight": "bold",
            "margin": "lg"
        }
        contents.append(content)
            

    return {
        "type": "flex",
        "altText": site.site_name,
        "contents": {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": site.category,
                                "size": "xs",
                                "color": site.category_color,
                                "weight": "bold"
                            },
                            {
                                "type": "text",
                                "text": site.site_name,
                                "margin": "sm",
                                "size": "xxl",
                                "weight": "bold",
                                "wrap": True
                            },
                            {
                                "type": "text",
                                "text": site.site_url,
                                "color": "#aaaaaa",
                                "size": "xxs",
                                "margin": "xs"
                            }
                        ],
                        "action": {
                            "type": "uri",
                            "label": "action",
                            "uri": site.site_url
                        }
                    },
                    {
                        "type": "separator",
                        "margin": "xl"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": contents
                    },
                    {
                        "type": "separator",
                        "margin": "xl"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "margin": "md",
                        "contents": [
                            {
                                "type": "text",
                                "text": "送信日",
                                "size": "xs",
                                "color": "#aaaaaa",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": "2024/02/12",
                                "color": "#aaaaaa",
                                "size": "xs",
                                "align": "end"
                            }
                        ]
                    }
                ]
            },
            "styles": {
                "footer": {
                    "separator": True
                }
            }
        }
    }
    



def post_line(message):
    data = {
        'to': 'U8060276c4250063b1941ceeaa0bec14b', 
        'messages': [message]
    }
    headers = {
        'Authorization': 'Bearer +s5r0+nzdBRTE2LPxp3IM4+AhTlQf7tu6NSrGkidxCwiuCs1hBoqfx+J5T32k0cHy5+mAIT2bZacd7USrOKwpu7sXWpvDz/P2CknFUWm2KRFvFXz8lDxTZjk6T5yqJkDGiFOdMg43BHjvIvBZo5KrQdB04t89/1O/w1cDnyilFU=',
        'Content-Type': 'application/json'
    }
    
    response = requests.post('https://api.line.me/v2/bot/message/push', headers=headers, data=json.dumps(data))
