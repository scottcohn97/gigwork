## Creating a loop to scrape from all pages

news_title = []
news_source = []
news_link = []

#pages = [str(i) for i in range(1,371)]

reqs = 0

start_time = time()

for url in url_list:
    
    full_url = 'https://web.archive.org/web/'+url
    
    #open page
    try:
        pg = rq.get(full_url).text
    except urllib.error.HTTPError as e:
        print('Error: {}'.format(e))
    except urllib.error.URLError as e:
        print('Error: {}'.format(e.reason))
        
    sleep(randint(10,20))
    reqs +=1
    
    # Calculate elapsed time between requests
    elapsed_time = time() - start_time
    print('Request: {}; Frequency: {} requests/s'.format(reqs,reqs/elapsed_time))
    

    
    #Break once the max pages is reached
    if reqs > len(url_list):
        warn('No. of requests was greater than expected')
        break
        
    # parse html using beautifulsoup and store in soup
    soup = bs(pg,'html.parser')
    
    #find all news containers
    articles = soup.find_all('article')
    
    # parse through news containers to get info
    for article in articles:
        try:
            
            if article != None:
                #title and link
                if article.find_all('h2') != None:
                    #get news title
                    title = article.find_all('h2')[1].a.text 
                    #get individual news article link
                    link = article.find_all('h2')[1].a['href'] 
                else:
                    title = 'N/A'
                    link = 'N/A'
                # source
                source = 'NBC News'

            # Append data elements to lists
            news_title.append(title)
            news_source.append(source)
            news_link.append(link)
        except:
            e = sys.exc_info()[0]
            print(e)
 
 ## Creating a loop to scrape summary from links

news_summary = []
summ_link = []

reqs = 0

start_time = time()

for url in news_link:
    
    #open page
    try:
        pg = rq.get(url).text
    except urllib.error.HTTPError as e:
        print('Error: {}'.format(e))
    except urllib.error.URLError as e:
        print('Error: {}'.format(e.reason))
        
    sleep(randint(10,20))
    reqs +=1
    
    # Calculate elapsed time between requests
    elapsed_time = time() - start_time
    print('Request: {}; Frequency: {} requests/s'.format(reqs,reqs/elapsed_time))
    

    
    #Break once the max pages is reached
    if reqs > len(news_link):
        warn('No. of requests was greater than expected')
        break
        
    # parse html using beautifulsoup and store in soup
    soup = bs(pg,'html.parser')
    
    #find all news containers
    article = soup.find('div',attrs={'class':'article container___2EGEI'})
    try:
        if article.div != None:
            summ = article.div.text
        else:
            summ = 'N/A'
        
        news_summary.append(summ)
        summ_link.append(url)
    except:
        e = sys.exc_info()[0]
        print(e)