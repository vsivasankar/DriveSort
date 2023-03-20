import regex as re
import os
import json

reg_movie="(?P<name>.+)[\.\s][\(]?(?P<year>[\d]{4})[\)]?(?P<repack>REPACK)?.*[\.\s\(](?P<res>2160p|1080[pi]|720[ip]|DVDRIP|DVDRip|DVD|576[ip]|480[pi]|568[pi]).*[\.\s](?P<typ>WEB-DL|WEBRip|WebRip|Web-Rip|WEB|REMUX|Remux|ReMUX|BluRay|BluRay|Blu-ray|Bluray|BDRip|XVID|XviD|x265).*[-\s][\s]?([^\s\[\.\)]+)[\)]?(?:\.mkv|\.mp4)"
reg_tv_folder2 = "(?P<name>.+)[\.\s](?P<season>[Ss][\d][\d][\d]?|(?<pack>[Ss][\d][\d][\d\s]?-[Ss][\d][\d][\d]?))[\.\s](?P<repack>REPACK)?.*[\(]?(?P<res>2160p|1080[pi]|720[ip]|DVDRIP|DVDRip|DVD|576[ip]|480[pi]|568[pi]).*[\.\s](?P<typ>WEB-DL|WEBRip|WebRip|Web-Rip|REMUX|Remux|ReMUX|BluRay|BluRay|Blu-ray|Bluray|BDRip|XVID|XviD).*[-]([^\s\[\)\(]+)[\)]?(?P<rartv>\[rartv\]|[\s]?[\(\[].+[\)\]])?"

regex_tv_folder2=re.compile(reg_tv_folder2)
regex_movie = re.compile(reg_movie)

def move(parent,destination,source=None):
    with open("/media/343c/ninja69/bin/rclone.conf", "rt+") as file:
        regex = r"(root_folder_id = )(.+[^\n])"
        content = file.read()
        pattern = re.compile(regex)
        match = pattern.findall(content)
        content = re.sub(match[0][1], parent, content, 1)
        file.seek(0)
        file.write(content)
    file_list = [
    '/media/343c/ninja69/bin/gclone move temp1:"',source,'" temp2:"',destination,'" -P --drive-server-side-across-configs']
    file_clone = "".join(filter(None, file_list))
    print(file_clone)
    if(source==None):print("Starting rclone folder")
    else:print("Starting rclone file")
    os.system(file_clone)

with open("/media/343c/ninja69/sort/documents/raw_movie_remux_1080p.txt", "r") as f:
        if (f!=None or f!="[]" or f!=""):
            to_move=json.load(f)
            for i in to_move:
                file_name=i.get("name")
                movie_folder_name=regex_movie.match(file_name)
                new_folder_name= movie_folder_name.group(1).replace('.'," ") + " (" + movie_folder_name.group(2) + ")"
                parent = i.get('parents')[0]
                dest_folder_name="Movies/1080p/REMUX/" + new_folder_name
                move(parentdest_folder_name,file_name)

with open("/media/343c/ninja69/sort/documents/raw_movie_remux_2160p.txt", "r") as f:
        if (f!=None or f!="[]" or f!=""):
            to_move=json.load(f)
            for i in to_move:
                file_name=i.get("name")
                movie_folder_name=regex_movie.match(file_name)
                new_folder_name= movie_folder_name.group(1).replace('.'," ") + " (" + movie_folder_name.group(2) + ")"
                parent = i.get('parents')[0]
                dest_folder_name="Movies/2160p/REMUX/" + new_folder_name
                move(parent,dest_folder_name,file_name)


"""with open("/media/343c/ninja69/sort/documents/raw_tv_remux_1080p.txt", "r") as f:
        f.write(json.dumps(tv_remux_1080p))


with open("/media/343c/ninja69/sort/documents/raw_tv_remux_2160p.txt", "r") as f:
        f.write(json.dumps(tv_remux_2160p))


with open("/media/343c/ninja69/sort/documents/raw_unsorted.txt", "r") as f:
        f.write(json.dumps(unsorted))"""


"""with open("/media/343c/ninja69/sort/documents/raw_folders.txt", "r") as f:
        if (f!=None or f!="[]" or f!=""):
            to_move=json.load(f)
            for i in to_move:
                tv_name = i.get('name')
                tv_folder_name=regex_tv_folder2.match(tv_name)
                new_folder_name= tv_folder_name.group(1).replace('.'," ")
                self_folder = i.get('id')
                if (tv_folder_name.group(3)==('1080p' or '1080i')):
                    dest_folder_name="TV/1080p/REMUX/"+new_folder_name+"/"+tv_name
                elif(tv_folder_name.group(3)=='2160p'):
                    dest_folder_name="TV/2160p/REMUX/"+new_folder_name+"/"+tv_name
                move(self_folder,dest_folder_name) """
