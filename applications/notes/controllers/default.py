# -*- coding: utf-8 -*-
import lxml.html

def index():
    return redirect(URL('notes'))

dict_test ={}
form1 = db(db.notes.username==auth.user_id).select(db.notes.datetime)
for i in form1:
    dict_test.setdefault(i['datetime'].year, [])
    if i['datetime'].month not in dict_test[i['datetime'].year]:
        dict_test[i['datetime'].year].append(i['datetime'].month)

@auth.requires_login()
def show():

    return dict(dict_test=dict_test,makers=[],html_list=[])

def maker():
    if request.vars.year =='Select Year':
        makers = []
    else:
        makers = dict_test[int(request.vars.year)]
    result = ""
    result += "<option value='" + str("Select Month") + "'>" +str("Select Month") + "</option>"
    for maker in makers:
        result += "<option value='" + str(maker) + "'>" +str(maker) + "</option>"

    return XML(result)

def two():
    result = ""
    result += "<option value='" + str("Select Day") + "'>" +str("Select Day") + "</option>"
    if request.vars.month =='Select Month':
        form1 = []
    else:
        form1 = db((db.notes.username==auth.user_id) &
                   (db.notes.datetime.year()==request.vars.year) &
                   (db.notes.datetime.month()==request.vars.month)).select(db.notes.datetime.day())
        for i in form1:
            result += "<option value='" + str(i["_extra"]["web2py_extract('day',notes.datetime)"]) + "'>" +str(i["_extra"]["web2py_extract('day',notes.datetime)"]) + "</option>"

    return XML(result)


@auth.requires_login()
def notes():

    db.notes.username.writable = False
    db.notes.username.readable = False
    db.notes.Notes.readable = False

    grid = SQLFORM.grid(db.notes.username==auth.user_id,db.notes,user_signature=False,
                        details=False,paginate=15,orderby=~db.notes.datetime)
    return locals()

@auth.requires_login()
def add_share_users():
    db.share_users.username.readable = False
    db.share_users.id.readable = False
    grid = SQLFORM.grid(db.share_users.username==auth.user_id,db.share_users,user_signature=False,details=True,paginate=15)
    return locals()

@auth.requires_login()
def share_notes():
    if request.vars.year and request.vars.month and request.vars.day and request.vars.user:
        if request.vars.year=="Select Year" or request.vars.month=="Select Month" or request.vars.day=="Select Day":
            link= ""
            return XML(link)
        str_day = (request.vars.day).encode('base64')
        str_month = (request.vars.month).encode('base64')
        str_year = (request.vars.year).encode('base64')
        KEY = request.vars.user
        print KEY

        link = A("Share this link",_href=URL('share', vars=dict(a=str_day,b=str_month,c=str_year), hmac_key=KEY),target="_blank")

        return XML(link)
    else:
        return dict(dict_test=dict_test,makers=[],html_list=[],form1=[],link="")

def share():
    response.menu=[]
    KEY = request.client
    print KEY
    if not URL.verify(request, hmac_key=KEY): raise HTTP(403)

    month = (request.vars.b).decode('base64')
    year = (request.vars.c).decode('base64')
    day = (request.vars.a).decode('base64')
    form1 = db((db.notes.datetime.day()==day) &
                   (db.notes.datetime.year()==year) &
                   (db.notes.datetime.month()==month)).select(db.notes.ALL,orderby=~db.notes.datetime)

    html_list = []
    for i in form1:
        html_list.append({str(i['datetime']):lxml.html.fromstring(i['Notes']).text_content()})
    return dict(html_list=html_list)

def one():

    if request.vars.month =='Select Month' and request.vars.year =='Select Month':
        html_list = []
    else:
        form = db(db.notes.datetime.month()==int(request.vars.month)).select(db.notes.ALL,orderby=~db.notes.datetime)
        html_list = []
        result = ""
        import datetime
        for i in form:
            result+="<pre><b>"+datetime.datetime.strptime(str(i['datetime']), '%Y-%m-%d').strftime('%d-%B-%Y').upper()+"</b>"+lxml.html.fromstring(i['Notes']).text_content()+"</pre><br>"

        return XML(result)

@auth.requires_login()
def todo():
    return dict()


def user():
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
