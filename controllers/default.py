# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################
state_name=['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana ', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal']

import datetime

def oncompare_time(food_meal,food_date):
    food_time=db(food_meal==db.Meal.meal_name).select(db.Meal.ALL)
    diff_datetime=datetime.datetime(
        food_date.year,
        food_date.month,
        food_date.day)
    return True

days=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
menu_data={}
menu_timings=db().select(db.Meal.meal_name)
def classify_menu():
    for row1 in db().select(db.mess_provider.place_of_mess, distinct=True):
        p=row1.place_of_mess
        Cater_Name={}
        for row2 in db(p==db.mess_provider.place_of_mess).select(db.mess_provider.caterer_name,distinct=True):
            c=row2.caterer_name
            d=[[],[],[],[],[],[],[]]
            for ss in range(7):
                for add in range(len(menu_timings)):
                    d[ss].append([])
            for row3 in db(p==db.mess_menu.place_of_mess and c==db.mess_menu.caterer_name).select():
                for i in range(7):
                    if row3.week_day==days[i]:
                        for k in range(len(menu_timings)):
                            if row3.mess_time==menu_timings[k].meal_name:
                                d[i][k].append(row3.eating_item)
                                break
                        break
            Cater_Name[c]=d
        menu_data[p]=Cater_Name

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    #response.flash = T("Hello World")
    if auth.is_logged_in():
        redirect(URL('default','after_login_index'))
    return dict(message=auth.user)

@auth.requires_login()
def after_login_index():
    if db(auth.user.id==db.user_details.user_id).count()==0:
        redirect(URL('default','complete_profile'))
    return locals()

@auth.requires_login()
def complete_profile():
    form=''
    if db(auth.user.id==db.user_details.user_id).count()==0:
        db.user_details.user_id.writable=False
        db.user_details.user_id.readable=False
        db.user_details.account_initial_balance.writable=False
        db.user_details.account_initial_balance.readable=False
        db.user_details.account_curr_balance.writable=False
        db.user_details.account_curr_balance.readable=False
        form=SQLFORM(db.user_details)
        form.vars.account_initial_balance=0
        form.vars.account_curr_balance=0;
        form.vars.user_id=auth.user.id
        if form.process().accepted:
            session.flash="Profile completed"
            redirect(URL('default','after_login_index'))
        elif form.errors:
            response.flash='Please complete your profile'
    else:
        temp=db(auth.user.id==db.user_details.user_id).select(db.user_details.ALL)
        form=SQLFORM.factory(
            Field('phone_number',requires=IS_MATCH('\d{10}'),default=temp[0].phone_number),
            Field('preferred_mess',requires=IS_IN_DB(db,'mess_provider.place_of_mess'),default=temp[0].preferred_mess),
            Field('preferred_caterer',requires=IS_IN_DB(db,'mess_provider.caterer_name'),default=temp[0].preferred_caterer),
            Field('your_booking_preference',requires=IS_IN_SET(['''Don't Book Food Automatically''','Book Food Automatically']),default=temp[0].your_booking_preference))
        
        if form.process().accepted:
            row=db(auth.user.id==db.user_details.user_id).select(db.user_details.user_id)
            curr_id=row[0].user_id
            db(curr_id==db.user_details.user_id).update(
                phone_number=form.vars.phone_number,
                preferred_mess=form.vars.preferred_mess,
                preferred_caterer=form.vars.prefrred_caterer,
                your_booking_preference=form.vars.your_booking_preference)
            session.flash='Profile successfully edited'
            redirect(URL('default','after_login_index'))
            
        elif form.errors:
            response.flash="Please fill in valid details"
    return locals()

def mess_menu():
    classify_menu()
    return dict(menu_data=menu_data,days=days,menu_timing=menu_timings)

@auth.requires_login()
def reserve_meal():
    form1=SQLFORM.factory(
                Field('reserve_eating_place',label='Mess Place',requires=IS_IN_DB(db,'mess_provider.place_of_mess')),
                Field('reserve_caterer',label='Caterer',requires=IS_IN_DB(db,'mess_provider.caterer_name')),
                Field('reserve_start_date','date',label='Start Date'),
                Field('reserve_end_date','date',label='End Date'),
                Field('reserve_start_meal',label='Start Meal',requires=IS_IN_DB(db,'Meal.meal_name')),
                Field('reserve_end_meal',label='End Meal',requires=IS_IN_DB(db,'Meal.meal_name')))
    
    if form1.process().accepted:
        deduction=0
        #date_list=map(int,form1.vars.reserve_start_date.split('-'))
        start=form1.vars.reserve_start_date
        #date_list=map(int,form1.vars.reserve_end_date.split('-'))
        end=form1.vars.reserve_end_date
        meal_s=form1.vars.reserve_start_meal
        meal_e=form1.vars.reserve_end_meal
        delta=end-start
        meal_list=db().select(db.Meal.meal_name)
        #redirect(URL('default','index/'+str(len(meal_list))))
        rate_list=db().select(db.Meal.meal_rate)
        if (delta.days-1)<0:
            start_pos=0
            end_pos=0
            for i in range(len(meal_list)):
                if meal_list[i].meal_name==meal_s:
                    start_pos=i
                    break
            for i in range(len(meal_list)):
                if meal_list[i].meal_name==meal_e:
                    end_pos=i
                    break
            j=start_pos

            while j<=end_pos:
                row=db(auth.user.id==db.reserve_food.author_id).select(db.reserve_food.ALL)
                found=False
                for x in row:
                    if (x.reserve_meal==meal_list[j].meal_name and x.reserve_date==form1.vars.reserve_start_date):
                        found=True
                        break
                if not found:
                    db.reserve_food.insert(
                        reserve_eating_place=form1.vars.reserve_eating_place,
                        reserve_caterer=form1.vars.reserve_caterer,
                        reserve_date=form1.vars.reserve_start_date,
                        reserve_meal=meal_list[j].meal_name,
                        author_id=auth.user.id)
                    deduction=deduction+int(rate_list[j].meal_rate)
                j=j+1
        
        else:
            start_pos=0
            end_pos=0
            for i in range(len(meal_list)):
                if meal_list[i].meal_name==meal_s:
                    start_pos=i
                    break
            for i in range(len(meal_list)):
                if meal_list[i].meal_name==meal_e:
                    end_pos=i
                    break
            j=start_pos
            while j<range(len(meal_list)):
                row=db(auth.user.id==db.reserve_food.author_id).select(db.reserve_food.ALL)
                found=False
                if j>=len(meal_list):
                    break
                for x in row:
                    if (x.reserve_meal==meal_list[j].meal_name and x.reserve_date==form1.vars.reserve_start_date):
                        found=True
                        break
                if not found:
                    db.reserve_food.insert(
                        reserve_eating_place=form1.vars.reserve_eating_place,
                        reserve_caterer=form1.vars.reserve_caterer,
                        reserve_date=form1.vars.reserve_start_date,
                        reserve_meal=meal_list[j].meal_name,
                        author_id=auth.user.id)
                    deduction=deduction+int(rate_list[j].meal_rate)
                j=j+1
            j=0
            while j<=end_pos:
                row=db(auth.user.id==db.reserve_food.author_id).select(db.reserve_food.ALL)
                found=False
                for x in row:
                    if (x.reserve_meal==meal_list[j].meal_name and x.reserve_date==form1.vars.reserve_start_date):
                        found=True
                        break
                if not found:
                    db.reserve_food.insert(
                        reserve_eating_place=form1.vars.reserve_eating_place,
                        reserve_caterer=form1.vars.reserve_caterer,
                        reserve_date=form1.vars.reserve_end_date,
                        reserve_meal=meal_list[j].meal_name,
                        author_id=auth.user.id)
                    deduction=deduction+int(rate_list[j].meal_rate)
                j=j+1

            i=0
            number_of_entry=delta.days-1
            start=start+datetime.timedelta(days=1)
            while i<number_of_entry:
                #temp=start.year+'-'+start.month+'-'+start.day
                for j in range(len(meal_list)):
                    row=db(auth.user.id==db.reserve_food.author_id).select(db.reserve_food.ALL)
                    found=False
                    for x in row:
                        if (x.reserve_meal==meal_list[j].meal_name and x.reserve_date==start):
                            found=True
                            break
                    if not found:
                        db.reserve_food.insert(
                            reserve_eating_place=form1.vars.reserve_eating_place,
                            reserve_caterer=form1.vars.reserve_caterer,
                            reserve_date=start,
                            reserve_meal=meal_list[j].meal_name,
                            author_id=auth.user.id)
                        deduction=deduction+int(rate_list[j].meal_rate)
                start=start+datetime.timedelta(days=1)
                i=i+1
        acc_balance=db(auth.user.id==db.user_details.user_id).select(db.user_details.account_curr_balance);
        auth_user_curr_balance=acc_balance[0]
        if (int(auth_user_curr_balance)-deduction)<0:
            if auth.account_type=='Student':
                response.flash='''Account Balance can't be negative. Please contact Mess Administrator'''
            else:
                auth_user_curr_balance=str(int(auth_user_curr_balance)-deduction)
                caterer_booked=db(db.mess_provider.caterer_name==form1.vars.reserve_caterer).select(db.mess_provider.ALL)
                db(db.mess_provider.id==caterer_booked[0].id).update(
                    account_curr_balance=str(int(caterer_booked[0].account_curr_balance)+deduction))
                db(db.user_details.user_id==auth.user.id).update(
                    account_curr_balance=auth_user_curr_balance)
                response.flash='''Your food is successfully reserved'''
        else:
            auth_user_curr_balance=str(int(auth_user_curr_balance)-deduction)
            caterer_booked=db(db.mess_provider.caterer_name==form1.vars.reserve_caterer).select(db.mess_provider.id,db.mess_provider.account_curr_balance)
            db(db.mess_provider.id==caterer_booked[0].id).update(
                account_curr_balance=str(int(caterer_booked[0].account_curr_balance)+deduction))
            db(db.user_details.user_id==auth.user.id).update(
                account_curr_balance=auth_user_curr_balance)
            response.flash='''Your food is successfully reserved'''
    return locals()

@auth.requires_login()
def manage_cancellation(table,row_id):
    #redirect(URL('default','manage_cancellation'))
    acc_balance=db(auth.user.id==db.user_details.user_id).select(db.user_details.account_curr_balance);
    auth_user_curr_balance=acc_balance[0]
    temp=db(row_id==db.reserve_food.id).select(db.reserve_food.ALL)
    mymealname=temp[0].reserve_meal
    cat_name=temp[0].reserve_caterer
    y=db(db.Meal.meal_name==mymealname).select(db.Meal.ALL)
    auth_user_curr_balance=int(auth_user_curr_balance)+int(y[0].meal_rate)
    c=db(db.mess_provider.caterer_name==cat_name).select(db.mess_provider.ALL)
    caterer_b=int(c[0].account_curr_balance)-int(y[0].meal_rate)
    db(temp[0].author_id==db.auth_user.id).update(account_curr_balance=auth_user_curr_balance)
    db(c[0].id==db.mess_provider.id).update(account_curr_balance=caterer_b)
    db(row_id==db.reserve_food.id).delete()

@auth.requires_login()
def cancel_meal():
    query=((db.reserve_food.author_id==auth.user.id))
    fields=(db.reserve_food.reserve_meal,
            db.reserve_food.reserve_date,
            db.reserve_food.reserve_eating_place,
            db.reserve_food.reserve_caterer)
    headers={
    'reserve_food.reserve_meal':'Booked Meals',
    'reserve_food.reserve_date':'Booking Date',
    'reserve_food.reserve_eating_place':'Booked Mess',
    'reserve_food.reserve_caterer':'Booked Caterer'
    }
    default_sort_order=[~db.reserve_food.reserve_date,]
    grid1=SQLFORM.grid(query=query, fields=fields, headers=headers, orderby=default_sort_order,
                create=False, deletable=True, editable=False,ondelete=manage_cancellation)
    return locals()

def mess_people():
    return locals()

def mess_incharge():
    query=((db.auth_user.account_class=='Admin') & (db.user_details.user_id==db.auth_user.id))
    row=db(query).select()
    return locals()

def mess_commitee():
    query=((db.auth_user.account_class=='Mess Committee') & (db.user_details.user_id==db.auth_user.id))
    row=db(query).select()
    return locals()

def mess_caterer():
    row=db().select(db.mess_provider.caterer_name,db.mess_provider.phone_number,db.mess_provider.place_of_mess)
    return locals()

def general_notifications():
    return locals()

@auth.requires_login()
def complaint_section():
    db.complaint_register.complaint_register_isread.default=False
    db.complaint_register.complaint_register_isread.readable=False
    db.complaint_register.complaint_register_isread.writable=False
    form1=SQLFORM(db.complaint_register)
    if form1.process().accepted:
        session.flash="Complaint registered"
        redirect(URL("default","index"))
    elif form1.errors:
        response.flash="Fill out the complaint form properly"
    return locals()

@auth.requires_login()
def admin_change_remove():
    if auth.user.account_class=='Admin':
        if request.vars.modify=='People':
            db.auth_user.id.readable=False
            db.auth_user.account_curr_balance.writable=True
            db.auth_user.account_initial_balance.writable=True
            query=((db.auth_user.account_class!='Admin' or db.auth_user.id!=auth.user.id))
            fields=(db.auth_user.first_name,db.auth_user.last_name,db.auth_user.email,db.auth_user.account_curr_balance)
            headers={
            'auth_user.first_name':"First Name",
            'auth_user.last_name':"Last Name",
            'auth_user.email':"Email",
            'auth_user.account_curr_balance':"Current Account Balance"
            }
            default_sort_order=[db.auth_user.first_name]

            grid1=SQLFORM.grid(query=query, fields=fields, headers=headers, orderby=default_sort_order,
                    create=True, deletable=True, editable=True)
        elif request.vars.modify=='Caterer':
            db.mess_provider.id.readable=False
            db.mess_provider.account_curr_balance.writable=True
            db.mess_provider.account_curr_balance.readable=True
            fields=(
                db.mess_provider.caterer_name,
                db.mess_provider.email,
                db.mess_provider.account_curr_balance,
                db.mess_provider.phone_number)
            query=db.mess_provider.id>0
            headers={
            'mess_provider.caterer_name':"Caterer Name",
            'mess_provider.email':"Email",
            'mess_provider.account_curr_balance':"Current Account Balance",
            'mess_provider.phone_number':"Phone number",
            }
            default_sort_order=[db.mess_provider.caterer_name]
            grid1=SQLFORM.grid(
                    query=query,
                    fields=fields,
                    headers=headers,
                    orderby=default_sort_order,
                    create=True,
                    deletable=True,
                    editable=True)
        elif request.vars.modify=='Mess_Place':
            form1=SQLFORM.grid(db.mess_places,editable=True,orderby=[db.mess_places.place_name])
        elif request.vars.modify=='Mess_Menu':
            form1=SQLFORM.grid(db.mess_menu,editable=True,orderby=[db.mess_menu.eating_item])
        elif request.vars.modify=='meals_timing':
            form1=SQLFORM.grid(db.meals_timing,editable=True,orderby=[db.meals_timing.mess_place])
        elif request.vars.modify=='meal_rate':
            form1=SQLFORM.grid(db.Meal,editable=True,orderby=[db.Meal.meal_name])
        elif request.vars.modify=='manage_people':
            form1=SQLFORM.grid(db.auth_user,editable=True,orderby=[db.auth_user.first_name])
        else:
            h='Invalid Page'
            redirect(URL('default','index'))
    else:
        h='Permission Denied'
    return locals()

def manageregistration(form):
    #db.user_details.insert(user_id=rowid);
    return
    
def registration_page():
    if auth.is_logged_in():
        session.flash="Already logged in. No registration required"
        redirect(URL('default','index'))
        return locals()
    else :
        registration_form=auth.register()
        return dict(signup_form=registration_form)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    if request.args(0)=='profile':
        db.user_details.account_curr_balance.writable=False
        db.user_details.account_initial_balance.writable=False
        db.user_details.account_curr_balance.readable=True
        db.user_details.account_initial_balance.readable=True
        row1=db(auth.user.id==db.user_details.user_id).select(db.user_details.ALL)
        return locals()
    elif request.args(0)=='register':
        redirect(URL('default','registration_page'));
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
