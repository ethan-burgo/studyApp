from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from . models import User, Schedule, Goals, Schedule_Items, WeekDay
from . forms import usersName, goals, get_goals, create_schedule, schedule_details
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User

#asks for users name
def home(request):
    current_user = request.user
    recentG = Goals.objects.all()
    recentS = Schedule_Items.objects.all()
    query = Schedule.objects.filter(favorite=True)
    list = []
    for x in query:
        object = Schedule_Items.objects.filter(title = x)
        list.append(object)

    print(list)
    current_user = request.user
    args = {
        'recentG': recentG,
        'current_user': current_user,
        'recentS': recentS,
        }
    return render(request, 'home.html', args)

#schedule page
def schedulePage(request):

    current_user = request.user
    data = Schedule.objects.all()
    queryS = request.GET.get('s')
    gotS = True
    if current_user.is_authenticated:
        usered = Schedule.objects.filter(user = current_user).all()
    else:
        usered = None

    if queryS == None:
        gotS = False

    if gotS == True:
        request.session['queryS'] = queryS
        return redirect('/cool')

    if request.method == "POST":
        create_scheduleForm = create_schedule(request.POST)
        if create_scheduleForm.is_valid():
            saved = create_scheduleForm.save(commit=False)
            saved.user = current_user
            saved.save()
            q = create_scheduleForm.cleaned_data['title']
            query = Schedule.objects.get(title = q).title
            request.session['query'] = query
            return redirect('/schedule_adding')

    else:
        create_scheduleForm = create_schedule()

    args = {
        'create_scheduleForm': create_scheduleForm,
        'list': list,
        'data': data,
        'current_user': current_user,
        'queryS': queryS,
        'usered': usered
    }

    return render(request, 'schedule.html', args)

#adding schedule items to a schedule
def schedule_adding(request):
    current_user = request.user
    title = request.session['query']
    got = Schedule.objects.get(title = title)
    data = Schedule_Items.objects.all().order_by('day_name', 'start_time')
    days = WeekDay.objects.all().order_by('day_order')
    done = request.GET.get('done')
    if done:
        return redirect('/schedulePage')
        print("ok")
    if request.method == "POST":
        schedule_detailsForm = schedule_details(request.POST)
        if schedule_detailsForm.is_valid():
            #start = schedule_detailsForm.cleaned_data['start_time']
            #end = schedule_detailsForm.cleaned_data['end_time']
            base = schedule_detailsForm.save(commit=False)
            base.title = got
            base.save()
    else:
        schedule_detailsForm = schedule_details()

    args = {
        'schedule_detailsForm': schedule_detailsForm,
        'data': data,
        'got': got,
        'current_user': current_user,
        'days': days
    }
    return render(request, 'schedule_adding.html', args)

#edit delete schedules from the data base
def configSchedules_view(request):
    get_form = get_goals(request.GET)
    current_user = request.user
    queryS = request.session['queryS']
    got = Schedule.objects.get(title = queryS)
    data = Schedule_Items.objects.all().order_by('day_name', 'start_time')
    days = WeekDay.objects.all().order_by('day_order')
    dataAll = Schedule.objects.all()
    gots = request.GET.get('s')

    if gots:
        queryS = gots
        request.session['queryS'] = queryS
        got = Schedule.objects.get(title = queryS)

        print(got)

    args = {
        'current_user': current_user,
        'queryS': queryS,
        'got': got,
        'data': data,
        'days': days,
        'dataAll': dataAll,
        'gots': gots,

    }
    return render(request, 'configSchedules.html', args)

#sign in page with form to add new users
def signInPage(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('/user details')

    else:
        form = UserCreationForm()

    return render(request, 'signIn.html', {'form': form})

#login page
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():

            user = form.get_user()
            login(request, user)
            return redirect('/')

    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

#logout view
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('/')

#extra user details views
def userDetails_view(request):
    if request.method == "POST":
        form = usersName(request.POST, instance=request.user)
        current_user = request.user
        if form.is_valid():
            form.save()

            return redirect('/')

    else:
        form = usersName()

    return render(request, 'userDetails.html', {'form': form})

#goal setting view
def setGoals_view(request):
    current_user = request.user
    data = Goals.objects.all()
    input_form = goals()
    get_form = get_goals(request.GET)
    query = request.GET.get('y')
    got = True
    if current_user.is_authenticated:
        usered = Goals.objects.filter(user = current_user).all()
    else:
        usered = None

    if query == None:
        got = False

    if got == True:
        request.session['query'] = query
        return redirect('/your goals')

    args = {
        'input_form': input_form,
        'data': data,
        'current_user': current_user,
        'query': query,
        'got': got,
        'usered': usered
    }

    if request.method == "POST":
        if current_user.is_authenticated:
            input_form = goals(request.POST)
            args = {'input_form': input_form}

            if input_form.is_valid():
                base = input_form.save(commit=False)
                base.user = current_user
                base.save()

        else:
            input_form = goals(request.POST)
            args = {'input_form': input_form}

    else:
        input_form = goals()
        get_form = get_goals(request.GET)


    return render(request, 'goals.html', args)

#edit and deleteing goals from the database
def configGoals_view(request):
    current_user = request.user
    data = Goals.objects.all()
    form = goals()
    get_form = get_goals(request.GET)
    query = request.session['query']
    edit = request.GET.get('q')
    goty1 = request.GET.get('y1')
    deleteB = request.GET.get('B')

    if goty1:
        query = goty1
        request.session['query'] = query

    user = Goals.objects.all().filter(user=current_user)
    id = Goals.objects.get(title=query, user=current_user).id
    instance = get_object_or_404(Goals, id=id)

    if deleteB == 'B':
        query = request.session['query']
        delete = Goals.objects.get(title=query)
        delete.delete()
        return redirect('/set goals')

    if request.method == "POST":
        form = goals(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

    if request.method == "GET":
        get_form = get_goals(request.GET)
        form = goals(instance=instance)

    args = {
        'data': data,
        'current_user': current_user,
        'query': query,
        'form': form,
        'goty1': goty1,
        'instance': instance
    }

    return render(request, 'configGoals.html', args)
