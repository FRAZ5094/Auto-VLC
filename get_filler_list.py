import requests
from bs4 import BeautifulSoup

name="bleach"
base_url="https://www.animefillerlist.com/shows/"
headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.191"}
def get_filler_list(anime_name):
    url=base_url+anime_name
    page=requests.get(url,headers=headers)
    soup=BeautifulSoup(page.content,"lxml")
    cannon_soup=[]
    cannon_soup+=soup.find_all("tr",class_="mixed_canon/filler odd")+soup.find_all("tr",class_="mixed_canon/filler even")+soup.find_all("tr",class_="manga_canon even")+soup.find_all("tr",class_="manga_canon odd")

    cannon_episodes=[]
    for tag in cannon_soup:
        ep=tag["id"]
        index=ep.find("-")
        ep=int(ep[index+1:])
        cannon_episodes.append(ep)

    cannon_episodes.sort(key=lambda x: int(x))
    return cannon_episodes



if __name__=="__main__":
    cannon_episodes=get_filler_list(name)
    print(cannon_episodes)