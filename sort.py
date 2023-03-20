import os, json, random
import regex as re
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

path_to_sa = ''   #give path to sa accounts folder
folder_id = ""   #give any folder id
index_path = ""  #give path to save generated files

sa_files = [sa_file for sa_file in os.listdir(path_to_sa) if sa_file.endswith('.json')]

def service_account_rotate():
        global drive_service
        SCOPES = ['https://www.googleapis.com/auth/drive']
        
        service_account_info = json.load(open(f"{path_to_sa}{random.choice(sa_files)}"))
        creds=Credentials.from_service_account_info(
            service_account_info, scopes=SCOPES)
        print("service_account changed")
        drive_service = build('drive', 'v3', credentials=creds)

reg_tv="(?P<name>.+)[\.\s](?P<episode>[Ss][\d][\d][\d]?[Ee][\d][\d][\d]?|[Ss][\d][\d][\d]?[Ee][\d][\d][\d]?-[Ee]?[\d][\d][\d]?)[\.\s](?P<repack>REPACK)?.*(?P<resolution>2160p|1080[pi]|720[ip]|DVDRIP|DVDRip|DVD|576[ip]|480[pi]|568[pi]).*[\.\s](?P<typ>WEB-DL|WEBRip|WebRip|Web-Rip|WEB|REMUX|Remux|ReMUX|BluRay|Blu-ray|Bluray|BDRip|XVID|XviD).*[-][\s]?(?P<group>[^\s\[]+)(?P<rartv>\[rartv\]|[\s]?[\(\[].+[\)\]])?(?:\.mkv|\.mp4)"
reg_movie="(?P<name>.+)[\.\s][\(]?(?P<year>[\d]{4})[\)]?(?P<repack>REPACK)?.*[\.\s\(](?P<resolution>2160p|1080[pi]|720[ip]|DVDRIP|DVDRip|DVD|576[ip]|480[pi]|568[pi]).*[\.\s](?P<typ>WEB-DL|WEBRip|WebRip|Web-Rip|WEB|REMUX|Remux|BluRay|ReMUX|BluRay|Bluray|Blu-ray|BDRip|XVID|XviD|x265).*[-\s][\s]?(?P<group>[^\s\[\.\)]+)[\)]?(?:\.mkv|\.mp4)"
#https://regex101.com/r/IrULCH/1
#reg_tv_folder = "(?P<name>.+)[\.\s](?P<season>[Ss][\d][\d][\d]?|(?<pack>[Ss][\d][\d][\d\s]?-[Ss][\d][\d][\d]?))[\.\s](?P<repack>REPACK)?.*[\(]?(?P<resolution>2160p|1080[pi]|720[ip]|DVDRIP|DVDRip|DVD|576[ip]|480[pi]|568[pi]).*[\.\s](?P<typ>WEB-DL|WEBRip|WebRip|Web-Rip|REMUX|Remux|ReMUX|BluRay|BluRay|Blu-ray|Bluray|BDRip|XVID|XviD).*[-](?P<group>[^\s\[\)\(]+)[\)]?(?P<rartv>\[rartv\]|[\s]?[\(\[].+[\)\]])?" packs
reg_tv_folder = "(?P<name>.+)[\.\s](?P<season>[Ss][\d][\d][\d]?|(?<pack>[Ss][\d][\d][\d\s]?-[Ss][\d][\d][\d]?))[\.\s](?P<repack>REPACK)?.*[\(]?(?P<resolution>2160p|1080[pi]|720[ip]|DVDRIP|DVDRip|DVD|576[ip]|480[pi]|568[pi]).*[\.\s](?P<typ>WEB-DL|WEBRip|WebRip|Web-Rip|REMUX|Remux|ReMUX|BluRay|Blu-ray|Bluray|BDRip|XVID|XviD).*[-](?P<group>[^\s\[\)\(]+)[\)]?(?P<rartv>\[rartv\]|[\s]?[\(\[].+[\)\]])?"
#https://regex101.com/r/A32jXN/1
reg="(?:(?<webdl>WEB[-_. ]DL(?:mux)?|WEBDL|AmazonHD|iTunesHD|MaxdomeHD|NetflixU?HD|WebHD|[. ]WEB[. ](?:[xh][ .]?26[45]|DDP?5[. ]1)|[. ](?-i:WEB)$|(?:720|1080|2160)p[-. ]WEB[-. ]|[-. ]WEB[-. ](?:720|1080|2160)p|\b\s\/\sWEB\s\/\s\b|(?:AMZN|NF|DP)[. -]WEB[. -](?!Rip))|(?<webrip>WebRip|Web-Rip|WEBMux)|(?<hdtv>HDTV)|(?<bdrip>BDRip|BDLight)|(?<brrip>BRRip)|(?<dvd>DVD|DVDRip|NTSC|PAL|xvidvd)|(?<dsr>WS[-_. ]DSR|DSR)|(?<pdtv>PDTV)|(?<sdtv>SDTV)|(?<tvrip>TVRip))(?:\b|$|[ .])"

regex_tv = re.compile(reg_tv)
regex_movie = re.compile(reg_movie)
regex_tv_folder =re.compile(reg_tv_folder)

with open(f"{index_path}movie_index.txt", "r") as f:
    movie_index_file = json.load(f)
with open(f"{index_path}tv_index.txt", "r") as f:
    tv_index_file = json.load(f)
with open(f"{index_path}duplicates.txt", "r") as f:
    duplicates_file = json.load(f)

files = []
folders = []
count=1
skipped_folders = ["BDMV","CERTIFICATE","FAB!","Featurette","Featurettes"] #add folder names to skip

with open(f"{index_path}raw_unsorted.txt", "r") as f:
    raw_unsorted_file=json.load(f)
with open(f"{index_path}raw_tv_folders.txt", "r") as f:
    raw_tv_folders_file=json.load(f)
with open(f"{index_path}raw_movie.txt", "r") as f:
    raw_movie_file = json.load(f)
with open(f"{index_path}raw_tv.txt", "r") as f:
    raw_tv_file = json.load(f)

unsorted_file = open(f"{index_path}unsorted.txt", "w+")
tv_folders_file = open(f"{index_path}tv_folders.txt", "w+")

def movie_index_update(movie,name):
        movie_name=movie.group("name").replace("."," ")+" "+ movie.group("year")
        group_sort(movie)
        if (movie_name in movie_index_file):
            try:
                if(name in movie_index_file[movie_name][resolution][typ][group]):
                    duplicates_file.update({movie_name:[name]})
                    print("Duplicate found:"+name+"\n")
                    return False
                elif(name not in movie_index_file[movie_name][resolution][typ][group]):
                    movie_index_file[movie_name][resolution][typ][group].append(name)
            except KeyError as e:
                error = e.args[0]
                #print(error + " error")
                if(error==resolution):
                    movie_index_file[movie_name].update({resolution:{typ:{group: [name]}}})
                if(error==group):
                    movie_index_file[movie_name][resolution][typ].update({group: [name]})
                if(error==typ):
                    movie_index_file[movie_name][resolution].update({typ:{group: [name]}})
                #print(str(movie_index_file[movie_name])+"\n")
        else:
            movie_index_file.update({movie_name:{resolution:{typ:{group:[name]}}}})
        return True

def tv_index_update(tv,old_name):
        show_name=tv.group("name").replace("."," ")
        group_sort(tv,old_name)
        if (show_name in tv_index_file):
            try:
                if(name in tv_index_file[show_name][season][resolution][typ][group]):
                    duplicates_file.update({show_name:[name]})
                    print("Duplicate found:"+name+"\n")
                    return False
                elif(name not in tv_index_file[show_name][season][resolution][typ][group]):
                    tv_index_file[show_name][season][resolution][typ][group].append(name)
            except KeyError as e:
                error = e.args[0]
                print(error + " error")
                if(error==resolution):
                    tv_index_file[show_name][season].update({resolution:{typ:{group: [name]}}})
                if(error==group):
                    tv_index_file[show_name][season][resolution][typ].update({group: [name]})
                if(error==typ):
                    tv_index_file[show_name][season][resolution].update({typ:{group: [name]}})
                if(error==season):
                    tv_index_file[show_name].update({season:{resolution:{typ:{group: [name]}}}})
                #print(str(tv_index_file[show_name])+"\n")
        else:
            tv_index_file.update({show_name:{season:{resolution:{typ:{group:[name]}}}}})
        return True

def raw_movie_update(movie,i):
        resolution=movie.group("resolution")
        typ=movie.group("typ").upper()
        if (resolution in raw_movie_file):
            try:
                if(raw_movie_file[resolution][typ]):
                    raw_movie_file[resolution][typ].append(i)
            except KeyError as e:
                error = e.args[0]
                print(error + " error")
                if(error==typ):
                    raw_movie_file[resolution].update({typ:[i]})
        else:
           raw_movie_file.update({resolution:{typ:[i]}})

def raw_tv_update(tv,i,tv_file):
        resolution=tv.group("resolution")
        typ=tv.group("typ").upper()
        if (resolution in tv_file):
            try:
                if(tv_file[resolution][typ]):
                    tv_file[resolution][typ].append(i)
            except KeyError as e:
                error = e.args[0]
                print(error + " error")
                if(error==typ):
                    tv_file[resolution].update({typ:[i]})
        else:
           tv_file.update({resolution:{typ:[i]}})

def group_sort(index,old_name=None):
    global resolution,typ,rartv,name,group,season
    resolution=index.group("resolution")
    if(resolution in ["DVD","DVDRip","DVDRIP","576p","576i","480i","480p","568p","568i"]):
        resolution="DVD"
    typ=index.group("typ")
    if(typ in ["WEB-DL","WEBRip","WebRip","Web-Rip","WEBRIP","WEB","BluRay","Bluray","Blu-ray","BDRip","x265"]):
        typ="Encode"
    elif(typ in ["XVID","XviD"]):
        typ="DVDRip"
    else:
        typ=typ.upper()
    group=index.group("group")
    if("HD.MA" in group or "x264" in group):
        group="NoGroup"
    if(old_name):
        season=index.group("season")
        if(index.group("rartv") is not None):
            name=old_name.replace(index.group("rartv"),"")
        else:
            name=old_name

def regex_sort(i):
        name = i.get('name')
        tv = regex_tv.match(name)
        if (tv):
            raw_tv_update(tv,i,raw_tv_file)
        else:
            movie = regex_movie.match(name)
            if(movie):
                    if(movie_index_update(movie,name)):
                        raw_movie_update(movie,i)
            else:
                    raw_unsorted_file.append(i)         #no index
                    unsorted_file.write(f"{name}\n\n")

def sort(folder_id,page_token=None):
        global count
        q = f"'{folder_id}' in parents"
        res=[]
        while True:
                response = drive_service.files().list(supportsAllDrives=True,includeItemsFromAllDrives=True,q=q,spaces='drive',pageSize=1000, fields='nextPageToken, files(parents,mimeType,id,name)',pageToken=page_token).execute()
                res.extend(response.get('files', []))
                page_token = response.get('nextPageToken', None)
                if page_token is None:
                    break
        for i in res:
                if(i.get('mimeType') == 'application/vnd.google-apps.folder'):
                        folders.append(i)
                        name=i.get("name")
                        tv_folder = regex_tv_folder.match(name)
                        if(tv_folder):
                                if(tv_index_update(tv_folder,name)):
                                    raw_tv_update(tv_folder,i,raw_tv_folders_file)
                                    tv_folders_file.write(f"{name}\n" + tv_folder.group(1).replace('.'," ") + "\n\n")
                                    print(f'folder skipped = {name}\n')
                        else:   
                            if(name not in skipped_folders):
                                if (count%50==0):
                                    service_account_rotate()
                                sort(i.get('id'))
                                count=count+1
                            else:
                                pass  #statements to deal with skipped folders
                else:
                        if(i.get('mimeType')=='video/x-matroska' or "video/mp4"):
                                files.append(i)
                                regex_sort(i)
        #print(files)      

service_account_rotate()

# Call the function on the specified folder
sort(folder_id)
print("response done")

with open(f"{index_path}raw_unsorted.txt", "r+") as f:
    f.seek(0)
    f.write(json.dumps(raw_unsorted_file))

with open(f"{index_path}raw_tv_folders.txt", "r+") as f:
    f.seek(0)
    f.write(json.dumps(raw_tv_folders_file))

with open(f"{index_path}movie_index.txt", "r+") as f:
    f.seek(0)
    f.write(json.dumps(movie_index_file,indent = 4)) 

with open(f"{index_path}tv_index.txt", "r+") as f:
    f.seek(0)
    f.write(json.dumps(tv_index_file,indent = 2)) 

with open(f"{index_path}duplicates.txt", "r+") as f:
    f.seek(0)
    f.write(json.dumps(duplicates_file))

with open(f"{index_path}raw_movie.txt", "r+") as f:
    f.seek(0)
    f.write(json.dumps(raw_movie_file)) 

with open(f"{index_path}raw_tv.txt", "r+") as f:
    f.seek(0)
    f.write(json.dumps(raw_tv_file))

unsorted_file.close()
tv_folders_file.close()
