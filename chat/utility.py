import pytz
from django.utils import timezone
from django.contrib.auth.models import User
from chat.models import ChatMessages, ChatRooms
from django.db.models import Q


kolkata_timezone = pytz.timezone('Asia/Kolkata')

def group_list(user_id):
    groups = ChatRooms.objects.filter(user=user_id)
    group_lst = []
    if groups.exists():
        for group in groups:
            g_dict = {}
            chatroom = group.chatroom
            query = ChatMessages.objects.filter(group_name=chatroom).last()
            if query:
                g_dict['message'] = query.message
                g_dict['date'] = timezone.localtime(query.message_at, timezone=kolkata_timezone).strftime('%H:%M')
            g_dict['group'] = group.name
            g_dict['chatroom'] = chatroom
            group_lst.append(g_dict)
    return group_lst

def user_list(request):
    all_users = User.objects.all()
    lst = []
    for x in all_users:
        tmd_dict = {}
        tem_list = sorted([x.username, request.user.username], key=lambda x: x.lower())
        GroupName = tem_list[0]+"_"+tem_list[1]
        message = ChatMessages.objects.filter(Q(user=x, to=request.user.username) | Q(to=x, user=request.user.id), group_name=GroupName).last()
        if message:
            tmd_dict['message'] = message.message
            tmd_dict['date'] = timezone.localtime(message.message_at, timezone=kolkata_timezone).strftime('%H:%M')
        tmd_dict['user'] = x.username
        lst.append(tmd_dict)
    return lst

def get_message(room, lst):
    to = lst[1]
    if lst[0] != 'g':
        tem_list = sorted(room.split("_"), key=lambda x: x.lower())
        GroupName = tem_list[0]+"_"+tem_list[1]
    else:
        GroupName = to
        to = 'group'
    query = ChatMessages.objects.filter(group_name=GroupName)
    tmp_list = []
    if query.exists():
        for x in query:
            tmp_dict = {}
            tmp_dict['user'] = x.user.username
            tmp_dict['to'] = x.to
            tmp_dict['message'] = x.message
            tmp_dict['date'] = x.message_at
            tmp_list.append(tmp_dict)
    return tmp_list


def create_group(request, group_name, group_user, chatroom):
    exist = ChatRooms.objects.filter(user__username=request.user.username, name=group_name).exists()
    if exist:
        error = "Group already exist."
        return {"status": False, "error": error}
    entry = ChatRooms.objects.create(chatroom=chatroom, name=group_name)
    for xy in group_user:
        users = User.objects.get(username=xy)
        entry.user.add(users)
    return {"status": True}

