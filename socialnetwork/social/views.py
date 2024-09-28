from django.shortcuts import render, redirect,get_object_or_404
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
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json
from django.views.generic import ListView
from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash,get_user_model
from django.contrib.auth.hashers import check_password


# Create your views here.



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

    
class PostDetailView(LoginRequiredMixin, View):
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
        form = CommentForm(request.POST, request.FILES)  # إضافة request.FILES

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

            new_comment.create_tags()

            # عرض رسالة نجاح
            messages.success(request, "تم إضافة التعليق بنجاح.")
        else:
            # عرض رسالة خطأ مع تفاصيل الأخطاء
            messages.error(request, "حدث خطأ أثناء إضافة التعليق.")
            for error in form.errors.values():
                messages.error(request, error)
        
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
    

class ProfileView(LoginRequiredMixin,View):
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
    

# class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = UserProfile
#     fields = ['name', 'bio', 'birth_date', 'location', 'picture']
#     template_name = 'social/profile_edit.html'

#     def get_success_url(self):
#         pk = self.kwargs['pk']
#         return reverse_lazy('profile', kwargs={'pk': pk})

#     def test_func(self):
#         profile = self.get_object()
#         return self.request.user == profile.user
class ProfileEditView2(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm  # استخدم النموذج المعدل هنا
    # template_name = 'social/profile_edit.html'
    template_name = 'social/pee.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('profile', kwargs={'pk': pk})

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user
    
class ProfileEditView2(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'social/profile_edit.html'

    # التحقق من صحة النموذج وحفظه
    def form_valid(self, form):
        print(self.request.POST)  # طباعة البيانات للتحقق
        return super().form_valid(form)

    # إذا كان النموذج غير صحيح، طباعة الأخطاء
    def form_invalid(self, form):
        print(form.errors)  # طباعة الأخطاء للتحقق
        return super().form_invalid(form)

    # إعادة التوجيه إلى صفحة الملف الشخصي بعد التحديث
    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.pk})

    # التحقق من أن المستخدم هو صاحب الحساب
    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user
    

class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'social/profile_edit.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.object.user  # تمرير المستخدم الحالي إلى النموذج
        return kwargs

    def form_valid(self, form):
        user = form.instance.user
        user.username = form.cleaned_data['username']
        user.email = form.cleaned_data['email']
        user.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.pk})

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user



    def form_invalid(self, form):
        print(form.errors)  # طباعة الأخطاء للتحقق
        return super().form_invalid(form)



    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.pk})



    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user


    
def check_availability(request):
    field_type = request.GET.get('field_type', None)
    value = request.GET.get('value', None)

    if field_type == 'username':
        is_available = not User.objects.filter(username=value).exists()
    elif field_type == 'email':
        is_available = not User.objects.filter(email=value).exists()
    else:
        is_available = False

    return JsonResponse({'is_available': is_available})




    
@login_required
def user_profile_images_view(request):
    # الحصول على جميع الصور القديمة
    images = list(UserProfileImage.objects.filter(user=request.user))

    # الحصول على الصورة الحالية من ملف التعريف
    try:
        current_profile = UserProfile.objects.get(user=request.user)
        if current_profile.picture:
            # إذا كانت الصورة الحالية موجودة بالفعل في القائمة، قم بإزالتها لتجنب التكرار
            images = [image for image in images if image.image != current_profile.picture]
            # ثم أضف الصورة الحالية إلى أول القائمة
            images.insert(0, current_profile.picture)
    except UserProfile.DoesNotExist:
        # التعامل مع حالة عدم وجود ملف تعريف
        current_profile = None

    context = {
        'images': images
    }
    return render(request, 'social/profile_image.html', context)




    
class SetProfileImageView(View):
    def get(self, request, image_id):
        image = get_object_or_404(UserProfileImage, id=image_id, user=request.user)
        profile = UserProfile.objects.get(user=request.user)
        profile.picture = image.image
        profile.save()
        return redirect('profile_image')  # عدل الرابط بناءً على URL إعادة التوجيه


class DeleteImageView(View):
    def get(self, request, image_id):
        image = get_object_or_404(UserProfileImage, id=image_id, user=request.user)
        image.delete()
        return redirect('profile_image')  # عدل الرابط بناءً على URL إعادة التوجيه




@login_required
def select_image(request):
    images = UserProfileImage.objects.filter(user=request.user)
    return render(request, 'social/select_image.html', {'images': images})



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
class UserSearch(LoginRequiredMixin,View):
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
    
    
class ListFollowers(LoginRequiredMixin,View):
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
        form = CommentForm(request.POST, request.FILES)  # تأكد من تضمين الملفات

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.parent = parent_comment
            new_comment.save()

            # إنشاء إشعار
            notification = Notification.objects.create(
                notification_type=2,
                from_user=request.user,
                to_user=parent_comment.author,
                comment=new_comment
            )

             # إضافة رسالة تنبيه
            messages.success(request, "تم إضافة تعليقك بنجاح!")

        else:
            messages.error(request, "فشل في إضافة التعليق. يرجى التحقق من التفاصيل.")

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


class PostNotification(LoginRequiredMixin,View):
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


class FollowNotification(LoginRequiredMixin,View):
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
    
class ThreadNotification(LoginRequiredMixin,View):
    def get(self, request, notification_pk, object_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        thread = ThreadModel.objects.get(pk=object_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('thread', pk=object_pk)


class RemoveNotification(LoginRequiredMixin,View):
    def delete(self, request, notification_pk, *args, **kwargs):
        # الحصول على الإشعار المحدد باستخدام معرف الإشعار (notification_pk)
        notification = Notification.objects.get(pk=notification_pk)

        # تعيين علامة بأن المستخدم قد شاهد الإشعار
        notification.user_has_seen = True
        notification.save()

        # إرسال استجابة تفيد بنجاح العملية
        return HttpResponse('Success', content_type='text/plain')


class ListThreads(LoginRequiredMixin,View):
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

class CreateThread(LoginRequiredMixin,View):
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


# class ThreadView(LoginRequiredMixin,View):
#     # الدالة `get` تُنفذ عند إرسال طلب GET إلى هذا العرض.
#     def get(self, request, pk, *args, **kwargs):
#         # نقوم بإنشاء نموذج فارغ للرسالة ليتم عرضه في صفحة المحادثة.
#         form = MessageForm()

#         # نجلب المحادثة (thread) من قاعدة البيانات باستخدام معرف المحادثة (pk).
#         thread = ThreadModel.objects.get(pk=pk)

        

#         # نقوم بجلب قائمة الرسائل التي تنتمي إلى هذه المحادثة من قاعدة البيانات.
#         # نستخدم `filter` لجلب جميع الرسائل التي تحتوي على معرف المحادثة.
#         message_list = MessageModel.objects.filter(thread__pk__contains=pk)

#         # نقوم بتجهيز البيانات (context) التي سيتم تمريرها إلى القالب لعرضها.
#         context = {
#             'thread': thread,               # المحادثة الحالية.
#             'form': form,                   # نموذج الرسالة الفارغ.
#             'message_list': message_list    # قائمة الرسائل في المحادثة.
#         }

#         # نقوم بعرض صفحة المحادثة (`thread.html`) مع تمرير البيانات اللازمة إليها.
#         return render(request, 'social/thread.html', context)
        


class ThreadView(LoginRequiredMixin, View):
    # الدالة `get` تُنفذ عند إرسال طلب GET إلى هذا العرض.
    def get(self, request, pk, *args, **kwargs):
        # نقوم بإنشاء نموذج فارغ للرسالة ليتم عرضه في صفحة المحادثة.
        form = MessageForm()

        # نجلب المحادثة (thread) من قاعدة البيانات باستخدام معرف المحادثة (pk).
        thread = get_object_or_404(ThreadModel, pk=pk)

        # تحديث حالة قراءة الرسائل التي استلمها المستخدم الحالي.
        MessageModel.objects.filter(receiver_user=request.user, thread=thread).update(is_read=True)

        # نجلب قائمة الرسائل التي تنتمي إلى هذه المحادثة من قاعدة البيانات.
        message_list = MessageModel.objects.filter(thread=thread)

        # نقوم بتجهيز البيانات (context) التي سيتم تمريرها إلى القالب لعرضها.
        context = {
            'thread': thread,               # المحادثة الحالية.
            'form': form,                   # نموذج الرسالة الفارغ.
            'message_list': message_list    # قائمة الرسائل في المحادثة.
        }

        # نقوم بعرض صفحة المحادثة (`thread.html`) مع تمرير البيانات اللازمة إليها.
        return render(request, 'social/thread.html', context)



class UpdateReadStatusView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # اجلب المحادثة
        thread = get_object_or_404(ThreadModel, pk=pk)
        # تحديث حالة قراءة الرسائل
        MessageModel.objects.filter(receiver_user=request.user, thread=thread, is_read=False).update(is_read=True)
        return JsonResponse({'status': 'success'})
    

class CreateMessage(LoginRequiredMixin,View):
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



class Explore(View):
    def get(self, request, *args, **kwargs):
        explore_form = ExploreForm()
        query = self.request.GET.get('query')

        if query:  # تحقق من أن query ليست None أو فارغة
            tag = Tag.objects.filter(name__icontains=query).first()
            if tag:
                posts = Post.objects.filter(tags__in=[tag])
            else:
                posts = Post.objects.all()
        else:
            posts = Post.objects.all()

        context = {
            'tag': tag if query else None,  # تعيين tag فقط إذا كانت قيمة query موجودة
            'posts': posts,
            'explore_form': explore_form,
            'no_results': not posts.exists() and not query,  # إضافة متغير لتحديد عدم وجود نتائج
        }

        return render(request, 'social/explore.html', context)

    
    def post(self, request, *args, **kwargs):
     explore_form = ExploreForm(request.POST)
     if explore_form.is_valid():
        query = explore_form.cleaned_data['query']
        if query:  # تحقق من أن query ليست فارغة
            tag = Tag.objects.filter(name__icontains=query).first()

            if tag:
                posts = Post.objects.filter(tags__in=[tag])
                
                # إذا لم يكن هناك أي منشورات مرتبطة بالوسم
                if not posts.exists():
                    messages.error(request, 'No posts found for this tag.')
                    return redirect('explore')  # إعادة التوجيه إلى صفحة البحث
            else:
                # إذا لم يتم العثور على الوسم
                messages.error(request, 'Tag not found.')
                return redirect('explore')  # إعادة التوجيه إلى صفحة البحث
             
            # إذا تم العثور على الوسم والمنشورات، نقوم بإعادة التوجيه مع الاستعلام
            return redirect(f'/social/explore?query={query}')
        else:
            messages.error(request, 'Invalid search query.')
            return redirect('/social/explore')
    
    # إذا كان النموذج غير صالح
     messages.error(request, 'Invalid search query.')
     return redirect('/social/explore')
    
User = get_user_model()

def get_suggestions(user, limit=6):
    followings = user.profile.followers.all()  # المتابعون الحاليون للمستخدم
    suggestions = User.objects.exclude(pk__in=followings).exclude(pk=user.pk).order_by("?")[:limit]  # استبعاد المستخدمين المتابعين الحاليين
    return suggestions

def suggestions_view(request):
    suggestions = get_suggestions(request.user)  # استدعاء الدالة لجلب اقتراحات المستخدمين
    return render(request, 'social/suggestions.html', {'suggestions': suggestions})  # إرسال الاقتراحات إلى القالب



#يعني الكلاس الذي يحتوي post get يكون cbsv

# واستخدم معه LoginRequiredMixin
#fbsv لا يحتوي get post واستخدم معه @loginrequird