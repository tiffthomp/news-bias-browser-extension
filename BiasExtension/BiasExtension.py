from lxml import html
import requests
import csv

def scrapeAllSides():
    newsSourceTypeDictionary = {'Author':'1','News Media':'2','Think Tank / Policy Group':'3'}
    for category, newsSourceTypeTID in newsSourceTypeDictionary.items():
        outputRows = []
        url = 'http://www.allsides.com/bias/bias-ratings?field_news_source_type_tid=' + newsSourceTypeTID + '&field_news_bias_nid=1&field_featured_bias_rating_value=All&title='
        page = requests.get(url)
        tree = html.fromstring(page.content)
        tableRows = tree.xpath('//tr')
        for tableRow in tableRows:
            newsSourceName = ''.join(tableRow.xpath('td[@class="views-field views-field-title source-title"]/a/text()'))
            if '(cartoonist)' in newsSourceName:
                newsSourceName = newsSourceName[0:(len(newsSourceName)-13)]
                newsSourceCategory = 'Cartoonist'
            else:
                newsSourceCategory = category
            newsSourceURL = 'http://www.allsides.com' + ''.join(tableRow.xpath('td[@class="views-field views-field-title source-title"]/a/@href'))
            biasRating = ''.join(tableRow.xpath('td[@class="views-field views-field-field-bias-image"]/a/@href'))[6:]
            outputRows.append({'Name':newsSourceName,'Category':newsSourceCategory,'URL':newsSourceURL,'Rating':biasRating})
        with open('allsides_' + newsSourceTypeTID + '.csv','w',encoding='utf8',newline='') as outputFile:
            writer = csv.DictWriter(outputFile,outputRows[0].keys())
            writer.writeheader()
            writer.writerows(outputRows)

scrapeAllSides()

# Error handling for invalid categoryFilter parameter
# Throws unicode encoding error
# scrapeAllSides() no longer accepts parameter; now iterates through dictionary
# Outputs multiple CSV files; needs to append to a single CSV