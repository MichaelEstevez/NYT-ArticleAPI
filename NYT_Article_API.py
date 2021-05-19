#importing 
import requests, pprint, time, pathlib, pickle, pandas, matplotlib



#setting up basics for getting response objects  
API_KEY='RqTkkGK55OY2L1hGMWEwizPWRH0FZmNs'
base_url='https://api.nytimes.com/svc/search/v2/articlesearch.json?q='
parameters={'q':'cryptocurrency' , 'api-key': API_KEY, 'fq':'document_type:("article")'}



#making new directory to store pickled files 
path = pathlib.Path.cwd()
NYTimes_pubdates = path/"pickled_files"
NYTimes_pubdates.mkdir(exist_ok = True)




# parsing through the articles to get their publication dates 
for i in range(92):
    parameters['page'] = i      #this will update the page we're parsing thru 
    pg_num = i 
    file_name = f"pub_dates{pg_num}"
    response_parsing = requests.get(base_url,params=parameters)
    content_parsing = response_parsing.json()
    pub_date = []
    for d in content_parsing['response']['docs']:               
        pub_date.append(d['pub_date'])
        with open(f"pickled_files/{file_name}",'wb') as p_file:             #storing each pages publication date information into a pickle file
            pickle.dump(pub_date,p_file)
        time.sleep(1)                                                       #setting a time.sleep() to avoid hitting the API too many times 



#going through all pickled files to create a master list of dates 
master_publist = []

cwd = pathlib.Path.cwd()
nytimes_pub_dir = cwd/"pickled_files"

for i in nytimes_pub_dir.iterdir():
    with open(i,'rb') as pub_file:
        pds = pickle.load(pub_file)
        for pd in pds: 
            year_date = pd[0:4]         #slicing to only include the publication year (transformation)
            master_publist.append(year_date)
master_publist.sort()



#creating a dataframe with pandas to store master_publist and create a bar graph 
dict_pubdate = {i:master_publist.count(i) for i in master_publist}     #creating a dictionary, keys are the year, values are the # of articles written in that year
df = pandas.DataFrame(list(dict_pubdate.items()), columns=['Years','# of Articles']) 
years_graph = df.plot.bar(x='Years',y='# of Articles', rot=0)
print(years_graph)
