# -*- coding: utf-8 -*-
import os
import time
from os import stat
from pwd import getpwuid
from stat import *
from hurry.filesize import size


@auth.requires_login()
def add_project():

    response.title ="Add Project"
    import Tkinter, tkFileDialog
    root = Tkinter.Tk()
    root.withdraw()
    test = ""
    dirname = ""
    ok=""
    if request.vars.type=="easy":
        dirname = tkFileDialog.askdirectory(parent=root,initialdir="/",title='Please select a directory')
    if request.vars.name and request.vars.path:
        name = request.vars.name
        path = request.vars.path
        check_name = db(db.projects.name==name).select(db.projects.id)
        check_path = db(db.projects.location_path==path).select(db.projects.id)
        if check_name:
            return dict(dirname=dirname,ok="name")
        if check_path:
            return dict(dirname=dirname,ok="path")

        id = db.projects.insert(name=name,location_path=path)
        if id:
            return dict(dirname=dirname,ok="ok")
    return dict(dirname=dirname,ok=ok)

def get_filepaths():

    file_paths = {}
    list_ignore = [".svn",".idea","venv",".git"]
    result = ""
    if request.vars.pname=="Select Project":
        return XML(result)
    for root, directories, files in os.walk(request.vars.pname):
        for filename in files:
            str = filename[0]!='.' and 'venv' not in root and '.git' not in root and '.idea' not in root
            if str:
                filepath = os.path.join(root, filename)
                file_paths[filepath] = {}
                file_paths[filepath]['Author'] = getpwuid(stat(filepath).st_uid).pw_name
                file_paths[filepath]['Permission'] = oct(os.stat(filepath)[ST_MODE])[-3:]
                file_paths[filepath]['Last Modified'] = time.ctime(os.stat(filepath)[ST_MTIME])
                file_paths[filepath]['Size'] = size(os.path.getsize(filepath))

    result+="<pre>"
    for i,j in file_paths.iteritems():
        test = i.rsplit('/', 1)
        result += "<b><font size=3px>"+test[1]+"</font></b><br>"
        result += "&thinsp;&thinsp;&thinsp;<b>Path</b> : "+test[0]+"<br>"
        for m,n in j.iteritems():
            result +="&thinsp;&thinsp;&thinsp;<b>"+m+"</b> : "+n+"<br>"
        result+="<br>"
    result+="</pre>"
    return XML(result)


@auth.requires_login()
def delete_project():

    response.title ="Delete Project"
    db.projects.id.readable = False
    db.projects.username.readable = False

    grid = SQLFORM.grid(db.projects.username==auth.user_id,db.projects,user_signature=False,
                        paginate=15,editable=False,create=False)
    return locals()


@auth.requires_login()
def view_project():

    response.title ="View Project"
    return dict(file_paths={})
