from django.shortcuts import render
from .models import Blogpost
# Create your views here.
from django.http import HttpResponse

def index(request):
    myposts= Blogpost.objects.all()
    print(myposts)
    return render(request, 'blog/index.html', {'myposts': myposts})

def blogpost(request, id):
    post = Blogpost.objects.filter(post_id = id)
    print(post)                          # will print the queryset of particular id given in above
                                         # line in post_id
    return render(request, 'blog/blogpost.html',{'post':post[0]})  # [0] to get first element from queryset
