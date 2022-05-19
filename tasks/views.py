import datetime

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Task
from django.contrib.auth.decorators import login_required
# Create your views here.


def helloworld(request):
    return HttpResponse('Hello world')
@login_required()
def taskview(request,id):
    task = get_object_or_404(Task,pk=id)
    return render(request,'tasks/task.html',{'task':task})
@login_required()
def newtask(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.done = 'doing'
            task.user = request.user # enviando o usuário que está autenticado
            task.save()
            return redirect('/')
    else:
        form = TaskForm()
        return render(request,'tasks/addtask.html',{'form':form})

@login_required()
def tasklist(request):

    search = request.GET.get('search')
    filter = request.GET.get('filter')
    tasksDoneRecently = Task.objects.filter(done='done',update_at__gt=datetime.datetime.now() - datetime.timedelta(days=30),user=request.user).count()
    tasksDone = Task.objects.filter(done='done',user=request.user).count()
    tasksDoing = Task.objects.filter(done='doing',user=request.user).count()

        # add filtro
    if search:
        tasks = Task.objects.filter(title__icontains=search,user=request.user)
    elif filter:
        tasks = Task.objects.filter(done=filter, user=request.user)
    else:
        # listando item no geral
        task_list = Task.objects.all().order_by('-created_at').filter(user=request.user)
        paginator = Paginator(task_list,3)
        page = request.GET.get('page')
        tasks = paginator.get_page(page)
    return render(request,'tasks/list.html',
                  {'tasks':tasks,'tasksdonerecently':tasksDoneRecently,'tasksdone':tasksDone,'tasksdoing':tasksDoing})

def yourname(request,name):
    return render(request,'tasks/yourname.html',{'name':name})
@login_required()
def edittask(request,id):
    task = get_object_or_404(Task,pk=id)
    form = TaskForm(instance=task)

    if(request.method == 'POST'):
        form = TaskForm(request.POST,instance=task)
        if(form.is_valid()):
            task.save()
            return redirect('/')
        else:
            return render(request, 'tasks/edittask.html', {'form': form, 'task': task})
    else:
        return render(request,'tasks/edittask.html',{'form':form,'task':task})


@login_required()
def deletetask(request,id):
    task = get_object_or_404(Task,pk=id)
    task.delete()

    messages.info(request,'Tarefa deletada com sucesso.')

    return redirect('/')


@login_required()
def changestatus(request,id):

    task = get_object_or_404(Task,pk=id)


    if(task.done == 'doing'):
        task.done = 'done'
    else:
        task.done = 'doing'

    task.save()
    return redirect('/')