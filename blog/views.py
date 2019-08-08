from django.shortcuts import render, redirect, get_object_or_404
from .models import Portfolio, Comment
from .forms import NewBlog, CommentForm # 모듈 추가
from django.db.models import Avg
from django.contrib.auth.decorators import login_required # 로그인 한 사용자만 글에 접근


# Create your views here.
# index, create, update, delete 참고 : 멋사 강의자료
def index(request):
    blogs = Portfolio.objects.all()
    
    return render(request, 'index.html', {'blogs' : blogs})

def map(request):
    return render(request, 'map.html')

@login_required
def create(request):
    if request.method == 'POST' : 
        form = NewBlog(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit = False) 
            post.save()
            return redirect('index')

    elif request.method == 'GET' :
        form = NewBlog()
        return render(request, 'create.html', {'form' : form})

@login_required
def update(request, blog_id):
    blog = get_object_or_404(Portfolio, pk = blog_id ) # 수정할 블로그 객체 가져오기
    form = NewBlog(request.POST, instance = blog) # 가져온 블로그 객체에 맞는 입력공간을 마련하기 : create 이용
    if form.is_valid():
        form.save()
        return redirect('index')
    return render(request, 'create.html', {'form' : form})

# 첫화면에서 삭제 버튼
@login_required
def delete(request, blog_id):
    blog = get_object_or_404(Portfolio, pk = blog_id ) 
    blog.delete()
    return redirect('index')

def detail(request, blog_id):
    blog_detail = get_object_or_404(Portfolio, pk=blog_id)

    #평균평점 구하는 부분(참고 : 템플릿상에서 {{average}}값이 평균평점값)
    a = Comment.objects.filter(post=blog_id).aggregate(Avg('평점'))
    b = a['평점__avg']
    if b is None:
        average = 0
    else:
        average = round(b,1) 

    return render(request, 'detail.html', {'blog': blog_detail,"average":average})

@login_required
def comment(request,post_id):

    pos = get_object_or_404(Portfolio, pk = post_id)
    if request.method =="POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = pos #어디에 달건지 저장
            comment.작성자 = request.user.get_username()
            comment.save()
            return redirect('index')
    
    else:
        form = CommentForm()
        return render(request, 'comment.html', {'form':form})

@login_required
def co_update(request, post_id):
    pos = get_object_or_404(Comment, pk = post_id)
    if request.method =="POST":
        form = CommentForm(request.POST, instance=pos)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.save()
            return redirect('index')
    
    else:
        form = CommentForm()
        return render(request, 'create.html', {'form':form})
@login_required
def co_delete(request,post_id):
    comment = get_object_or_404(Comment, pk = post_id)
    comment.delete()
    return redirect('index')