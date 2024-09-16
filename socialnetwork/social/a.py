from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpResponseRedirect,HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.views import View
from .models import *
from .forms import *
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib import messages
from django.utils import timezone


# Create your views here.

# class PostListView(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         posts = Post.objects.all().order_by('-created_on')
#         form = PostForm()

#         context = {
#             'post_list': posts,
#             'form': form,
#         }

#         return render(request, 'social/post_list.html', context)


#     def post(self, request, *args, **kwargs):
#         posts = Post.objects.all().order_by('-created_on')
#         form = PostForm(request.POST)

#         if form.is_valid():
#             new_post = form.save(commit=False)
#             new_post.author = request.user
#             new_post.save()

#         context = {
#             'post_list': posts,
#             #'posts': posts,  # تغيير الاسم إلى 'posts'
#             'form': form,
#         }

#         return render(request, 'social/post_list.html', context)

# class PostListView(LoginRequiredMixin, View):
#     # يُشترط أن يكون المستخدم مسجلاً للدخول للوصول إلى هذا العرض
#     def get(self, request, *args, **kwargs):
#         # الحصول على المستخدم الذي قام بتسجيل الدخول
#         logged_in_user = request.user
        
#         # الحصول على جميع المنشورات التي كتبها المستخدمون الذين يتابعهم المستخدم الحالي
#         # يتم استخدام `author__profile__followers__in=[logged_in_user.id]` للبحث عن المنشورات التي كتبها
#         # مستخدمون يتبعهم المستخدم الحالي
#         posts = Post.objects.filter(
#             author__profile__followers__in=[logged_in_user.id]
#         ).order_by('-created_on')  # ترتيب المنشورات من الأحدث إلى الأقدم
        
#         # إنشاء نموذج جديد للمنشورات
#         form = PostForm()

#         # إعداد السياق الذي سيتم تمريره إلى القالب
#         context = {
#             'post_list': posts,  # قائمة المنشورات التي سيتم عرضها
#             'form': form,        # نموذج لإضافة منشورات جديدة
#         }

#         # عرض قالب `post_list.html` مع السياق الذي يحتوي على المنشورات والنموذج
#         return render(request, 'social/post_list.html', context)

#     def post(self, request, *args, **kwargs):
#         logged_in_user = request.user
#         # الحصول على جميع المنشورات وترتيبها من الأحدث إلى الأقدم
#         posts = Post.objects.all().order_by('-created_on')
        
#         # إنشاء نموذج للمنشورات باستخدام البيانات المرسلة عبر POST
#         form = PostForm(request.POST,request.FILES)

#         # التحقق من صحة النموذج
#         if form.is_valid():
#             # حفظ المنشور الجديد بدون تقديمه مباشرة
#             new_post = form.save(commit=False)
#             # تعيين مؤلف المنشور إلى المستخدم الذي قام بتسجيل الدخول
#             new_post.author = request.user
#             # حفظ المنشور الجديد في قاعدة البيانات
#             new_post.save()

#         # إعداد السياق الذي سيتم تمريره إلى القالب
#         context = {
#             'post_list': posts,  # قائمة المنشورات التي سيتم عرضها
#             'form': form,        # نموذج لإضافة منشورات جديدة
#         }

#         # عرض قالب `post_list.html` مع السياق الذي يحتوي على المنشورات والنموذج
#         return render(request, 'social/post_list.html', context)

class PostListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logged_in_user = request.user
        posts = Post.objects.filter(
            author__profile__followers__in=[logged_in_user.id]
        ).order_by('-created_on')
        form = PostForm()
        share_form = ShareForm()


        context = {
            'post_list': posts,
            'shareform': share_form,
            'form': form,
        }

        return render(request, 'social/post_list.html', context)

    def post(self, request, *args, **kwargs):
        logged_in_user = request.user
        posts = Post.objects.filter(
            author__profile__followers__in=[logged_in_user.id]
        ).order_by('-created_on')
        form = PostForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')
        share_form = ShareForm()

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()

            new_post.create_tags()

            for f in files:
                img = Image(image=f)
                img.save()
                new_post.image.add(img)

            new_post.save()

        context = {
            'post_list': posts,
            'shareform': share_form,
            'form': form,
        }

        return render(request, 'social/post_list.html', context)    
# class PostDetailView(View):
#     def get(self, request,pk, *args, **kwargs):
#         post=Post.objects.get(pk=pk)
#         form = CommentForm()
#         context ={
#             'post':post
#         }

#         return render(request,'social/post_detail.html', context)
   
# # def post(self, request, pk, *args, **kwargs):

# # هذه هي تعريف دالة post التي تتعامل مع طلبات POST إلى الخادم.
# # self: إشارة إلى الكائن الذي يستدعي هذه الدالة، وهي عادةً طريقة داخل فئة (مثل DetailView أو CreateView).
# # request: يمثل الطلب الوارد من المستخدم، والذي يحتوي على بيانات الطلب مثل البيانات المرسلة عبر النموذج.
# # pk: هذا هو المفتاح الأساسي (Primary Key) للكائن الذي يتفاعل معه العرض (مثل منشور معين).
# # *args و **kwargs: هذه المعاملات تستخدم لتمرير أي وسائط إضافية إلى الدالة، وهي مفيدة إذا كان هناك وسائط إضافية غير معروفة مقدماً.
# # post = Post.objects.get(pk=pk)

# # يقوم هذا السطر بجلب الكائن Post من قاعدة البيانات الذي يطابق المفتاح الأساسي الممرر (pk).
# # Post.objects.get(pk=pk): هذه هي الطريقة القياسية في Django لجلب كائن محدد من قاعدة البيانات باستخدام مفتاحه الأساسي.
# # form = CommentForm(request.POST)

# # هنا يتم إنشاء نموذج CommentForm باستخدام البيانات التي أرسلها المستخدم عبر الطلب.
# # request.POST: يحتوي على البيانات المرسلة عبر نموذج HTML عندما يقوم المستخدم بملء النموذج وتقديمه. يتم تمرير هذه البيانات إلى نموذج CommentForm للتحقق منها أو حفظها.
# # context = { 'post': post }

# # يتم إنشاء قاموس (Dictionary) يسمى context يحتوي على البيانات التي قد تحتاج إلى تمريرها إلى القالب (Template) لاحقًا. 
#     def post(self, request,pk, *args, **kwargs):
#         post=Post.objects.get(pk=pk)
#         form = CommentForm(request.POST)

#         if form.is_valid():
#             new_comment = form.save(commit=False)
#             new_comment.author = request.user
#             new_comment.post = post
#             new_comment.save()

#         context ={
#             'post':post
#         }

#         return render(request,'social/post_detail.html', context)
    

# class PostDetailView(View):

#     def get(self, request, pk, *args, **kwargs):
#         # جلب المنشور باستخدام المفتاح الأساسي (pk) 
#         post = Post.objects.get(pk=pk)
#         # إنشاء نموذج تعليق فارغ
#         form = CommentForm()

#         comments = Comment.objects.filter(post=post).order_by('-created_on')
#         # إنشاء قاموس للسياق يحتوي على المنشور فقط في الوقت الحالي
#         context = {
#             'post': post,
#             'form': form,
#             'comments':comments
#         }
#         # عرض الصفحة باستخدام القالب مع تمرير السياق
#         return render(request, 'social/post_detail.html', context)

#     def post(self, request, pk, *args, **kwargs):
#         # جلب المنشور باستخدام المفتاح الأساسي (pk) 
#         post = Post.objects.get(pk=pk)
#         # إنشاء نموذج تعليق باستخدام البيانات المرسلة من قبل المستخدم
#         form = CommentForm(request.POST)

#         # التحقق من صحة النموذج
#         if form.is_valid():
#             # إنشاء تعليق جديد ولكن بدون حفظه في قاعدة البيانات حتى الآن
#             new_comment = form.save(commit=False)
#             # تعيين المستخدم الحالي ككاتب للتعليق
#             new_comment.author = request.user
#             # ربط التعليق بالمنشور الحالي
#             new_comment.post = post
#             # حفظ التعليق في قاعدة البيانات
#             new_comment.save()

#         comments = Comment.objects.filter(post=post).order_by('-created_on')

#         # إنشاء قاموس للسياق يحتوي على المنشور والنموذج
#         context = {
#             'post': post,
#             'form': form,
#             'comments':comments
#         }

#         # عرض الصفحة باستخدام القالب مع تمرير السياق
#         return render(request, 'social/post_detail.html', context)

    
class PostDetailView(LoginRequiredMixin,  View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm()
        
        comments = Comment.objects.filter(post=post).order_by('-created_on')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }

        return render(request, 'social/post_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

            new_comment.create_tags()
        
        comments = Comment.objects.filter(post=post).order_by('-created_on')
        notification = Notification.objects.create(notification_type=2, from_user=request.user, to_user=post.author, post=post)

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }

        return render(request, 'social/post_detail.html', context)
    
class PostEditView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['body']
    template_name = 'social/post_edit.html'
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('post-detail', kwargs={'pk': pk})
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Post
    template_name = 'social/post_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class SharedPostView(View):
    def post(self, request, pk, *args, **kwargs):
       original_post = Post.objects.get(pk=pk)
       form = ShareForm(request.POST)

       if form.is_valid():
            new_post = Post(
                shared_body=self.request.POST.get('body'),
                body=original_post.body,
                author=original_post.author,
                created_on=original_post.created_on,
                shared_user=request.user,
                shared_on=timezone.now(),
            )
            new_post.save()

            for img in original_post.image.all():
                new_post.image.add(img)

            new_post.save()

       return redirect('post-list')


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Comment
    template_name = 'social/comment_delete.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('post-detail', kwargs={'pk': pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    

class ProfileView(View):
    def get(self, request, pk, *args, **kwargs):
        
        # الحصول على كائن الملف الشخصي باستخدام المعرف (pk)
        profile = UserProfile.objects.get(pk=pk)
        
        # الحصول على المستخدم المرتبط بهذا الملف الشخصي
        user = profile.user
        
        # استرجاع المشاركات التي أنشأها المستخدم وترتيبها بترتيب تنازلي حسب تاريخ الإنشاء
        posts = Post.objects.filter(author=user).order_by('-created_on')

        # إعداد السياق الذي سيتم تمريره إلى القالب
        # # context = {
        #     'user': user,
        #     'profile': profile,
        #     'posts': posts
        # }

        followers = profile.followers.all()

        if len(followers) == 0:
            is_following = False

        for follower in followers:
            if follower == request.user:
                is_following = True
                break
            else:
                is_following = False

        number_of_followers = len(followers)

        context = {
            'user': user,
            'profile': profile,
            'posts': posts,
            'number_of_followers': number_of_followers,
            'is_following': is_following,
        }

        # عرض القالب 'profile.html' مع تمرير السياق
        return render(request, 'social/profile.html', context)
    

class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    fields = ['name', 'bio', 'birth_date', 'location', 'picture']
    template_name = 'social/profile_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('profile', kwargs={'pk': pk})

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user
    

class AddFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.add(request.user)

        notification = Notification.objects.create(notification_type=3, from_user=request.user, to_user=profile.user)


        return redirect('profile', pk=profile.pk)

class RemoveFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.remove(request.user)

        return redirect('profile', pk=profile.pk)
    

# الفئة AddLike تقوم بإدارة إضافة أو إزالة الإعجابات من منشور.
# هذه الفئة تتطلب أن يكون المستخدم مسجلاً للدخول، لذا نستخدم LoginRequiredMixin.

class AddLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        # نحصل على المنشور الذي نريد إضافة الإعجاب إليه بناءً على المفتاح الأساسي (pk).
        post = Post.objects.get(pk=pk)

        # نتحقق إذا كان المستخدم قد قام بالفعل بعدم الإعجاب بالمنشور.
        is_dislike = False
        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        # إذا كان المستخدم قد قام بعدم الإعجاب سابقًا، نزيل عدم الإعجاب.
        if is_dislike:
            post.dislikes.remove(request.user)

        # نتحقق إذا كان المستخدم قد أعجب بالفعل بالمنشور.
        is_like = False
        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        # إذا لم يقم المستخدم بالإعجاب سابقًا، نضيف الإعجاب.
        if not is_like:
            post.likes.add(request.user)
            notification = Notification.objects.create(notification_type=1, from_user=request.user, to_user=post.author, post=post)


        # إذا كان المستخدم قد قام بالإعجاب سابقًا، نزيل الإعجاب.
        if is_like:
            post.likes.remove(request.user)

        # نعيد توجيه المستخدم إلى الصفحة السابقة بعد إتمام العملية.
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


class AddDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        # الحصول على المنشور باستخدام المعرف (pk)
        post = Post.objects.get(pk=pk)

        # التحقق مما إذا كان المستخدم قد أعجب بالمنشور بالفعل
        is_like = False
        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        # إذا كان المستخدم قد أعجب بالمنشور بالفعل، قم بإزالة الإعجاب
        if is_like:
            post.likes.remove(request.user)

        # التحقق مما إذا كان المستخدم قد أضاف "عدم إعجاب" (Dislike) للمنشور بالفعل
        is_dislike = False
        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        # إذا لم يكن المستخدم قد أضاف "عدم إعجاب" بالفعل، قم بإضافته
        if not is_dislike:
            post.dislikes.add(request.user)

        # إذا كان المستخدم قد أضاف "عدم إعجاب" بالفعل، قم بإزالته
        if is_dislike:
            post.dislikes.remove(request.user)

        # إعادة التوجيه إلى الصفحة السابقة أو الصفحة الرئيسية
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


# تعريف View للبحث عن المستخدمين
class UserSearch(View):
    def get(self, request, *args, **kwargs):
        # الحصول على قيمة البحث من المستخدم (من الـ GET request)
        query = self.request.GET.get('query')
        
        #الرمز Q في Django يشير إلى كائنات Q objects التي تُستخدم لبناء استعلامات معقدة في قاعدة البيانات، وخاصة عندما تحتاج إلى استخدام شروط منطقية مثل OR وAND في استعلام واحد.
        # تصفية قائمة ملفات المستخدمين بناءً على اسم المستخدم المطابق للقيمة المدخلة في البحث
        profile_list = UserProfile.objects.filter(
            Q(user__username__icontains=query)  # البحث في أسماء المستخدمين التي تحتوي على النص المدخل
        )

        # إعداد البيانات التي سيتم تمريرها إلى القالب (template)
        context = {
            'profile_list': profile_list,  # قائمة ملفات المستخدمين المطابقة للبحث
        }

        # إعادة عرض صفحة البحث مع البيانات المفلترة
        return render(request, 'social/search.html', context)
    
    
class ListFollowers(View):
    def get(self, request, pk, *args, **kwargs):
        # الحصول على ملف تعريف المستخدم بناءً على الـ primary key (pk) المرسل في الطلب
        profile = UserProfile.objects.get(pk=pk)
        
        # الحصول على جميع المتابعين لهذا الملف الشخصي
        followers = profile.followers.all()

        # إعداد السياق الذي سيتم تمريره إلى القالب
        context = {
            'profile': profile,      # الملف الشخصي للمستخدم الذي يتم عرض قائمة المتابعين له
            'followers': followers,  # قائمة المتابعين للمستخدم
        }

        # عرض قالب `followers_list.html` مع السياق الذي يحتوي على الملف الشخصي وقائمة المتابعين
        return render(request, 'social/followers_list.html', context)



class CommentReplyView(LoginRequiredMixin, View):
    def post(self, request, post_pk, pk, *args, **kwargs):
        post = Post.objects.get(pk=post_pk)
        parent_comment = Comment.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.parent = parent_comment
            new_comment.save()

        notification = Notification.objects.create(notification_type=2, from_user=request.user, to_user=parent_comment.author, comment=new_comment)

        return redirect('post-detail', pk=post_pk)
    
    

class AddCommentLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        is_dislike = False

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            comment.dislikes.remove(request.user)

        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            comment.likes.add(request.user)
            notification = Notification.objects.create(notification_type=1, from_user=request.user, to_user=comment.author, comment=comment)


        if is_like:
            comment.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class AddCommentDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            comment.likes.remove(request.user)

        is_dislike = False

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            comment.dislikes.add(request.user)

        if is_dislike:
            comment.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


class PostNotification(View):
    def get(self, request, notification_pk, post_pk, *args, **kwargs):
        # الحصول على الإشعار المحدد باستخدام معرف الإشعار (notification_pk)
        notification = Notification.objects.get(pk=notification_pk)
        
        # الحصول على المنشور المحدد باستخدام معرف المنشور (post_pk)
        post = Post.objects.get(pk=post_pk)

        # تعيين علامة بأن المستخدم قد شاهد الإشعار
        notification.user_has_seen = True
        notification.save()

        # إعادة توجيه المستخدم إلى صفحة تفاصيل المنشور
        return redirect('post-detail', pk=post_pk)


class FollowNotification(View):
    def get(self, request, notification_pk, profile_pk, *args, **kwargs):
        # الحصول على الإشعار المحدد باستخدام معرف الإشعار (notification_pk)
        notification = Notification.objects.get(pk=notification_pk)
        
        # الحصول على الملف الشخصي للمستخدم الذي تم متابعته باستخدام معرف الملف الشخصي (profile_pk)
        profile = UserProfile.objects.get(pk=profile_pk)

        # تعيين علامة بأن المستخدم قد شاهد الإشعار
        notification.user_has_seen = True
        notification.save()

        # إعادة توجيه المستخدم إلى صفحة الملف الشخصي للمستخدم الذي تم متابعته
        return redirect('profile', pk=profile_pk)
    
class ThreadNotification(View):
    def get(self, request, notification_pk, object_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        thread = ThreadModel.objects.get(pk=object_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('thread', pk=object_pk)


class RemoveNotification(View):
    def delete(self, request, notification_pk, *args, **kwargs):
        # الحصول على الإشعار المحدد باستخدام معرف الإشعار (notification_pk)
        notification = Notification.objects.get(pk=notification_pk)

        # تعيين علامة بأن المستخدم قد شاهد الإشعار
        notification.user_has_seen = True
        notification.save()

        # إرسال استجابة تفيد بنجاح العملية
        return HttpResponse('Success', content_type='text/plain')


class ListThreads(View):
    #نستخدم Q من django.db.models لإنشاء شرط تصفية معقد يسمح لنا بالبحث عن المحادثات التي يكون فيها المستخدم الحالي إما منشئ المحادثة (user) أو المستقبل للمحادثة (receiver).

    # الدالة `get` تُنفذ عند إرسال طلب GET إلى هذا العرض.
    def get(self, request, *args, **kwargs):
        # نقوم بتصفية المحادثات (`ThreadModel`) التي يكون فيها المستخدم الحالي إما المستخدم الذي أنشأ المحادثة (user)
        # أو المستقبل للمحادثة (receiver). نستخدم `Q` للتصفية بناءً على شرط OR (إما أن يكون المستخدم الحالي هو المستخدم الأول أو المستقبل).
        threads = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user))

        # نقوم بتمرير المحادثات المستخرجة إلى القالب عن طريق إنشاء سياق (`context`) يحتوي على المفتاح 'threads'.
        context = {
            'threads': threads
        }

        # نقوم بعرض صفحة HTML (`inbox.html`) باستخدام القالب `social/inbox.html`، وتمرير البيانات المخزنة في `context` إلى القالب.
        return render(request, 'social/inbox.html', context)

class CreateThread(View):
    # الدالة `get` تُنفذ عند إرسال طلب GET إلى هذا العرض.
    def get(self, request, *args, **kwargs):
        # نقوم بإنشاء نموذج (form) فارغ من النموذج `ThreadForm`.
        form = ThreadForm()

        # نقوم بتمرير النموذج إلى القالب عن طريق إنشاء سياق (`context`) يحتوي على المفتاح 'form'.
        context = {
            'form': form
        }

        # نقوم بعرض صفحة HTML (`create_thread.html`) باستخدام القالب `social/create_thread.html`، وتمرير البيانات المخزنة في `context` إلى القالب.
        return render(request, 'social/create_thread.html', context)

    # الدالة `post` تُنفذ عند إرسال طلب POST إلى هذا العرض.
    def post(self, request, *args, **kwargs):
        # نقوم بإنشاء نموذج (form) باستخدام البيانات التي تم إرسالها من قبل المستخدم عبر الطلب.
        form = ThreadForm(request.POST)

        # نحصل على اسم المستخدم الذي أدخله المستخدم في النموذج.
        username = request.POST.get('username')

        try:
            # نحاول العثور على المستخدم في قاعدة البيانات باستخدام اسم المستخدم الذي أدخله المستخدم.
            receiver = User.objects.get(username=username)
            
            # نتحقق مما إذا كانت هناك محادثة سابقة بين المستخدم الحالي والمستخدم الذي أدخل اسمه (receiver).
            if ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
                # إذا كانت المحادثة موجودة، نقوم بإعادة توجيه المستخدم إلى تلك المحادثة.
                thread = ThreadModel.objects.filter(user=request.user, receiver=receiver)[0]
                return redirect('thread', pk=thread.pk)
            elif ThreadModel.objects.filter(user=receiver, receiver=request.user).exists():
                # نتحقق أيضًا إذا كان المستخدم الآخر قد بدأ محادثة مع المستخدم الحالي، وإذا كانت موجودة نقوم بإعادة التوجيه إلى تلك المحادثة.
                thread = ThreadModel.objects.filter(user=receiver, receiver=request.user)[0]
                return redirect('thread', pk=thread.pk)

            # إذا كان النموذج صحيحًا (is_valid)، نقوم بإنشاء محادثة جديدة.
            if form.is_valid():
                thread = ThreadModel(
                    user=request.user,
                    receiver=receiver
                )
                thread.save()

                # بعد إنشاء المحادثة الجديدة، نقوم بإعادة التوجيه إلى صفحة المحادثة.
                return redirect('thread', pk=thread.pk)
        except:
            messages.error(request, 'Invalid username')
            # إذا حدث خطأ (مثل عدم العثور على المستخدم)، نقوم بإعادة توجيه المستخدم إلى صفحة إنشاء المحادثة مجددًا.
            return redirect('create-thread')


class ThreadView(View):
    # الدالة `get` تُنفذ عند إرسال طلب GET إلى هذا العرض.
    def get(self, request, pk, *args, **kwargs):
        # نقوم بإنشاء نموذج فارغ للرسالة ليتم عرضه في صفحة المحادثة.
        form = MessageForm()

        # نجلب المحادثة (thread) من قاعدة البيانات باستخدام معرف المحادثة (pk).
        thread = ThreadModel.objects.get(pk=pk)

        # نقوم بجلب قائمة الرسائل التي تنتمي إلى هذه المحادثة من قاعدة البيانات.
        # نستخدم `filter` لجلب جميع الرسائل التي تحتوي على معرف المحادثة.
        message_list = MessageModel.objects.filter(thread__pk__contains=pk)

        # نقوم بتجهيز البيانات (context) التي سيتم تمريرها إلى القالب لعرضها.
        context = {
            'thread': thread,               # المحادثة الحالية.
            'form': form,                   # نموذج الرسالة الفارغ.
            'message_list': message_list    # قائمة الرسائل في المحادثة.
        }

        # نقوم بعرض صفحة المحادثة (`thread.html`) مع تمرير البيانات اللازمة إليها.
        return render(request, 'social/thread.html', context)


class CreateMessage(View):
    def post(self, request, pk, *args, **kwargs):
        form = MessageForm(request.POST, request.FILES)
        thread = ThreadModel.objects.get(pk=pk)
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver

        if form.is_valid():
            message = form.save(commit=False)
            message.thread = thread
            message.sender_user = request.user
            message.receiver_user = receiver
            message.save()

        notification = Notification.objects.create(
            notification_type=4,
            from_user=request.user,
            to_user=receiver,
            thread=thread
        )
        return redirect('thread', pk=pk)

# class CreateMessage(View):
#     # الدالة `post` تُنفذ عند إرسال طلب POST إلى هذا العرض.
#     def post(self, request, pk, *args, **kwargs):
#         # نقوم بجلب المحادثة (thread) من قاعدة البيانات باستخدام معرف المحادثة (pk).
#         thread = ThreadModel.objects.get(pk=pk)
        
#         # نتحقق من هو المستقبل (receiver) في هذه المحادثة.
#         # إذا كان المستخدم الحالي هو المستقبل في المحادثة، نعين المرسل (user) كـ المستقبل.
#         if thread.receiver == request.user:
#             receiver = thread.user
#         else:
#             # إذا لم يكن المستخدم الحالي هو المستقبل، نعين المستقبل كـ receiver في المحادثة.
#             receiver = thread.receiver

#         # نقوم بإنشاء رسالة جديدة باستخدام البيانات التي تم إدخالها في النموذج.
#         message = MessageModel(
#             thread=thread,                  # المحادثة التي تنتمي إليها الرسالة.
#             sender_user=request.user,       # المستخدم الذي أرسل الرسالة (المستخدم الحالي).
#             receiver_user=receiver,         # المستخدم الذي سيتلقى الرسالة.
#             body=request.POST.get('message') # نص الرسالة المرسل من قبل المستخدم.
#         )

#         # نقوم بحفظ الرسالة الجديدة في قاعدة البيانات.
#         message.save()

#         notification = Notification.objects.create(
#             notification_type=4,
#             from_user=request.user,
#             to_user=receiver,
#             thread=thread
#         )
        
#         # بعد حفظ الرسالة، نقوم بإعادة توجيه المستخدم إلى صفحة المحادثة الحالية.
#         return redirect('thread', pk=pk)
# class PostListView(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         posts = Post.objects.all().order_by('-created_on')
#         form = PostForm()

#         context = {
#             'post_list': posts,
#             'form': form,
#         }

#         return render(request, 'social/post_list.html', context)


#     def post(self, request, *args, **kwargs):
#         posts = Post.objects.all().order_by('-created_on')
#         form = PostForm(request.POST)

#         if form.is_valid():
#             new_post = form.save(commit=False)
#             new_post.author = request.user
#             new_post.save()

#         context = {
#             'post_list': posts,
#             #'posts': posts,  # تغيير الاسم إلى 'posts'
#             'form': form,
#         }

#         return render(request, 'social/post_list.html', context)

# class PostListView(LoginRequiredMixin, View):
#     # يُشترط أن يكون المستخدم مسجلاً للدخول للوصول إلى هذا العرض
#     def get(self, request, *args, **kwargs):
#         # الحصول على المستخدم الذي قام بتسجيل الدخول
#         logged_in_user = request.user
        
#         # الحصول على جميع المنشورات التي كتبها المستخدمون الذين يتابعهم المستخدم الحالي
#         # يتم استخدام `author__profile__followers__in=[logged_in_user.id]` للبحث عن المنشورات التي كتبها
#         # مستخدمون يتبعهم المستخدم الحالي
#         posts = Post.objects.filter(
#             author__profile__followers__in=[logged_in_user.id]
#         ).order_by('-created_on')  # ترتيب المنشورات من الأحدث إلى الأقدم
        
#         # إنشاء نموذج جديد للمنشورات
#         form = PostForm()

#         # إعداد السياق الذي سيتم تمريره إلى القالب
#         context = {
#             'post_list': posts,  # قائمة المنشورات التي سيتم عرضها
#             'form': form,        # نموذج لإضافة منشورات جديدة
#         }

#         # عرض قالب `post_list.html` مع السياق الذي يحتوي على المنشورات والنموذج
#         return render(request, 'social/post_list.html', context)

#     def post(self, request, *args, **kwargs):
#         logged_in_user = request.user
#         # الحصول على جميع المنشورات وترتيبها من الأحدث إلى الأقدم
#         posts = Post.objects.all().order_by('-created_on')
        
#         # إنشاء نموذج للمنشورات باستخدام البيانات المرسلة عبر POST
#         form = PostForm(request.POST,request.FILES)

#         # التحقق من صحة النموذج
#         if form.is_valid():
#             # حفظ المنشور الجديد بدون تقديمه مباشرة
#             new_post = form.save(commit=False)
#             # تعيين مؤلف المنشور إلى المستخدم الذي قام بتسجيل الدخول
#             new_post.author = request.user
#             # حفظ المنشور الجديد في قاعدة البيانات
#             new_post.save()

#         # إعداد السياق الذي سيتم تمريره إلى القالب
#         context = {
#             'post_list': posts,  # قائمة المنشورات التي سيتم عرضها
#             'form': form,        # نموذج لإضافة منشورات جديدة
#         }

#         # عرض قالب `post_list.html` مع السياق الذي يحتوي على المنشورات والنموذج
#         return render(request, 'social/post_list.html', context)
    # class PostDetailView(View):
#     def get(self, request,pk, *args, **kwargs):
#         post=Post.objects.get(pk=pk)
#         form = CommentForm()
#         context ={
#             'post':post
#         }

#         return render(request,'social/post_detail.html', context)
   
# # def post(self, request, pk, *args, **kwargs):

# # هذه هي تعريف دالة post التي تتعامل مع طلبات POST إلى الخادم.
# # self: إشارة إلى الكائن الذي يستدعي هذه الدالة، وهي عادةً طريقة داخل فئة (مثل DetailView أو CreateView).
# # request: يمثل الطلب الوارد من المستخدم، والذي يحتوي على بيانات الطلب مثل البيانات المرسلة عبر النموذج.
# # pk: هذا هو المفتاح الأساسي (Primary Key) للكائن الذي يتفاعل معه العرض (مثل منشور معين).
# # *args و **kwargs: هذه المعاملات تستخدم لتمرير أي وسائط إضافية إلى الدالة، وهي مفيدة إذا كان هناك وسائط إضافية غير معروفة مقدماً.
# # post = Post.objects.get(pk=pk)

# # يقوم هذا السطر بجلب الكائن Post من قاعدة البيانات الذي يطابق المفتاح الأساسي الممرر (pk).
# # Post.objects.get(pk=pk): هذه هي الطريقة القياسية في Django لجلب كائن محدد من قاعدة البيانات باستخدام مفتاحه الأساسي.
# # form = CommentForm(request.POST)

# # هنا يتم إنشاء نموذج CommentForm باستخدام البيانات التي أرسلها المستخدم عبر الطلب.
# # request.POST: يحتوي على البيانات المرسلة عبر نموذج HTML عندما يقوم المستخدم بملء النموذج وتقديمه. يتم تمرير هذه البيانات إلى نموذج CommentForm للتحقق منها أو حفظها.
# # context = { 'post': post }

# # يتم إنشاء قاموس (Dictionary) يسمى context يحتوي على البيانات التي قد تحتاج إلى تمريرها إلى القالب (Template) لاحقًا. 
#     def post(self, request,pk, *args, **kwargs):
#         post=Post.objects.get(pk=pk)
#         form = CommentForm(request.POST)

#         if form.is_valid():
#             new_comment = form.save(commit=False)
#             new_comment.author = request.user
#             new_comment.post = post
#             new_comment.save()

#         context ={
#             'post':post
#         }

#         return render(request,'social/post_detail.html', context)
    

# class PostDetailView(View):

#     def get(self, request, pk, *args, **kwargs):
#         # جلب المنشور باستخدام المفتاح الأساسي (pk) 
#         post = Post.objects.get(pk=pk)
#         # إنشاء نموذج تعليق فارغ
#         form = CommentForm()

#         comments = Comment.objects.filter(post=post).order_by('-created_on')
#         # إنشاء قاموس للسياق يحتوي على المنشور فقط في الوقت الحالي
#         context = {
#             'post': post,
#             'form': form,
#             'comments':comments
#         }
#         # عرض الصفحة باستخدام القالب مع تمرير السياق
#         return render(request, 'social/post_detail.html', context)

#     def post(self, request, pk, *args, **kwargs):
#         # جلب المنشور باستخدام المفتاح الأساسي (pk) 
#         post = Post.objects.get(pk=pk)
#         # إنشاء نموذج تعليق باستخدام البيانات المرسلة من قبل المستخدم
#         form = CommentForm(request.POST)

#         # التحقق من صحة النموذج
#         if form.is_valid():
#             # إنشاء تعليق جديد ولكن بدون حفظه في قاعدة البيانات حتى الآن
#             new_comment = form.save(commit=False)
#             # تعيين المستخدم الحالي ككاتب للتعليق
#             new_comment.author = request.user
#             # ربط التعليق بالمنشور الحالي
#             new_comment.post = post
#             # حفظ التعليق في قاعدة البيانات
#             new_comment.save()

#         comments = Comment.objects.filter(post=post).order_by('-created_on')

#         # إنشاء قاموس للسياق يحتوي على المنشور والنموذج
#         context = {
#             'post': post,
#             'form': form,
#             'comments':comments
#         }

#         # عرض الصفحة باستخدام القالب مع تمرير السياق
#         return render(request, 'social/post_detail.html', context)

    
# class PostDetailView(LoginRequiredMixin,  View):
#     def get(self, request, pk, *args, **kwargs):
#         post = Post.objects.get(pk=pk)
#         form = CommentForm()
        
#         comments = Comment.objects.filter(post=post).order_by('-created_on')

#         context = {
#             'post': post,
#             'form': form,
#             'comments': comments,
#         }

#         return render(request, 'social/post_detail.html', context)

#     def post(self, request, pk, *args, **kwargs):
#         post = Post.objects.get(pk=pk)
#         form = CommentForm(request.POST)

#         if form.is_valid():
#             new_comment = form.save(commit=False)
#             new_comment.author = request.user
#             new_comment.post = post
#             new_comment.save()

#             new_comment.create_tags()
        
#         comments = Comment.objects.filter(post=post).order_by('-created_on')
#         notification = Notification.objects.create(notification_type=2, from_user=request.user, to_user=post.author, post=post)

#         context = {
#             'post': post,
#             'form': form,
#             'comments': comments,
#         }

#         return render(request, 'social/post_detail.html', context)
    # class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = UserProfile
#     form_class = UserProfileForm
#     template_name = 'social/profile_edit.html'

#     # def form_valid(self, form):
#     #     # تحديث username للمستخدم
#     #     user = form.instance.user
#     #     user.username = form.cleaned_data['username']
#     #     user.email = form.cleaned_data['email']  # تحديث البريد الإلكتروني
#     #     user.save()  # حفظ التعديلات في User
#     #     return super().form_valid(form)

#     def form_valid(self, form):
#      user = form.instance.user
#      print("Username:", form.cleaned_data['username'])
#      print("Email:", form.cleaned_data['email'])
#      user.username = form.cleaned_data['username']
#      user.email = form.cleaned_data['email']
#      print("Username:", form.cleaned_data['username'])
#      print("Email:", form.cleaned_data['email'])
#      user.save()

#      return super().form_valid(form)
    
    # def check_username_availability(request):
#     username = request.GET.get('username', None)
#     is_available = not User.objects.filter(username=username).exists()
#     return JsonResponse({'is_available': is_available})
# def get_success_url(self):
#     return reverse_lazy('profile', kwargs={'pk': self.object.pk})
# class CommentReplyView(LoginRequiredMixin, View):
#     def post(self, request, post_pk, pk, *args, **kwargs):
#         post = Post.objects.get(pk=post_pk)
#         parent_comment = Comment.objects.get(pk=pk)
#         form = CommentForm(request.POST)

#         if form.is_valid():
#             new_comment = form.save(commit=False)
#             new_comment.author = request.user
#             new_comment.post = post
#             new_comment.parent = parent_comment
#             new_comment.save()

#         notification = Notification.objects.create(notification_type=2, from_user=request.user, to_user=parent_comment.author, comment=new_comment)

#         return redirect('post-detail', pk=post_pk)
# class CreateMessage(View):
#     # الدالة `post` تُنفذ عند إرسال طلب POST إلى هذا العرض.
#     def post(self, request, pk, *args, **kwargs):
#         # نقوم بجلب المحادثة (thread) من قاعدة البيانات باستخدام معرف المحادثة (pk).
#         thread = ThreadModel.objects.get(pk=pk)
        
#         # نتحقق من هو المستقبل (receiver) في هذه المحادثة.
#         # إذا كان المستخدم الحالي هو المستقبل في المحادثة، نعين المرسل (user) كـ المستقبل.
#         if thread.receiver == request.user:
#             receiver = thread.user
#         else:
#             # إذا لم يكن المستخدم الحالي هو المستقبل، نعين المستقبل كـ receiver في المحادثة.
#             receiver = thread.receiver

#         # نقوم بإنشاء رسالة جديدة باستخدام البيانات التي تم إدخالها في النموذج.
#         message = MessageModel(
#             thread=thread,                  # المحادثة التي تنتمي إليها الرسالة.
#             sender_user=request.user,       # المستخدم الذي أرسل الرسالة (المستخدم الحالي).
#             receiver_user=receiver,         # المستخدم الذي سيتلقى الرسالة.
#             body=request.POST.get('message') # نص الرسالة المرسل من قبل المستخدم.
#         )

#         # نقوم بحفظ الرسالة الجديدة في قاعدة البيانات.
#         message.save()

#         notification = Notification.objects.create(
#             notification_type=4,
#             from_user=request.user,
#             to_user=receiver,
#             thread=thread
#         )
        
#         # بعد حفظ الرسالة، نقوم بإعادة توجيه المستخدم إلى صفحة المحادثة الحالية.
#         return redirect('thread', pk=pk)
    # def post(self, request, *args, **kwargs):
    #     explore_form = ExploreForm(request.POST)
    #     if explore_form.is_valid():
    #         query = explore_form.cleaned_data['query']
    #         tag = Tag.objects.filter(name=query).first()

    #         if tag:
    #             posts = Post.objects.filter(tags__in=[tag])
                
    #             # إذا لم يكن هناك أي منشورات مرتبطة بالوسم
    #             if not posts.exists():
    #                 messages.error(request, 'No posts found for this tag.')
    #                 return redirect('explore')  # إعادة التوجيه إلى صفحة البحث
    #         else:
    #             # إذا لم يتم العثور على الوسم
    #             messages.error(request, 'Tag not found.')
    #             return redirect('explore')  # إعادة التوجيه إلى صفحة البحث
            
    #         # إذا تم العثور على الوسم والمنشورات، نقوم بإعادة التوجيه مع الاستعلام
    #         return redirect(f'/social/explore?query={query}')
        
    #     # إذا كان النموذج غير صالح
    #     messages.error(request, 'Invalid search query.')
    #     return redirect('/social/explore')
    


# في دالة post:
# المقصود: عند إرسال نموذج من قبل المستخدم (مثل نموذج البحث)، فإن دالة post تتعامل مع البيانات التي أرسلها المستخدم.
# أين تظهر رسالة الخطأ: إذا كان هناك خطأ في البيانات المرسلة، مثل إدخال غير صحيح أو عدم وجود وسم في قاعدة البيانات، فإن رسالة الخطأ تظهر مباشرة بعد محاولة المستخدم إرسال البيانات. هذا يعني أن الرسالة تكون أمام المستخدم مباشرة بعد إجراء العملية، وتساعده على فهم السبب وتوجيهه لإصلاح الخطأ.
# في دالة get:
# المقصود: دالة get تُستخدم لعرض البيانات على الصفحة عند تحميلها، سواء كان ذلك لأول مرة أو بعد إعادة التوجيه من دالة post.

# def post(self, request, *args, **kwargs):
#         explore_form = ExploreForm(request.POST)
#         if explore_form.is_valid():
#             query = explore_form.cleaned_data['query']
#             tag = Tag.objects.filter(name=query).first()

#             posts = None
#             if tag:
#                 posts = Post.objects.filter(tags__in=[tag])

#             if posts:
#                 context = {
#                     'tag': tag,
#                     'posts': posts,
#                 }
#             else:
#                 context = {
#                     'tag': tag,
#                 }
#             return redirect(f'/social/explore?query={query}')
#         return redirect('/social/explore')