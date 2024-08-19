from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

from django.views import View
from .models import *
from .forms import *
from django.views.generic.edit import UpdateView, DeleteView
# Create your views here.

class PostListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_on')
        form = PostForm()

        context = {
            'post_list': posts,
            'form': form,
        }

        return render(request, 'social/post_list.html', context)


    def post(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_on')
        form = PostForm(request.POST)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()

        context = {
            'post_list': posts,
            #'posts': posts,  # تغيير الاسم إلى 'posts'
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