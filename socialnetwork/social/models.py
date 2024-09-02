from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.



class Post(models.Model):
    shared_body = models.TextField(blank=True, null=True)
    body = models.TextField()
    #add
    #image = models.ImageField(upload_to='uploads/post_photos', blank=True, null=True)
    image = models.ManyToManyField('Image', blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    shared_on = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='+')
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')
    tags = models.ManyToManyField('Tag', blank=True)

    def create_tags(self):
        for word in self.body.split():
            if word.startswith('#'):
                tag, created = Tag.objects.get_or_create(name=word[1:])
                self.tags.add(tag)

        if self.shared_body:
            for word in self.shared_body.split():
                if word.startswith('#'):
                    tag, created = Tag.objects.get_or_create(name=word[1:])
                    self.tags.add(tag)

        self.save()

    class Meta:
        ordering = ['-created_on', '-shared_on']



# نموذج يمثل التعليق (Comment) في قاعدة البيانات

# class Comment(models.Model):
#     # النص الفعلي للتعليق
#     comment = models.TextField()

#     # تاريخ ووقت إنشاء التعليق، يتم تعيينه تلقائيًا إلى الوقت الحالي
#     created_on = models.DateTimeField(default=timezone.now)

#     # المستخدم الذي كتب التعليق، يمثل علاقة خارجية مع نموذج المستخدم (User)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)

#     # المنشور المرتبط بالتعليق، يمثل علاقة خارجية مع نموذج المنشور (Post)
#     post = models.ForeignKey('Post', on_delete=models.CASCADE)

#     # المستخدمون الذين قاموا بإعجاب التعليق، يمثل علاقة متعددة (ManyToMany) مع نموذج المستخدم
#     likes = models.ManyToManyField(User, blank=True, related_name='comment_likes')

#     # المستخدمون الذين قاموا بعدم إعجاب التعليق، يمثل علاقة متعددة (ManyToMany) مع نموذج المستخدم
#     dislikes = models.ManyToManyField(User, blank=True, related_name='comment_dislikes')

#     # إذا كان هذا التعليق ردًا على تعليق آخر، فإنه يشير إلى التعليق الأب (parent)
#     # العلاقة مع الذات (self) تشير إلى التعليق الأب إذا كان موجودًا
#     parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
#     tags = models.ManyToManyField('Tag', blank=True)

#     def create_tags(self):
#         for word in self.comment.split():
#             if word.startswith('#'):
#                 tag, created = Tag.objects.get_or_create(name=word[1:])
#                 self.tags.add(tag)
#         self.save()

#     # خاصية ترجع جميع التعليقات الفرعية (الأطفال) المرتبطة بهذا التعليق، مرتبة حسب تاريخ الإنشاء تنازليًا
#     @property
#     def children(self):
#         return Comment.objects.filter(parent=self).order_by('-created_on').all()

#     # خاصية تحدد ما إذا كان هذا التعليق هو تعليق أب (parent) أم لا
#     @property
#     def is_parent(self):
#         # إذا لم يكن هناك تعليق أب، فهذا التعليق هو التعليق الأب
#         if self.parent is None:
#             return True
#         return False

#     class Meta:
#         ordering = ['-created_on']


from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

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
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='+')

    # الوسوم المرتبطة بالتعليق
    tags = models.ManyToManyField('Tag', blank=True)

    # حقل الصورة لإضافة صورة واحدة إلى التعليق
    image = models.ImageField(upload_to='uploads/comment_images', blank=True, null=True)

    def create_tags(self):
        for word in self.comment.split():
            if word.startswith('#'):
                tag, created = Tag.objects.get_or_create(name=word[1:])
                self.tags.add(tag)
        self.save()

    @property
    def children(self):
        return Comment.objects.filter(parent=self).order_by('-created_on').all()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

    class Meta:
        ordering = ['-created_on']


# نموذج يمثل التعليق (Comment) في قاعدة البيانات
# class Comment(models.Model):
#     # النص الفعلي للتعليق
#     comment = models.TextField()

#     # تاريخ ووقت إنشاء التعليق، يتم تعيينه تلقائيًا إلى الوقت الحالي
#     created_on = models.DateTimeField(default=timezone.now)

#     # المستخدم الذي كتب التعليق، يمثل علاقة خارجية مع نموذج المستخدم (User)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)

#     # المنشور المرتبط بالتعليق، يمثل علاقة خارجية مع نموذج المنشور (Post)
#     post = models.ForeignKey('Post', on_delete=models.CASCADE)

#     # المستخدمون الذين قاموا بإعجاب التعليق، يمثل علاقة متعددة (ManyToMany) مع نموذج المستخدم
#     likes = models.ManyToManyField(User, blank=True, related_name='comment_likes')

#     # المستخدمون الذين قاموا بعدم إعجاب التعليق، يمثل علاقة متعددة (ManyToMany) مع نموذج المستخدم
#     dislikes = models.ManyToManyField(User, blank=True, related_name='comment_dislikes')

#     # إذا كان هذا التعليق ردًا على تعليق آخر، فإنه يشير إلى التعليق الأب (parent)
#     # العلاقة مع الذات (self) تشير إلى التعليق الأب إذا كان موجودًا
#     parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='+')

#     # خاصية ترجع جميع التعليقات الفرعية (الأطفال) المرتبطة بهذا التعليق، مرتبة حسب تاريخ الإنشاء تنازليًا
#     @property
#     def children(self):
#         return Comment.objects.filter(parent=self).order_by('-created_on').all()

#     # خاصية تحدد ما إذا كان هذا التعليق هو تعليق أب (parent) أم لا
#     @property
#     def is_parent(self):
#         # إذا لم يكن هناك تعليق أب، فهذا التعليق هو التعليق الأب
#         if self.parent is None:
#             return True
#         return False

    
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
    thread = models.ForeignKey('ThreadModel', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    # تاريخ ووقت إنشاء الإشعار
    date = models.DateTimeField(default=timezone.now)

    # حالة الإشعار إذا تم رؤيته من قبل المستخدم المستهدف
    user_has_seen = models.BooleanField(default=False)


class ThreadModel(models.Model):
    # `user`: يشير إلى المستخدم الذي بدأ المحادثة. الربط مع نموذج المستخدم الرئيسي `User` باستخدام `ForeignKey`.
    # `on_delete=models.CASCADE` يعني أنه إذا تم حذف هذا المستخدم، سيتم حذف جميع المحادثات المرتبطة به.
    # `related_name='+'` يعني أنه لن يتم إنشاء علاقة عكسية تلقائيًا لهذا الحقل، مما يعني أنه لا يمكن الوصول إلى المحادثات من خلال `user.threadmodel_set` على سبيل المثال.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')

    # `receiver`: يشير إلى المستخدم الذي يستقبل الرسائل في هذه المحادثة. مشابه للمستخدم الأول، يستخدم `ForeignKey` للربط مع نموذج `User`.
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')



class MessageModel(models.Model):
    # `thread`: يشير إلى المحادثة التي تنتمي إليها هذه الرسالة. الربط مع `ThreadModel` باستخدام `ForeignKey`.
    # `blank=True, null=True` يعني أن هذا الحقل يمكن أن يكون فارغًا (غير مملوء) أو يحتوي على قيمة `null`.
    thread = models.ForeignKey('ThreadModel', related_name='+', on_delete=models.CASCADE, blank=True, null=True)

    # `sender_user`: يشير إلى المستخدم الذي أرسل الرسالة. الربط مع نموذج المستخدم الرئيسي `User`.
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')

    # `receiver_user`: يشير إلى المستخدم الذي استقبل الرسالة. الربط مع نموذج المستخدم الرئيسي `User`.
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')

    # `body`: يحتوي على نص الرسالة. يستخدم `CharField` مع حد أقصى لطول النص (1000 حرف).
    body = models.CharField(max_length=1000)

    # `image`: يسمح بإرفاق صورة مع الرسالة. يستخدم `ImageField` لتخزين مسار الصورة المرفقة.
    # `upload_to='uploads/message_photos'` يحدد المسار الذي سيتم تخزين الصور فيه.
    # `blank=True, null=True` يعني أن هذا الحقل يمكن أن يكون فارغًا أو يحتوي على قيمة `null`.
    image = models.ImageField(upload_to='uploads/message_photos', blank=True, null=True)

    # `date`: يحتوي على تاريخ ووقت إرسال الرسالة. يتم تعيينه افتراضيًا إلى الوقت الحالي باستخدام `timezone.now`.
    date = models.DateTimeField(default=timezone.now)

    # `is_read`: حقل منطقي (Boolean) يشير إلى ما إذا كانت الرسالة قد تمت قراءتها أم لا. الافتراضي هو `False`.
    is_read = models.BooleanField(default=False)


class Image(models.Model):
	image = models.ImageField(upload_to='uploads/post_photos', blank=True, null=True)




class Tag(models.Model):
	name = models.CharField(max_length=255)