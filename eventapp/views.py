from django.shortcuts import render,redirect,get_object_or_404
from django.utils import timezone
from django.http import HttpResponse,Http404
import datetime
from .models import Event,Task,Attendee
from userAcc.models import CustomUser
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Sum
from datetime import datetime
import math
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import auth
from django.contrib import auth, messages
import re
from django.core.files.storage import default_storage
# import imghdr
from django.core.files.base import ContentFile
from django.contrib.auth import authenticate,login
from django.template import RequestContext
from .keys import cipher_suite
from django.contrib.auth.models import User,Group,Permission
from .keys import cipher_suite
# Create your views here.

def custom_404_view(request, exception):
    return render(request, "404.html", status=404)

def is_in_staff_group(user):
    return user.groups.filter(name="staff").exists()


def desboard_page(request):
    
    amount=0
    summ={}
    percentage ={}
    numberOfTask = {}
    number_Total = 0
    current_date = datetime.now().date()
    # if request.user.is_authenticated:
    if request.user.is_superuser:
        event = Event.objects.filter(date__gte=current_date).order_by('date')
        task =Task.objects.all()
        user_info = CustomUser.objects.all()
        

        for i in event:
            # print('iii' ,i)
            for j in task:
                if i.id == j.Event_id:
                    amount+=j.Budget
                    number_Total+=1
            summ[i.id] = amount
            numberOfTask[i.id] = number_Total
            percentage[i.id]=math.ceil((amount/i.Budget)*100)
            # if percentage[i:id] >100:
            #     percentage[i.id] =100
            amount=0
            number_Total = 0
        for i in percentage:

            if percentage[i] > 100:
                percentage[i]=100
        context ={
                'events': event,
                'summs':summ,
                'user_info':user_info,
                'percentages':percentage,
                'numbersotask':numberOfTask,
                
            }
        return render(request,'index.html',context)
    elif is_in_staff_group(request.user):
        event = Event.objects.filter(date__gte=current_date,manager_email = request.user.email ).order_by('date')
        task =Task.objects.all()
        user_info = CustomUser.objects.all()
        print(event)
        for i in event:
            # print('iii' ,i)
            for j in task:
                if i.id == j.Event_id:
                    amount+=j.Budget
                    number_Total+=1
            summ[i.id] = amount
            numberOfTask[i.id] = number_Total
            percentage[i.id]=math.ceil((amount/i.Budget)*100)
            # if percentage[i:id] >100:
            #     percentage[i.id] =100
            amount=0
            number_Total = 0
        for i in percentage:

            if percentage[i] > 100:
                percentage[i]=100
        context ={
                'events': event,
                'summs':summ,
                'user_info':user_info,
                'percentages':percentage,
                'numbersotask':numberOfTask
            }
        return render(request,'index.html',context)
    elif not is_in_staff_group(request.user) and request.user.is_staff:
        return render(request,'access_denied.html')
    else:
        present_date = datetime.now().date()
        events = Event.objects.all()
        lstOfDate = []
        current_datetime = datetime.now()
        time = current_datetime.time()
        lstofrow =[]
        rows_passed1 = Event.objects.filter(date__lt=current_datetime.date())
        rows_passed2 = Event.objects.filter(date=current_datetime.date())
        for i in rows_passed1:
            # if i.time < time :
                lstOfDate.append(i.id)
        for j in rows_passed2:
            if j.time <time :
                lstOfDate.append(j.id)
        # for i in events:
        #     if i.date< present_date:
        #         lstOfDate.append(i.id)

        if request.user.is_authenticated:
            
            registered_event_ids = Attendee.objects.filter(user_id=request.user.id).values_list('event_id', flat=True)
            # attendee = {}
            # for i in events:
            #     for j in attendeeModel:
            #         if i.id == j.event_id and j.user_id == request.user.id:
            #             attendee[i.id]= 'yess'
            
            return render(request, 'index.html', {'userevents': events,'attendees':registered_event_ids,'presentDate':lstOfDate})
        
        
        return render(request, 'index.html', {'userevents': events,'presentDate':lstOfDate})
    # return render(request,'index.html')
            


@login_required(login_url='login_page')
def Event_page(request):
    # grr = Group.objects.get(name='Even')
    user_perm = CustomUser.objects.get(id= request.user.id)
    print('user_perm 1344',user_perm.groups.all())
    if request.user.is_superuser or (request.user.has_perm('eventapp.can_add_event') and is_in_staff_group(request.user)):
        amount=0
        summ={}
        event = Event.objects.all()
        # if request.method == 'GET':
        #     event_title = request.GET.get('eventTitle')
        #     print(event_title)
        #     try:
        #         event =Event.objects.filter(venue=event_title)
        #         print(event)
        #     except:
        #         event = Event.objects.all()
        #         print("else")
        task =Task.objects.all()
        current_datetime = datetime.now()
        time = current_datetime.time()
        lstofrow =[]
        rows_passed1 = Event.objects.filter(date__lt=current_datetime.date())
        rows_passed2 = Event.objects.filter(date=current_datetime.date())
        print(rows_passed1)
        print(rows_passed2)
        for i in rows_passed1:
            
        #     if i.time < time :
                lstofrow.append(i.id)
        for j in rows_passed2:
            if j.time <time :
                lstofrow.append(j.id)
        print("lst of rows :",lstofrow)

        
        for i in event:
            
            for j in task:
                if i.id == j.Event_id:
                    amount+=j.Budget
                
            summ[i.id] = amount
            amount=0
        # events = Event.objects.all()
        newinfo = CustomUser.objects.all()
        
        context = {
            'events': event,
            'info': newinfo,
            'summs': summ,
            'past_event':lstofrow
        }
        return render(request, 'Event_page.html', context)
    else:
        return render(request,'access_denied.html')
    return render(request, 'Event_page.html')

@csrf_exempt
def deshborad_data(request):
    if request.method=='POST':
        if request.user.is_authenticated:
            if request.user.is_superuser:
                event = list(Event.objects.values())
                return JsonResponse({'data_chart': event},safe=False)
            elif request.user.is_staff:
                event = list(Event.objects.values().filter(manager_email=request.user.email))
                return JsonResponse({'data_chart': event},safe=False)
        
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'})
    return redirect('home')

@login_required(login_url='login_page')
def User_Event_page(request):
    event = Event.objects.all()
    registered_event_ids = Attendee.objects.filter(user_id=request.user.id).values_list('event_id', flat=True)
    return render(request,'Event_user.html',{'attendees':registered_event_ids,'events':event})

@csrf_exempt
def delete_user_event(request):
    if request.method =='POST':
        try:
            eventid = request.POST.get('event_Id')
            userid = request.POST.get('user_Id')
            print('155500',eventid,userid)
            attendeeCount = Event.objects.get(id=eventid).Attendee
            Attendee.objects.create(event_id = eventid,user_id = userid)
            Event.objects.filter(id=eventid).update(Attendee =attendeeCount-1)
            Attendee.objects.filter(user_id = userid,event_id=eventid).delete()
            messages.success(request,f'Event deleted Successfully')
            return JsonResponse({'status': 'success'},safe=False)
        except:
            messages.error(request,'Opps! cant delete that event plz try again')
    return JsonResponse({'erroe': 'Sumthing Error'})

@login_required(login_url='login_page')
def Task_page(request):

    if not is_in_staff_group(request.user) and request.user.is_staff and not request.user.is_superuser:
        return render(request,'access_denied.html')
    amount=0
    summ={}
    events = Event.objects.all()
    task =Task.objects.all()
    for i in events:
        for j in task:
            if i.id == j.Event_id:
                amount+=j.Budget
            
        summ[i.id] = amount
        amount=0
    context = {
        'events': events,
        'summs':summ
    }
    return render(request,'Task_page.html', context)

@csrf_exempt
def task_table(request):
    if request.method =='POST':
        
        task = list(Task.objects.values())
        eventid = request.POST.get('event_id')
        print(eventid)

        current_datetime = datetime.now()
        time = current_datetime.time()
        lstofrow =[]
        rows_passed1 = Event.objects.filter(date__lt=current_datetime.date())
        rows_passed2 = Event.objects.filter(date=current_datetime.date())
        for i in rows_passed1:
            
            # if i.time < time :
                lstofrow.append(i.id)
        for j in rows_passed2:
            if j.time <time :
                lstofrow.append(j.id)

        total_sum_amount = Task.objects.filter(Event_id = eventid).aggregate(total_sum=Sum('Budget'))
        return JsonResponse({'total_sum': total_sum_amount['total_sum'],'task':task,'TodayDate':lstofrow},safe=False)
        # return JsonResponse(task, safe=False)
    
@csrf_exempt
def top_task(request):
    if request.method =='POST':
        # task = list(Task.objects.values().order_by('-Budget'))
        eventid = request.POST.get('event_id')
        
        task = list(Task.objects.values().filter(Event_id = eventid).order_by('-Budget'))
        print("total task ",task)
        total_sum_amount = Task.objects.filter(Event_id = eventid).aggregate(total_sum=Sum('Budget'))
        return JsonResponse({'total_sum': total_sum_amount['total_sum'],'task':task},safe=False)

def total_amount(request):
    if request.method =='POST':
        eventid = request.POST.get('event_id')
        print(eventid)
        total_sum_amount = Task.objects.filter(Event_id = eventid).aggregate(total_sum=Sum('Budget'))
        return JsonResponse({'total_sum': total_sum_amount['total_sum']})

# def User_Event_page(request):
#     events = Event.objects.all()
#     return render(request, 'Event_user.html', {'events': events})
def hasedValue():
    cipherHas = cipher_suite
    return cipherHas

@login_required(login_url='login_page')
def Acount_new_page(request):
    if request.user.is_superuser or (request.user.has_perm('userAcc.can_add_staff') and is_in_staff_group(request.user)):
        
        staff_users = CustomUser.objects.filter(
            is_staff=True,
            is_superuser=False,
        ).exclude(email=request.user.email)
        
        user_data = []
        groups = Group.objects.exclude(name="staff")  
        
        for user in staff_users:
            user_groups = user.groups.all()
            group_names = [g.name for g in user_groups]
            filtered_groups = user_groups.exclude(name="staff")
            
            # ✅ Make sure hashed_id is generated
            hashed_id = cipher_suite.encrypt(str(user.id).encode()).decode()
            print('User:', user.id, 'Hashed ID:', hashed_id)
            user_data.append({
                'user': user,
                'groups': filtered_groups,
                'group_names': group_names,
                'hashed_id': hashed_id
            })
        
        context = {
            'info_user': user_data,
            'groups': groups
        }
        
        return render(request, 'Account_new.html', context)
    
    else:
        return render(request, 'access_denied.html')
def Account_edit(request, encoded_userId):
    if request.user.is_superuser or (request.user.has_perm('userAcc.can_add_staff') and is_in_staff_group(request.user)):
        try:
            userId = cipher_suite.decrypt(encoded_userId.encode()).decode()
            userInfo = CustomUser.objects.get(id=userId)

            user_groups = userInfo.groups.all()
            group_ids = [group.id for group in user_groups]
            all_groups = Group.objects.exclude(name="staff")
            is_in_staff_group = userInfo.groups.filter(name="staff").exists()

            context = {
                'userInfo': userInfo,
                'groups': group_ids,
                'all_group': all_groups,
                'is_in_staff_group': is_in_staff_group
            }
            return render(request, 'Account_edit.html', context)

        except Exception as e:
            print("Decryption Error:", e)
            messages.error(request, "Invalid or expired link.")
            return redirect('account_page')

    elif not is_in_staff_group(request.user) and request.user.is_staff:
        return render(request, 'access_denied.html')

    return redirect('account_page')


def Edit_account_admin(request, encoded_userId):
    if request.method == 'POST' and (request.user.is_superuser or (request.user.has_perm('userAcc.can_edit_staff') and is_in_staff_group(request.user))):
        try:
            userId = cipher_suite.decrypt(encoded_userId.encode()).decode()
            userInfo = CustomUser.objects.get(id=userId)

            active_c = request.POST.get('active_edit')
            staff_c = request.POST.get('staff_edit')
            email = request.POST.get('email_edit')
            phone_number = request.POST.get('phone_number_edit')
            groups_ids = request.POST.getlist('groups_name')

            # Email check excluding current user
            if CustomUser.objects.filter(email=email).exclude(id=userId).exists():
                messages.error(request, f"The email {email} already exists")
                return redirect('account_edit', encoded_userId=encoded_userId)


            # Phone number validation
            phone_pattern = r'^[6-9]\d{9}$'
            if not re.match(phone_pattern, phone_number):
                messages.error(request, "Enter a valid 10-digit Indian phone number")
                return redirect('account_edit', encoded_userId=encoded_userId)


            active = (active_c == 'on')
            staff = (staff_c == 'on')

            userInfo.groups.clear()

            staff_group, _ = Group.objects.get_or_create(name='staff')
            if staff:
                staff_group.user_set.add(userInfo)
            else:
                staff_group.user_set.remove(userInfo)

            for group_id in groups_ids:
                group = Group.objects.get(id=group_id)
                group.user_set.add(userInfo)

            userInfo.is_active = active
            userInfo.email = email
            userInfo.phone_number = phone_number
            userInfo.save()

            messages.success(request, 'Account updated successfully')
            return redirect('account_edit', encoded_userId=encoded_userId)


        except Exception as e:
            print("Error:", e)
            messages.error(request, "Oops! Couldn't update the account.")
            return redirect('account_edit', encoded_userId=encoded_userId)


    return render(request, 'access_denied.html')

def profile_edit_page(request):
    return render(request,'Profile_Edit.html')

from PIL import Image
def profile_edit(request):
    if request.method == "POST" and request.user.is_authenticated:
        try:
            first_name = request.POST.get('first_name_profile')
            last_name = request.POST.get('last_name_profile')
            user_name = request.POST.get('user_name_profile')
            email_user = request.POST.get('email_profile')
            phone_number = request.POST.get('phone_profile')
            profile_pic = request.FILES.get('profile_pic')
            remove_pic = request.POST.get('check_pic')

            if CustomUser.objects.filter(email=email_user).exclude(id=request.user.id).exists():
                messages.error(request, f"The email {email_user} already exists")
                return redirect("profile_edit_page") 
            if CustomUser.objects.filter(username=user_name).exclude(id=request.user.id).exists():
                messages.error(request, f"The username {user_name} already exists")
                return redirect("profile_edit_page") 
            if not first_name:
                messages.error(request, f"First Name required")
                return redirect("profile_edit_page")
            
            pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if not re.match(pattern, email_user):
                messages.error(request, f"Invalid Email")
                return redirect("profile_edit_page")

            if not email_user:
                messages.error(request, f"Email required")
                return redirect("profile_edit_page")  # Redirect to the registration page

            phone_pattern = r'^[6-9]\d{9}$'
            if not re.match(phone_pattern, phone_number):
                messages.error(request, "Enter a valid phone number")
                return redirect("profile_edit_page")  # or "account_page" in Account_view
            user = CustomUser.objects.get(id=request.user.id)

            if profile_pic:
                try:
                    image = Image.open(profile_pic)
                    image.verify()
                    profile_pic.seek(0)

                    user.profile_image = profile_pic

                except (IOError, SyntaxError):
                    messages.error(request, "File should be an image.")
                    return redirect("home")

            if remove_pic == 'on':
                user.profile_image = ''

            user.first_name = first_name
            user.last_name = last_name
            user.username = user_name
            user.email = email_user
            user.phone_number = phone_number
            user.save()

            messages.success(request, "Profile has been edited successfully.")
            return redirect('profile_edit_page')

        except:
            messages.error(request, 'Oops! Something went wrong.')
            return redirect('profile_edit_page')
        
def password_page(request):
    global current_password
    if request.method == 'POST' and request.user.is_authenticated:
        current_password = request.POST.get('Current_password')
        check_password = authenticate(request, username=request.user.email, password=current_password)
        if check_password is not None:
            return render(request,'password_update.html')
        else:
            messages.error(request,'Password was not currect')
            return redirect('profile_edit_page')
    return render(request,'Profile_Edit.html')

def password_reset(request):
    if request.method == 'POST' and request.user.is_authenticated:
        user = request.user

        password1 = request.POST.get('password_c1')
        password2 = request.POST.get('password_c2')

        
        if password1 != password2:
            messages.error(request,'The password doesn\'t match')
            return render(request,'password_update.html')
        if password1 == '' :
            messages.error(request,'Enter password')
            return render(request,'password_update.html')
        
        if current_password == password1:
            messages.error(request,'Please Enter a New Password')
            return render(request,'password_update.html')
        print(password1,password2)
        user.set_password(password1)
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request,'Password Changed Successfully')
        # You may want to log the user out after changing the password
        # logout(request)
        # Redirect the user to a success page or login page
        # messages.success(request,'Password Changes Successfully')
        return redirect('profile_edit_page')
    return render(request,'password_update.html')
        
@login_required(login_url='login_page')
def create_event(request):
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            description = request.POST.get('discription')
            venue = request.POST.get('venue')
            date = request.POST.get('date')
            time = request.POST.get('time')
            budget = request.POST.get('budget')
            managed_by = request.POST.get('assgin_to')
            managed_by_email = request.POST.get('assign_to_email_name')
            print('32 = ',managed_by_email,title,description,venue,time,budget,managed_by)    

            print("321321321",type(budget))
            if int(budget) < 1 :
                print('300')
                messages.error('Invalid Budget')
                return redirect('Event-page')
            print('30333')
            try:
                print('327 Try ')
                int(budget)
            except:
                print("3300 except")
                messages.error('Invalid Budget')
                return redirect('Event-page')
            
            # if not managed_by or not managed_by_email :
            #     messages.error('Did you forgate to assign event?')
            #     return redirect('Event-page')
            print("333 77")
            Event.objects.create(title=title, description=description, venue=venue, date=date, time=time, Budget=budget, managed_by=managed_by,manager_email=managed_by_email,created_by=request.user.email)
            messages.success(request,f'Event added Successfully')
            return redirect('Event-page')
        except:
            messages.error(request,'Oops! cant add that event Plz Try again ')
            return redirect('Event-page')
    elif not is_in_staff_group(request.user) and request.user.is_staff:
        return render(request,'access_denied.html')
    return render(request, 'Event_page.html')


def get_event_data(request):
        if request.method == 'POST':
            try:
                print("get_event_data")
                event_id = request.POST.get('id_of_event_name')
                print("event_id ",event_id)
                event = Event.objects.get(id=event_id)
                print("event ",event)
                event.title = request.POST.get('edit_title')
                event.description = request.POST.get('edit_discription')
                event.venue = request.POST.get('edit_venue')
                event.date = request.POST.get('edit_date')
                event.time = request.POST.get('edit_time')
                event.Budget = request.POST.get('edit_budget')
                event.status = request.POST.get('Status_edit')
                event.manager_email = request.POST.get('edit_assign_to_email_name')
                event.managed_by = request.POST.get('edit_assgin_to')
                # event.Attendee = request.POST.get('edit_attendee')
                print("797979797 :: ",request.POST.get('edit_assign_to_email_name'),request.POST.get('edit_assgin_to'))
                event.save()
                # print(data)
                messages.success(request,f'Event Update Successfully')
                return redirect('Event-page')
            except:
                messages.error(request,'Oops! cant update that event Plz Try again ')
                return redirect('Event-page')
        return render(request, 'Event_page.html')

def search_product(request):
    if request.method == 'POST':
        search_data = request.POST.get('search_event')
        print('2222222222222222',search_data)
        if(len(search_data)==0):
            raise Http404('please provide valid data')
        else:
            # for description too first import from django.db.models import Q
            # result = ProductModel.objects.filter(Q(product_name__icontains = search_data) | Q(product_description__icontains = search_data))
            result = Event.objects.filter(Q(title__icontains = search_data) | Q(venue__icontains = search_data) | Q(date__icontains = search_data))
            attends = Attendee.objects.filter(user_id=request.user.id).values_list('event_id', flat=True)
            current_datetime = datetime.now()
            time = current_datetime.time()
            lstofrow =[]
            rows_passed1 = Event.objects.filter(date__lt=current_datetime.date())
            rows_passed2 = Event.objects.filter(date=current_datetime.date())
            for i in rows_passed1:
                
                # if i.time < time :
                    lstofrow.append(i.id)
            for j in rows_passed2:
                if j.time <time :
                    lstofrow.append(j.id)
            context = {
                'userevents':result,
                'attendees': attends,
                'presentDate':lstofrow
            }

            return render(request,'index.html',context)
    return render(request,'index.html')

@csrf_exempt
def delete_event(request):

    if request.method == 'POST':
        try:
            event_id = request.POST.get('event_id')
            print("93  === ",event_id)
            
            Event.objects.filter(id=event_id).delete()
            messages.success(request,f'Event Deleted Successfully')
            return JsonResponse({'status': 'success'})
        except:
            messages.error(request,'Oops! cant delete that event Plz Try again ')
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'})


@login_required(login_url='login_page')
@csrf_exempt
def attend_event(request):  
    if request.method =='POST':
        try:
            eventid=request.POST.get('eventuser')
            userid = request.POST.get('userId')
            usertitle = request.POST.get('eventtitle')
            print(eventid)
            attendeeCount = Event.objects.get(id=eventid).Attendee
            print(attendeeCount)
            Attendee.objects.create(event_id = eventid,user_id = userid)
            Event.objects.filter(id=eventid).update(Attendee =attendeeCount+1)
            messages.success(request,f'Registerd for Event: "{usertitle}" Successfully')
            return JsonResponse({'status': 'success'})
        
        except:
            messages.error(request,'Oops! cant Add that event Plz Try again ')
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'})
    
@csrf_exempt
def new_task(request):
    if request.method =='POST':
        title = request.POST.get('title')
        budget = request.POST.get('budget')
        managed_by = request.POST.get('managed_by')
        event_id = request.POST.get('event_id')
        statusE = request.POST.get('status_E')
        # Create the Task object
        task = Task.objects.create(title=title, Budget=budget, maneged_by=managed_by, Event_id=event_id)
        print('109 ===' ,statusE)
        if statusE == 'Pending':
            
            Event.objects.filter(id=event_id).update(status='Ongoing')
        # Optionally, you can return the created task data as JSON
        return JsonResponse({'status': 'success', 'task_id': task.id})
        
    
    return render(request, 'Task_page.html')


def login_page(request):
    if not request.user.is_authenticated:
        return render(request,'login.html')
    else:
        auth.logout(request)
        return render(request,'login.html')

def register_page(request):
    return render(request,'register.html')


def userInfoToAssign(request):
    # username = request.user.get_username()
    newinfo = CustomUser.objects.all()
    # Now you can access user attributes like user.email, user.first_name, etc.
    # ...
    context = {
        'info':newinfo
    }
    # print(info)
    return render(request,'Event_page.html',context)


@csrf_exempt
def edit_task_data(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        title = request.POST.get('title')
        budget = request.POST.get('budget')
        # Retrieve the task object
        try:
            task = Task.objects.get(pk=task_id)
            # Update task attributes
            task.title = title
            task.Budget = budget
            # Save changes
            task.save()
            return JsonResponse({'status': 'success'})
        except Task.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Task not found'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'})

@csrf_exempt
def delete_task(request):

    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        event_id =request.POST.get('event_id')
        print("93  === ",event_id)
        
        Task.objects.filter(id=task_id).delete()
        if Task.objects.filter(Event_id=event_id).count() < 1:
            Event.objects.filter(id=event_id).update(status ='Pending')
            print('less then 1 in task')
        return JsonResponse({'status': 'success'})
        
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'})

@csrf_exempt
def update_event(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        status_t = request.POST.get('status')
        print(' eveveveveveveveve ::::: ',status_t)
        try:
            event = Event.objects.get(id=event_id)
            event.status = status_t
            event.save()
            return JsonResponse({'status': 'success'})
        except Event.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Event not found'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'})





def new_group(request):
    
    # Block entirely if not authenticated
    if not request.user.is_authenticated:
        return render(request, 'access_denied.html')

    # Allow superuser no matter what
    if request.user.is_superuser:
        pass  # Allow access

    # Block if user is marked as staff but not actually in staff group
    elif request.user.is_staff and not is_in_staff_group(request.user):
        return render(request, 'access_denied.html')

    # Block if user does not have permission to make group
    elif not request.user.has_perm('userAcc.can_make_group'):
        return render(request, 'access_denied.html')

    # Otherwise, allowed
    groups = Group.objects.exclude(name="staff")  # Exclude 'staff' group
    membars = CustomUser.objects.all()
    
    context = {
        'groups': groups,
        'info': membars
    }
    return render(request, 'new_group.html', context)

def make_group(request):
    if request.method=='POST':
        group_name = request.POST.get('group_name')
        members_lst = request.POST.getlist('members_lst')
        try:
            if group_name == '':
                messages.error(request,'Please Enter Group Name')
                return redirect('new_group')
            else:
                groupName = Group.objects.create(name=group_name)
                for member_id in members_lst:
                    user = get_object_or_404(CustomUser, pk=member_id)
                    groupName.user_set.add(user)
            
            if request.POST.get('event_group') == 'on':
                perme1 =  Permission.objects.get(codename='can_add_event')
                perme2 =  Permission.objects.get(codename='can_edit_event')
                groupName.permissions.add(perme1, perme2)

            if request.POST.get('staff_group') == 'on':
                perms1 =  Permission.objects.get(codename='can_add_staff')
                perms2 =  Permission.objects.get(codename='can_edit_staff')
                groupName.permissions.add(perms1, perms2)


            if request.POST.get('group_group') == 'on':
                perm1 =  Permission.objects.get(codename='can_make_group')
                groupName.permissions.add(perm1)

            messages.success(request,'Group has created')
            return redirect('new_group')
        except:
            messages.error(request,'Something Went wrong')
            return redirect('new_group')

@csrf_exempt
def group_info(request):
    group_id=request.POST.get('groupid')
    # print('group nmz ',group_id)
    group = Group.objects.get(id=group_id)
    # print('group 758 ',group)
    group_permissions = list(group.permissions.values())
    group_members = []
    for user in group.user_set.all():
        member_data = {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'profile_pic': user.profile_image.url if user.profile_image else None  # Assuming profile_image is the ImageField
        }
        group_members.append(member_data)
    print('group 758 ',group_members)
    return JsonResponse({'status': 'success','permissions':group_permissions,'group_member':group_members})

@csrf_exempt
def delete_group(request):

    try:
        global groupInfo
        groupid= request.POST.get('groupid')
        print('id group',groupid)
        # groupInfo = cipher_suite.decrypt(groupid.encode()).decode()
        group = Group.objects.get(id=groupid)
        group.delete()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': e})


def edit_group(request):
    if request.method == 'POST':
        try:
            groupName = request.POST.get('group_edit')
            groupid = request.POST.get('group_id_name')
            print('groupINFOO',groupid,groupName)
            selected_checkboxes = request.POST.getlist('checkName')
     
            membars = request.POST.getlist('checkNamem')
            Addmembars = request.POST.getlist('edit_members_lst')
            AddPermission = request.POST.getlist('edit_permission_lst')

            print("New Val",membars)
            group = get_object_or_404(Group, pk=groupid)

            for member_id in membars:
                user = get_object_or_404(CustomUser, pk=member_id)
                group.user_set.remove(user)
            for i in selected_checkboxes:
                if i == 'group':
                    permission = Permission.objects.get(codename='can_make_group')
                    group.permissions.remove(permission)
                if i=='event':
                    permission1 = Permission.objects.get(codename='can_edit_event')
                    permission2 = Permission.objects.get(codename='can_add_event')
                    group.permissions.remove(permission1,permission2)
                if i=='staff':
                    permission1 = Permission.objects.get(codename='can_add_staff')
                    permission2 = Permission.objects.get(codename='can_edit_staff')
                    group.permissions.remove(permission1,permission2)
            for i in Addmembars:
                user = get_object_or_404(CustomUser, pk=i)
                group.user_set.add(user)
            for i in AddPermission:
                if i == 'e':
                    perme1 =  Permission.objects.get(codename='can_add_event')
                    perme2 =  Permission.objects.get(codename='can_edit_event')
                    group.permissions.add(perme1, perme2)
                if i == 's':
                    perme1 =  Permission.objects.get(codename='can_add_staff')
                    perme2 =  Permission.objects.get(codename='can_edit_staff')
                    group.permissions.add(perme1, perme2)
                if i == 'g':
                    perme1 =  Permission.objects.get(codename='can_make_group')
                    
                    group.permissions.add(perme1)

            members = group.user_set.all()
            for i in members:
                print(i.id,i.first_name,i.last_name,i.email,i.profile_image)
            group.name = groupName
            group.save()
            messages.success(request,'Group has Updated')
            return redirect('new_group')
        except:
            messages.error(request,'Something Went wrong')
            return redirect('new_group')

def get_data(request):
    selected_checkboxes = request.POST.getlist('checkName')
    print("New Val",selected_checkboxes)
    return redirect('new_group')