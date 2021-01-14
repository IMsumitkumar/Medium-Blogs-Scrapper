try:     
    import requests
    from bs4 import BeautifulSoup as bs4
    from urllib.request import urlopen, Request
    from datetime import datetime
    import numpy as np
    import pandas as pd
    np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
except ModuleNotFoundError:
    print("Install dependencies from requirements.txt")
except Exception as e:
    print(e)


def fetch_links(request_url: str, tag: str):
    try:
        uClinet = urlopen(request_url)
        medium_page = uClinet.read()
        uClinet.read()

        page_beautify = bs4(medium_page, "html.parser")
        
        big_boxes = page_beautify.find_all("div", {"class":"js-postListHandle"})
        
        a = []
        b = []
        c = []
        d = []
        e = []
        

        for box in big_boxes[:10]:

            dt = datetime.now()
            date = dt.strftime('%Y-%m-%d')

            try:
                name_section = box.find_all("div",{"class":"postMetaInline-authorLockup"})
                for name in name_section:
                    try:
                        author_name = name.a.text
                    except:
                        author_name = "Missing"
                    try:
                        post_date = name.div.a.text
                    except:
                        post_date = "Missing"
                    try:
                        reading_time = name.find("span",{"class":"readingTime"})['title']
                    except:
                        reading_time = "Missing"
                        
                    a.append(author_name)
                    a.append(post_date)
                    a.append(reading_time)
                    a.append(tag)
                    
                    
            except Exception as e:
                print(e)



            try:
                claps_section = box.find_all("span",{"class":"js-actionMultirecommendCount"})
                for claps in claps_section:
                    try:
                        clap = claps.text
                    except:
                        clap = "Missing"
                    
                    b.append(clap)
            except Exception as e:
                print(e)
                
            
            try:
                responses = box.find_all("div",{"class":"buttonSet"})
                for response in responses:
                    try:
                        response_per_post = response.a.text
                    except:
                        response_per_post = "Missing"
                        
                    c.append(response_per_post)
            except Exception as e:
                print(e)

                
            try:
                titles = box.find_all("h3",{"class":"graf--title"})
                for title in titles:
                    try:
                        page_title = title.text
                    except:
                        page_title = "Missing"
                    

                    d.append(page_title)
            except Exception as e:
                print(e)

            try:
                desc = box.find_all("div",{"class":"postArticle-readMore"})
                for dec in desc:
                    post_tag = dec.find('a')
                    try:
                        post_link = post_tag.attrs['href']
                    except:
                        post_link = "Missing"
                    
                    post_content = requests.get(post_link)
                    beautify_single_post = bs4(post_content.text, "html.parser")

                    try:
                        blog_html = beautify_single_post.find("div",{"class":"s"})
                    except:
                        blog_html = "Missing"
                        
                    e.append(post_link)
                    e.append(blog_html)
                        
            except Exception as e:
                print(e)
                print("Tag not Found! Try another One.")
                
            
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        d = np.array(d)
        e = np.array(e)

        a = pd.DataFrame(a.reshape(10,4))
        b = pd.DataFrame(b.reshape(10,1))
        c = pd.DataFrame(c.reshape(10,1))
        d = pd.DataFrame(d.reshape(10,1))
        e = pd.DataFrame(e.reshape(10,2))
        
        frames = [a,b,c,d,e]
        data = pd.concat(frames, axis=1)
        
        return data
        

    except Exception as e:
        print(e)


if __name__ == '__main__':
    search_url = "https://medium.com/search?q={a}"
    try:
        query = str(input("Enter Search string:"))
    except Exception as e:
        print(e)
    query = query.replace(' ', '+')
    tag = query
    search_url = search_url.format(a=query)
    req = Request(search_url, headers={'User-Agent': 'Mozilla/5.0'})
    
    data = fetch_links(request_url=req, tag=tag)
    data.columns = ['Creator', 'post_date', 'read_time', 'tag', 'claps', 'responses', 'Title', 'post_link', 'blog_html']


    print(data)

