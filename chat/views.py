import uuid
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from chat.models import Profile
from chat.utility import group_list, user_list, get_message, create_group
from chat.forms import UserRegisterForm, EditProfileForm, LoginForm
from django.contrib.auth import login, authenticate
from django.contrib import messages


def editprofile(request):
    instance = Profile.objects.get(user=request.user.id)
    form = EditProfileForm(instance=instance)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('name')
            dob = form.cleaned_data.get('dob')
            messages.add_message(request, messages.SUCCESS, "Your Profile has been updated.")
    return render(request, "chat/edit_profile.html", {"form": form})


def register(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(request, username=username, password=raw_password)
            if user is not None:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, "Your have successfully registered.")
                return redirect("chat-page")
        messages.add_message(request, messages.WARNING, "Something went wrong.")
    return render(request, "chat/Register.html", {'form':form})

    
def login_user(request):
    form = LoginForm()
    if request.user.is_authenticated:
        return redirect("chat-page")
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('chat-page')
        messages.add_message(request, messages.WARNING, "Please enter correct credentials.")
        return redirect('login-user')
    return render(request, "chat/LoginPage.html", {"form": form})



def chatPage(request, *args, **kwargs):
    # ChatRooms.objects.filter(name='Best Friends').delete()
    if not request.user.is_authenticated:
        return redirect("login-user")
    
    group_lst = group_list(request.user.id)
  
    all_users = User.objects.all()
    lst = user_list(request)
    
    if request.method == 'POST':
        group_name = request.POST.get('groupname')
        group_user = request.POST.getlist('group_user')
        chatroom = str(uuid.uuid4())
        create = create_group(request, group_name, group_user, chatroom)
        if create['status'] == False:
            messages.add_message(request, messages.WARNING, "Group already exist.")
            return redirect("chat-page")
        else:
            messages.add_message(request, messages.SUCCESS, f"Group, {group_name} has been created.")
            return redirect("chat-page")
    context = {"all_users": all_users, "user_list": lst, "groups": group_lst}
    return render(request, "chat/chatPage.html", context)


def get_messages(request):
    if not request.user.is_authenticated:
        return redirect("login-user")
    
    room = request.GET.get('room')
    lst = room.split("_")

    tmp_list = get_message(room, lst)
   
    return JsonResponse({"status": "success", "data": tmp_list})