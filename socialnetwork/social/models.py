from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Post(models.Model):
    body = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')



# نموذج يمثل التعليق (Comment) في قاعدة البيانات
class Comment(models.Model):
    # النص الفعلي للتعليق
    comment = models.TextField()

    # تاريخ ووقت إنشاء التعليق، يتم تعيينه تلقائيًا إلى الوقت الحالي
    created_on = models.DateTimeField(default=timezone.now)

    # المستخدم الذي كتب التعليق، يمثل علاقة خارجية مع نموذج المستخدم (User)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # المنشور المرتبط بالتعليق، يمثل علاقة خارجية مع نموذج المنشور (Post)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    # المستخدمون الذين قاموا بإعجاب التعليق، يمثل علاقة متعددة (ManyToMany) مع نموذج المستخدم
    likes = models.ManyToManyField(User, blank=True, related_name='comment_likes')

    # المستخدمون الذين قاموا بعدم إعجاب التعليق، يمثل علاقة متعددة (ManyToMany) مع نموذج المستخدم
    dislikes = models.ManyToManyField(User, blank=True, related_name='comment_dislikes')

    # إذا كان هذا التعليق ردًا على تعليق آخر، فإنه يشير إلى التعليق الأب (parent)
    # العلاقة مع الذات (self) تشير إلى التعليق الأب إذا كان موجودًا
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='+')

    # خاصية ترجع جميع التعليقات الفرعية (الأطفال) المرتبطة بهذا التعليق، مرتبة حسب تاريخ الإنشاء تنازليًا
    @property
    def children(self):
        return Comment.objects.filter(parent=self).order_by('-created_on').all()

    # خاصية تحدد ما إذا كان هذا التعليق هو تعليق أب (parent) أم لا
    @property
    def is_parent(self):
        # إذا لم يكن هناك تعليق أب، فهذا التعليق هو التعليق الأب
        if self.parent is None:
            return True
        return False

    
    # comment = models.TextField()
    # created_on = models.DateTimeField(default=timezone.now)
    # post = models.ForeignKey('Post', on_delete=models.CASCADE)
    # author = models.ForeignKey(User, on_delete=models.CASCADE)


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    birth_date=models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    picture = models.ImageField(upload_to='uploads/profile_pictures', default='uploads/profile_pictures/default.png', blank=True)
    followers = models.ManyToManyField(User, blank=True, related_name='followers')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        
# الدالة create_user_profile: تُنفذ بعد حفظ كائن User في قاعدة البيانات.
# sender: النموذج الذي أرسل الإشارة، وهو هنا User.
# instance: الكائن الذي تم حفظه، وهو هنا كائن User الجديد.
# created: قيمة Boolean تشير إلى ما إذا كان الكائن قد تم إنشاؤه حديثًا (True) أو تم تحديثه (False).
# **kwargs: يُستخدم لتمرير معلمات إضافية.

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
# create_user_profile: ينشئ ملفًا شخصيًا جديدًا عندما يتم إنشاء مستخدم جديد.
# save_user_profile: يحفظ ملف المستخدم الشخصي المرتبط إذا كان موجودًا، مما يضمن مزامنة أي تغييرات بين User و UserProfile.
    

class Notification(models.Model):
    # نوع الإشعار: 1 = إعجاب، 2 = تعليق، 3 = متابعة
    notification_type = models.IntegerField()

    # المستخدم الذي يتم إرسال الإشعار له
    to_user = models.ForeignKey(User, related_name='notification_to', on_delete=models.CASCADE, null=True)

    # المستخدم الذي أنشأ الإشعار (على سبيل المثال، الشخص الذي أعجب أو علّق أو تابع)
    from_user = models.ForeignKey(User, related_name='notification_from', on_delete=models.CASCADE, null=True)

    # المنشور المرتبط بالإشعار (يمكن أن يكون فارغًا إذا كان الإشعار لا يتعلق بمنشور)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='+', blank=True, null=True)

    # التعليق المرتبط بالإشعار (يمكن أن يكون فارغًا إذا كان الإشعار لا يتعلق بتعليق)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='+', blank=True, null=True)

    # تاريخ ووقت إنشاء الإشعار
    date = models.DateTimeField(default=timezone.now)

    # حالة الإشعار إذا تم رؤيته من قبل المستخدم المستهدف
    user_has_seen = models.BooleanField(default=False)
