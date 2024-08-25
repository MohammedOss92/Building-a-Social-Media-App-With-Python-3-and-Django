from django import template
from social.models import Notification

# إنشاء كائن للتسجيل في مكتبة القوالب
register = template.Library()

@register.inclusion_tag('social/show_notifications.html', takes_context=True)
def show_notifications(context):
    # الحصول على المستخدم الحالي من سياق القالب
    request_user = context['request'].user
    
    # جلب الإشعارات التي تخص المستخدم الحالي والتي لم يتم رؤيتها بعد، وترتيبها حسب التاريخ من الأحدث إلى الأقدم
    notifications = Notification.objects.filter(to_user=request_user).exclude(user_has_seen=True).order_by('-date')
    
    # إعادة الإشعارات ليتم عرضها في القالب المحدد 'social/show_notifications.html'
    return {'notifications': notifications}
