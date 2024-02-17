
import json
class Entry:
    def __init__(self,title,desc,start,end,duration,parent=None) -> None:
        self.name = title
        self.desc = desc
        self.start = start
        self.end = end
        self.duration = duration
        self.parent = parent
        self.widget = None

    def to_dict(self):
        return {
            "title": self.name,
            "desc": self.desc,
            "start": self.start,
            "end": self.end,
            "duration": self.duration
        }
    

class Genre:
    def __init__(self, name):
        self.name = name
        self.items = []
        self.parent = None
        self.widget = None

    def add_item(self, entry):
        self.items.append(entry)
        if isinstance(entry,Genre):
            entry.parentGenre = self

    def get_items(self,title_widgets):
        for item in self.items:
            if item.name != title_widgets[0].currentText():continue
            if title_widgets[1:]:
                return self.items
            self.get_items(title_widgets[1:])            

    def remove_genre(self,entry):
        self.items.remove(entry)

        if self.items:return
        if not self.parentGenre:
            self.widget.deleteLater()
            return self
         
        a = self.parentGenre.remove_genre(self)
        self.parentGenre = None
        return a

    def to_dict(self):
        return {
            "genre_name" : f"{self.name}",
            "items": [e.to_dict() for e in self.items]
        }


def check_genre_exists(title,items_list):
    result = None
    for item in items_list:
        if isinstance(item, Entry): continue
        if item.name == title:
            return item 
        elif len(item.items)== 1: #im assuming that len(item.items) == 1 means that it only has one item which is AN Entry instance
            return None
        result = check_genre_exists(title, item.items)
    return result


def find_genre_sequence(titles, items_list):
    for item in items_list:
        if isinstance(item, Entry):
            continue
        if titles[0] != item.name:
            continue
        subItem = find_genre_sequence(titles[1:], item.items)
        if subItem == None:
            return item
        return subItem 
    return None 

def get_last_entry(obj):
    if isinstance(obj,Entry):
        return obj
    return get_last_entry(obj.items[-1])

def find_entry(title, obj):
    if isinstance(obj,Entry):
        if obj.title == title:
            return obj
        else:
            return None
    for item in obj.items:
        find_entry(title,item)

def deserialize_data(item_dic, parent=None):
    if "desc" in item_dic.keys():
        e = Entry(item_dic["title"], item_dic["desc"], item_dic["start"], item_dic["end"], item_dic["duration"])
        e.parent = parent 
        return e
    genre = Genre(item_dic["genre_name"])
    genre.parent = parent
    for genre_dic in item_dic["items"]:
        subitem = deserialize_data(genre_dic, genre)
        genre.add_item(subitem)

    return genre 

def read_data(file):
    items = []
    with open(file) as fp:
        items_list = json.load(fp)

    for item_dic in items_list:
        item = deserialize_data(item_dic)
        items.append(item)
    return items

def save_data(events,file):
    json_data_list = [e.to_dict() for e in events]
    with open(file, 'w') as fp:
        json.dump(json_data_list,fp,indent=2)
        
def construct_item(widgets:list,forum_answers:list, parent=None):
    if not widgets:
        return  
    widget = widgets[0]
    if len(widgets) == 1:
        entry = Entry(widget.currentText(),forum_answers[0],
                      forum_answers[1].toString("yyyy-MM-dd hh:mm:ss AP"),
                      forum_answers[2].toString("yyyy-MM-dd hh:mm:ss AP"),
                      forum_answers[1].secsTo(forum_answers[2]), parent)
        if parent:
            parent.add_item(entry)
        return entry
    parent_genre = Genre(widget.currentText())
    parent_genre.parent= parent 
    if parent:
        parent.add_item(parent_genre)
    construct_item(widgets[1:], forum_answers, parent_genre)
    return parent_genre

        


   

   
        


    