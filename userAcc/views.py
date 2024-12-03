from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import auth, messages
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth.hashers import make_password
# from social_django.models import UserSocialAuth  # Import the UserSocialAuth model
# import requests
from userAcc.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
# import imghdr
import re

def signin_view(request):
    if request.method == "POST":
        email = request.POST.get("email_login")
        password = request.POST.get("password_login")
        print("13 === == ",email)
        user = authenticate(request, username=email, password=password)
        print("new  === ",user)
        if user is not None:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request,f'Wellcome {request.user.first_name}')
            return redirect("home")
        else:
            print("None")
            messages.error(request,'Account not found or Incorrect Credentials')
            return redirect('login_page')
            
    return render(request, "index.html")

from PIL import Image
def signup_view(request):

    if request.method == "POST":
        # Extract user registration data from the request.POST dictionary

        email = request.POST.get("email_r_name")
        username = request.POST.get("Username_r_name")
        first_name = request.POST.get("first_r_name")
        last_name = request.POST.get("last_r_name")
        phone_number = request.POST.get("phone_r_name")
        password = request.POST.get("password_r_name1")
        password2 = request.POST.get("password_r_name2")
        profile_pic = request.FILES.get("profile_pic")  # Get uploaded profile picture
        print('6767 == ',profile_pic)

        # Check if the email already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, f"The email {email} already exists")
            return redirect("register_page") 
        
        
        if not first_name:
            messages.error(request, f"First Name required")
            return redirect("register_page")
        
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, email):
            messages.error(request, f"Invalid Email")
            return redirect("register_page")
        if not email:
            messages.error(request, f"Email required")
            return redirect("register_page")  # Redirect to the registration page
        if password!=password2:
            messages.error(request, f"The password Dosent match")
            return redirect("register_page")  # Redirect to the registration page

        # Save profile picture if provided
        profile_image_path = None
        if profile_pic:
            try:
                # Open the image using Pillow
                image = Image.open(profile_pic)
                image.verify()  # Verify that the file is a valid image file
                
                # If the image is valid, reset the file pointer and save the image
                profile_pic.seek(0)  # Reset the file pointer to the beginning
                
                # Define the path to save the profile picture (e.g., 'profile_pics/filename')
                profile_image_path = default_storage.save('profile_pics/' + profile_pic.name, ContentFile(profile_pic.read()))

                # You can proceed with saving other information related to the user as needed
                messages.success(request, "Profile image uploaded successfully.")
                return redirect("home")

            except (IOError, SyntaxError):
                # If the file is not a valid image
                messages.error(request, "File should be an image.")
                return redirect("register_page")

        # Create a new CustomUser instance and save it to the database
        user = CustomUser.objects.create(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            profile_image=profile_image_path,  # Save the profile picture path
            password=make_password(password)  # Hash the password
        )

        # Log the user in
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request,'Account Created Successfully')
        return redirect("home")

    return render(request, "register.html")



@login_required(login_url='login_page')
def logout_view(request):
    auth.logout(request)
    return redirect("home")


def Account_view(request):

    if request.method == "POST":
        # Extract user registration data from the request.POST dictionary

        email = request.POST.get("email_A_name")
        username = request.POST.get("Username_A_name")
        first_name = request.POST.get("first_A_name")
        last_name = request.POST.get("last_A_name")
        phone_number = request.POST.get("phone_A_name")
        password = request.POST.get("password_A_name")
        # password2 = request.POST.get("password_r_name2")
        profile_pic = request.FILES.get("profile_pic_Account")  # Get uploaded profile picture
        group_lst = request.POST.getlist('groups_name_add')
        print('6767 == ',profile_pic)

        # Check if the email already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, f"The email {email} already exists")
            return redirect("account_page") 
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, f"The username {username} already exists")
            return redirect("account_page") 
        
        if not first_name:
            messages.error(request, f"First Name required")
            return redirect("account_page")
        
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, email):
            messages.error(request, f"Invalid Email")
            return redirect("account_page")

        if not email:
            messages.error(request, f"Email required")
            return redirect("account_page")  # Redirect to the registration page

        # Save profile picture if provided
        if not password:
            messages.error(request, f"Password required")
            return redirect("account_page")
        if profile_pic:
            try:
                # Open the image using Pillow
                image = Image.open(profile_pic)
                image.verify()  # Verify that the file is a valid image

                # If the image is valid, reset the file pointer and save the image
                profile_pic.seek(0)  # Reset the file pointer to the beginning of the file
                
                # Define the path to save the profile picture (e.g., 'profile_pics/filename')
                path = default_storage.save('profile_pics/' + profile_pic.name, ContentFile(profile_pic.read()))

                messages.success(request, "Profile picture uploaded successfully.")
                return redirect("home")

            except (IOError, SyntaxError):
                # If the file is not a valid image
                messages.error(request, "The file should be an image.")
                return redirect("account_page")
                        
        # Create a new CustomUser instance and save it to the database
        user = CustomUser.objects.create(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            profile_image=path if profile_pic else None,  # Save the profile picture path
            is_active=True,
            is_staff=True,
            password=make_password(password)  # Hash the password
        )
        user_id = get_object_or_404(CustomUser, email = email)
        
        for i in group_lst:
            groupName = Group.objects.get(id = i)
            groupName.user_set.add(user_id)

        # Log the user in
        # user = authenticate(request, username=email, password=password)
        # if user is not None:
        #     login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request,'Account Created Successfully')
        return redirect("account_page")

    return render(request, "Account_new.html")


