# 在增、改、删的view中
# 调用log_addition, log_change, log_deletion 这三个函数，记录到LogEntry（给管理员偷窥的）
# 调用inform_sb，增添Information（给动作承受的用户看的）
# 从admin/options.py复制来的，最log_deletion中object_repr的取值进行了化简

from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from .models import Information

def get_content_type_for_model(obj):
    # Since this module gets imported in the application's root package,
    # it cannot import models from other applications at the module level.

    return ContentType.objects.get_for_model(obj, for_concrete_model=False)

def inform_sb(to_whom, from_whom, info):
    if to_whom!=from_whom:
        info["who"]=from_whom.id
        Information.objects.create(user=to_whom, info=info)

def log_addition(request, obj, message):
    """
    Log that an object has been successfully added.

    The default implementation creates an admin LogEntry object.
    """
    
    return LogEntry.objects.log_action(
        user_id=request.user.pk,
        content_type_id=get_content_type_for_model(obj).pk,
        object_id=obj.pk,
        object_repr=str(obj),
        action_flag=ADDITION,
        change_message=message,
    )

def log_change(request, obj, message):
    """
    Log that an object has been successfully changed.

    The default implementation creates an admin LogEntry object.
    """

    return LogEntry.objects.log_action(
        user_id=request.user.pk,
        content_type_id=get_content_type_for_model(obj).pk,
        object_id=obj.pk,
        object_repr=str(obj),
        action_flag=CHANGE,
        change_message=message,
    )

def log_deletion(request, obj, message):
    """
    Log that an object will be deleted. Note that this method must be
    called before the deletion.

    The default implementation creates an admin LogEntry object.
    """

    return LogEntry.objects.log_action(
        user_id=request.user.pk,
        content_type_id=get_content_type_for_model(obj).pk,
        object_id=obj.pk,
        object_repr=str(obj),
        action_flag=DELETION,
    )