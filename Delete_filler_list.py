import requests
from bs4 import BeautifulSoup
from glob import glob
import os 

base_url="https://www.animefillerlist.com/shows/"
headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.191"}
def get_filler_list():
    ans=input("what anime?: ")
    url=base_url+str(ans)
    page=requests.get(url,headers=headers)
    if page.ok:
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
    else:
        print("invalid anime name")
        return get_filler_list()


if __name__=="__main__":
    cannon_episodes=get_filler_list()
    max_e=max(cannon_episodes)
    all_e=list(range(1,max_e+1))
    filler_list=[]
    for ep in all_e:
        if ep not in cannon_episodes:
            filler_list.append(int(ep))
    print("filler episodes:\n")
    print(filler_list)
    ans=input("Delete all non-cannon episodes? (y/n): ")

    if ans=="y":
        ans2=input("enter video format (eg mp4): ")
        files=glob(f"*.{ans2}")
        for file in files:
            # print(type([int(i) for i in file.split() if i.isdigit()]))
            if [int(i) for i in file.split() if i.isdigit()][0] in filler_list:
                os.remove(file)
                print(f"removing {file}")

