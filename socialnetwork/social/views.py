from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.db.models import Q

from django.views import View
from .models import *
from .forms import *
from django.views.generic.edit import UpdateView, DeleteView
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

class PostListView(LoginRequiredMixin, View):
    # يُشترط أن يكون المستخدم مسجلاً للدخول للوصول إلى هذا العرض
    def get(self, request, *args, **kwargs):
        # الحصول على المستخدم الذي قام بتسجيل الدخول
        logged_in_user = request.user
        
        # الحصول على جميع المنشورات التي كتبها المستخدمون الذين يتابعهم المستخدم الحالي
        # يتم استخدام `author__profile__followers__in=[logged_in_user.id]` للبحث عن المنشورات التي كتبها
        # مستخدمون يتبعهم المستخدم الحالي
        posts = Post.objects.filter(
            author__profile__followers__in=[logged_in_user.id]
        ).order_by('-created_on')  # ترتيب المنشورات من الأحدث إلى الأقدم
        
        # إنشاء نموذج جديد للمنشورات
        form = PostForm()

        # إعداد السياق الذي سيتم تمريره إلى القالب
        context = {
            'post_list': posts,  # قائمة المنشورات التي سيتم عرضها
            'form': form,        # نموذج لإضافة منشورات جديدة
        }

        # عرض قالب `post_list.html` مع السياق الذي يحتوي على المنشورات والنموذج
        return render(request, 'social/post_list.html', context)

    def post(self, request, *args, **kwargs):
        # الحصول على جميع المنشورات وترتيبها من الأحدث إلى الأقدم
        posts = Post.objects.all().order_by('-created_on')
        
        # إنشاء نموذج للمنشورات باستخدام البيانات المرسلة عبر POST
        form = PostForm(request.POST)

        # التحقق من صحة النموذج
        if form.is_valid():
            # حفظ المنشور الجديد بدون تقديمه مباشرة
            new_post = form.save(commit=False)
            # تعيين مؤلف المنشور إلى المستخدم الذي قام بتسجيل الدخول
            new_post.author = request.user
            # حفظ المنشور الجديد في قاعدة البيانات
            new_post.save()

        # إعداد السياق الذي سيتم تمريره إلى القالب
        context = {
            'post_list': posts,  # قائمة المنشورات التي سيتم عرضها
            'form': form,        # نموذج لإضافة منشورات جديدة
        }

        # عرض قالب `post_list.html` مع السياق الذي يحتوي على المنشورات والنموذج
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
        
        comments = Comment.objects.filter(post=post).order_by('-created_on')

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
