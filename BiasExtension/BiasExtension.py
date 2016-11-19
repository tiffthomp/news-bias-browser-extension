from lxml import html
import requests
import csv

def scrapeAllSides(categoryFilter='Unknown'):
    newsSourceTypeDictionary = {'Author':'1','News Media':'2','Think Tank / Policy Group':'3','Unknown':'All'}
    outputRows = []
    url = 'http://www.allsides.com/bias/bias-ratings?field_news_source_type_tid=' + newsSourceTypeDictionary[categoryFilter] + '&field_news_bias_nid=1&field_featured_bias_rating_value=All&title='
    page = requests.get(url)
    tree = html.fromstring(page.content)
    tableRows = tree.xpath('//tr')
    for tableRow in tableRows:
        newsSourceName = ''.join(tableRow.xpath('td[@class="views-field views-field-title source-title"]/a/text()'))
        if '(cartoonist)' in newsSourceName:
            newsSourceName = newsSourceName[0:(len(newsSourceName)-13)]
            newsSourceCategory = 'Cartoonist'
        else:
            newsSourceCategory = categoryFilter
        newsSourceURL = 'http://www.allsides.com' + ''.join(tableRow.xpath('td[@class="views-field views-field-title source-title"]/a/@href'))
        biasRatingHREF = ''.join(tableRow.xpath('td[@class="views-field views-field-field-bias-image"]/a/@href'))
        biasRating = biasRatingHREF[6:]
        biasRatingURL = 'http://www.allsides.com' + biasRatingHREF  
        outputRows.append({'Name':newsSourceName,'Category':newsSourceCategory,'URL':newsSourceURL,'Rating':biasRating,'Rating URL':biasRatingURL})
    with open('allsides.csv','w',encoding='utf8',newline='') as outputFile:
        writer = csv.DictWriter(outputFile,outputRows[0].keys())
        writer.writeheader()
        writer.writerows(outputRows)

scrapeAllSides('News Media')        # Accepts 'Author','News Media', 'Think Tank / Policy Group', 'Unknown'

# Error handling for invalid categoryFilter parameter
# Throws unicode encoding error
# CSV output wipes over previous allsides.csv file (need to iterate through dict)
# Remove biasRatingURL