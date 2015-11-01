# -*- coding: utf-8 -*-
# try something like

def __check_for_admin():
	if auth.user.account_class!='Admin':
		redirect(URL('default','index'))

@auth.requires_login()
def index():
	__check_for_admin()
	row=db(db.complaint_register.complaint_register_isread==False).select(db.complaint_register.ALL)
	return locals()

@auth.requires_login()
def set_account_balance():
	__check_for_admin()
	db.auth_user.id.readable=False
	db.user_details.account_curr_balance.writable=True
	db.user_details.account_initial_balance.writable=True
	query=((db.user_details.id>0) & (db.auth_user.id==db.user_details.user_id))
	fields=(db.auth_user.first_name,
		db.auth_user.last_name,
		db.auth_user.email,
		db.user_details.account_curr_balance)
	headers={
		'auth_user.first_name':"First Name",
		'auth_user.last_name':"Last Name",
		'auth_user.email':"Email",
		'user_details.account_curr_balance':"Current Balance"}

	grid1=SQLFORM.grid(
		query=query,
		fields=fields,
		headers=headers,
		create=False,
		deletable=False,
		editable=True)

	if request.args(0)=='edit':
		session.curr_user=db(db.auth_user.id==int(request.args(2))).select(db.auth_user.ALL)
		session.is_pr_set=session.curr_user[0].profile_set
		session.curr_user_details=db(db.user_details.user_id==int(request.args(2))).select(db.user_details.ALL)
		redirect(URL('default_admin','viewedit'))
	return locals()

@auth.requires_login()
def viewedit():
	__check_for_admin()
	if session.is_pr_set==False:
		redirect(URL('default_admin','set_account_balance'))
	elif session.curr_user!=None and session.curr_user_details!=None:
		form_bal=SQLFORM.factory(Field('account_bal'))
		if form_bal.process().accepted:
			db(db.user_details.user_id==session.curr_user[0].id).update(account_curr_balance=form_bal.vars.account_bal)
			session.curr_user=None
			session.is_pr_set=None
			session.curr_user_details=None
			redirect(URL('default_admin','set_account_balance'))
		elif form_bal.errors:
			response.flash="Enter valid value"
		else:
			response.flash="Update Account Balance"
	else:
		redirect(URL('default_admin','set_account_balance'))
	return locals()

@auth.requires_login()
def set_meal_timings():
	__check_for_admin()
	db.meals_timing.id.readable=False
	db.meals_timing.id.writable=False
	query=((db.meals_timing.id>0))
	fields=(db.meals_timing.mess_place,
		db.meals_timing.mess_time,
		db.meals_timing.eating_time,
		db.meals_timing.advance_booking,
		db.meals_timing.advance_cancellation)
	headers={
		'meals_timing.mess_place':"Mess Place",
		'meals_timing.mess_time':"Mess Time",
		'meals_timing.eating_time':"Eating Time",
		'meals_timing.advance_booking':"Advance Booking",
		'meals_timing.advance_cancellation':"Advance Cancellation",
		}

	grid1=SQLFORM.grid(
		query=query,
		fields=fields,
		headers=headers,
		create=True,
		deletable=True,
		editable=True)
	return locals()

@auth.requires_login()
def set_meal_rates():
	__check_for_admin()
	db.Meal.id.readable=False
	db.Meal.id.writable=False
	query=((db.Meal.id>0))
	fields=(
		db.Meal.meal_name,
		db.Meal.meal_rate)
	headers={
		'Meal.meal_name':'Meal',
		'Meal.meal_rate':'Rate'
	}
	grid1=SQLFORM.grid(
		query=query,
		fields=fields,
		headers=headers,
		create=True,
		deletable=True,
		editable=True)
	return locals()

@auth.requires_login()
def set_mess_places():
	__check_for_admin()
	db.mess_places.id.readable=False
	db.mess_places.id.writable=False
	query=((db.mess_places.id>0))
	fields=(
		db.mess_places.place_name,)
	headers={
		'mess_places.place_name':'Mess Name',
	}
	grid1=SQLFORM.grid(
		query=query,
		fields=fields,
		headers=headers,
		create=True,
		deletable=True,
		user_signature=False,
		editable=True)
	return locals()

@auth.requires_login()
def manage_student():
	__check_for_admin()
	query=((db.auth_user.account_class=='Student'))
	#print '1'
	db.auth_user.id.writable=True
	db.auth_user.id.readable=True
	#print '2'
	fields=(
		db.auth_user.first_name,
		db.auth_user.last_name,
		db.auth_user.roll_no)
	#print '3'
	headers={
		'auth_user.first_name':'First Name',
		'auth_user.last_name':'Last Name',
		'auth_user.roll_no':'Roll No',
	}
	#print '4'
	grid1=SQLFORM.grid(
		query=query,
		fields=fields,
		headers=headers,
		create=False,
		deletable=True,
		editable=True,
		user_signature=False)
	print grid1
	print 'dfsfsdf'
	return locals()

@auth.requires_login()
def manage_faculty():
	__check_for_admin()
	query=((db.auth_user.id>0) & (db.auth_user.account_class=='Faculty'))
	db.auth_user.id.writable=False
	db.auth_user.id.readable=False
	fields=(
		db.auth_user.first_name,
		db.auth_user.last_name,
		db.auth_user.roll_no)
	headers={
		'auth_user.first_name':'First Name',
		'auth_user.last_name':'Last Name',
		'auth_user.email':'Email',
	}
	grid1=SQLFORM.grid(
		query=query,
		fields=fields,
		headers=headers,
		create=True,
		deletable=True,
		editable=True,
		user_signature=False,
		paginate=100)
	return locals()

@auth.requires_login()
def manage_committee():
	__check_for_admin()
	return locals()

@auth.requires_login()
def manage_caterer():
	__check_for_admin()
	query=((db.mess_provider.id>0))
	db.mess_provider.id.writable=False
	db.mess_provider.id.readable=False
	fields=(
		db.mess_provider.caterer_name,
		db.mess_provider.place_of_mess,
		db.mess_provider.email)
	headers={
		'mess_provider.caterer_name':'Caterer Name',
		'mess_provider.place_of_mess':'Mess Name',
		'mess_provider.email':'Email',
	}
	grid1=SQLFORM.grid(
		query=query,
		fields=fields,
		headers=headers,
		deletable=True,
		editable=True,
		user_signature=False,
		paginate=100)

	return locals()

@auth.requires_login()
def set_mess_menu():
	__check_for_admin()

	dayss=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
	meals=db(db.Meal.id>0).select()
	meal_list=[]
	for tt in meals:
		meal_list.append(tt.meal_name)

	if (request.vars.dayw in dayss) and (request.vars.mealname in meal_list):
		query=((db.mess_menu.id>0) & 
			(db.mess_menu.mess_time==request.vars.mealname) & 
			(db.mess_menu.week_day==request.vars.dayw ))
		db.mess_menu.id.writable=False
		db.mess_menu.id.readable=False
		grid1=SQLFORM.grid(query=query,create=True,editable=True,deletable=True)

	else:
		redirect(URL('default_admin','index'))
	return locals()

@auth.requires_login()
def manage_complaints():
	__check_for_admin()

	unread_complaints=db(db.complaint_register.complaint_register_isread==False).select()
	read_complaints=db(db.complaint_register.complaint_register_isread==True).select()

	form_check=SQLFORM.factory(Field('mark_all_as_read','boolean'))

	if form_check.process().accepted:
		db(db.complaint_register.complaint_register_isread==False).update(complaint_register_isread=True)
		redirect('default_admin','manage_complaints')

	return locals()

@auth.requires_login()
def manage_approval():	
	__check_for_admin()
	query=((db.auth_user.registration_key=='pending'))
	#print '1'
	db.auth_user.id.writable=False
	db.auth_user.id.readable=False
	db.auth_user.first_name.writable=False
	db.auth_user.last_name.writable=False
	db.auth_user.roll_no.writable=False
	db.auth_user.account_class.readable=False
	db.auth_user.account_class.writable=False
	db.auth_user.registration_key.writable=True
	db.auth_user.password.writable=False
	db.auth_user.profile_set.readable=False
	db.auth_user.profile_set.writable=False
	db.auth_user.email.writable=False
	#print '2'
	fields=(
		db.auth_user.first_name,
		db.auth_user.last_name,
		db.auth_user.roll_no)
	#print '3'
	headers={
		'auth_user.first_name':'First Name',
		'auth_user.last_name':'Last Name',
	}
	#print '4'
	grid1=SQLFORM.grid(
		query=query,
		fields=fields,
		headers=headers,
		create=False,
		deletable=False,
		editable=True,
		user_signature=False)
	return locals()




