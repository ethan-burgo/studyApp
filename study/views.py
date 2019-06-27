from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from . models import User, Schedule, Goals, Schedule_Items, WeekDay
from . forms import usersName, goals, get_goals, create_schedule, schedule_details, carry_goals, edit_goals
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User

#asks for users name
def home(request):
    current_user = request.user
    data = Schedule_Items.objects.all().order_by('day_name', 'start_time')
    current_user = request.user
    recentG = Goals.objects.all()
    recentS = Schedule_Items.objects.all()
    list = []
    if current_user.is_authenticated:
        query = Schedule.objects.all().filter(favorite=True, user = current_user)
        for x in query:
            got = x
            args={ 'got':got }
            list.append(got)
        got = list

        args = {'got': got}
    else:
        got = list
    days = WeekDay.objects.all().order_by('day_order')

#arguments passed to the html files
    args = {
        'recentG': recentG,
        'current_user': current_user,
        'recentS': recentS,
        'days': days,
        'got': got,
        'data': data
        }
    return render(request, 'home.html', args)

#schedule page
def schedulePage(request):
    current_user = request.user
    data = Schedule.objects.all()
    queryS = request.GET.get('s')
    gotS = True
    same = False
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
            q = create_scheduleForm.cleaned_data['title']
            if Schedule.objects.all().filter(user = current_user, title = q):
                same = True
                request.session['same'] = same
            else:
                saved.save()
                query = Schedule.objects.get(title = q, user = current_user).title
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
        'usered': usered,
        'same': same
    }

    return render(request, 'schedule.html', args)

#adding schedule items to a schedule
def schedule_adding(request):
    current_user = request.user
    title = request.session['query']
    got = Schedule.objects.get(title = title, user = current_user)
    data = Schedule_Items.objects.all().order_by('day_name', 'start_time')
    days = WeekDay.objects.all().order_by('day_order')
    done = request.GET.get('done')
    editChoice = request.GET.get("editChoice")
    request.session['queryS'] = editChoice
    if editChoice:
        print(request.session['queryS'])
        return redirect('/Edit_Schedules')

    if done:
        return redirect('/schedulePage')
        print("ok")
    if request.method == "POST":
        schedule_detailsForm = schedule_details(request.POST)
        if schedule_detailsForm.is_valid():
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
    #query data base and getting data from html file
    get_form = get_goals(request.GET)
    current_user = request.user
    queryS = request.session['queryS']
    got = Schedule.objects.get(title = queryS, user = current_user)
    data = Schedule_Items.objects.all().order_by('day_name', 'start_time')#!
    days = WeekDay.objects.all().order_by('day_order')
    dataAll = Schedule.objects.all()
    gots = request.GET.get('s')
    deleteB = request.GET.get('B')
    print(queryS)

    if gots:
        queryS = gots
        request.session['queryS'] = queryS
        got = Schedule.objects.get(title = queryS, user = current_user)

    if deleteB == 'B':
        delete = got
        delete.delete()
        return redirect('/schedules')

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

#editing schedules: add, delete, edit
def EditSchedules_view(request):
#variables needed and established before anything can happen
    current_user = request.user
    queryS = request.session['queryS']
    print(queryS)
    got = Schedule.objects.get(title = queryS, user = current_user)
    data = Schedule_Items.objects.all().order_by('day_name', 'start_time')#!
    days = WeekDay.objects.all().order_by('day_order')
    dataAll = Schedule.objects.all()
    form = schedule_details()
    formf = create_schedule()
    schedule_detailsForm = schedule_details()
    editChoice = request.GET.get("editChoice")
    deleteB = request.GET.get('B')
    add = request.GET.get('q')

#editing the title/fav function
    if request.method == "POST":
        formf = create_schedule(request.POST, instance = got)
        if formf.is_valid():
            formf.save()
            request.session['queryS'] = formf.cleaned_data['title']

    if request.method == "GET":
        formf = create_schedule(instance = got)

#the use of buttons to help with displaying things and variables
    if deleteB and editChoice:
        instance = Schedule_Items.objects.get(id = int(editChoice))
    if add:
        editChoice == None

#edit function for particular schedule Activities
    if editChoice:
        instance = Schedule_Items.objects.get(id = int(editChoice))
        request.session['queryC'] = editChoice
        if request.method == "POST" and add == None:
            form = schedule_details(request.POST, instance=instance)

            if form.is_valid():
                save = form.save(commit=False)
                save.save()
                return redirect('/Edit_Schedules')

        else:
            form = schedule_details(instance = instance)

#delete function for particular schedule Activities
    if deleteB:
        queryC = request.session['queryC']
        delete = Schedule_Items.objects.get(id = queryC)
        delete.delete()
        return redirect('/Edit_Schedules')

#adding function to add more activities to the schedule
    if editChoice == None:
        args = {'schedule_detailsForm': schedule_detailsForm}
        if request.method == "POST":
            schedule_detailsForm = schedule_details(request.POST)
            if schedule_detailsForm.is_valid():
                save = schedule_detailsForm.save(commit=False)
                save.title = got
                save.save()
                return redirect('/Edit_Schedules')

        else:
            schedule_detailsForm = schedule_details()

#arguments passed to html file that enable certain things to be displayed
    args = {
        'current_user': current_user,
        'queryS': queryS,
        'got': got,
        'data': data,
        'days': days,
        'dataAll': dataAll,
        'form': form,
        'editChoice': editChoice,
        'schedule_detailsForm': schedule_detailsForm,
        'add': add,
        'formf': formf
    }

    return render(request, 'EditSchedules.html', args)

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
    same = False
    if current_user.is_authenticated:
        usered = Goals.objects.filter(user = current_user).all()
    else:
        usered = None

    if query == None:
        got = False

    if got == True:
        request.session['query'] = query
        return redirect('/your goals')

    if request.method == "POST":
        if current_user.is_authenticated:
            input_form = goals(request.POST)
            args = {'input_form': input_form}
            if input_form.is_valid():
                base = input_form.save(commit=False)
                base.user = current_user

                carry = input_form.cleaned_data['title']
                if Goals.objects.all().filter(user = current_user, title = carry):
                    same = True
                    request.session['same'] = same
                else:
                    base.save()
                    request.session['carryQuery'] = carry
                    return redirect('/carry_goals')

        else:
            input_form = goals(request.POST)
            args = {'input_form': input_form}

    else:
        input_form = goals()
        get_form = get_goals(request.GET)

    print(same)
    args = {
        'input_form': input_form,
        'data': data,
        'current_user': current_user,
        'query': query,
        'got': got,
        'usered': usered,
        'same': same
    }

    return render(request, 'goals.html', args)

#edit and deleteing goals from the database
def configGoals_view(request):
    current_user = request.user
    data = Goals.objects.all()
    form = edit_goals()
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
        delete = Goals.objects.get(title=query, user = current_user)
        delete.delete()
        return redirect('/set goals')

    if request.method == "POST":
        form = edit_goals(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

    if request.method == "GET":
        get_form = get_goals(request.GET)
        form = edit_goals(instance=instance)

    args = {
        'data': data,
        'current_user': current_user,
        'query': query,
        'form': form,
        'goty1': goty1,
        'instance': instance
    }

    return render(request, 'configGoals.html', args)

#adding time fields to your goals
def carryGoals_view(request):
    carryQuery = request.session['carryQuery']
    carryQuery = str(carryQuery)
    data = Goals.objects.all()
    current_user = request.user
    form = carry_goals()
    instance = Goals.objects.get(title = carryQuery, user = current_user)

    if request.method == "POST":
        form = carry_goals(request.POST, instance=instance)
        if form.is_valid():
            form.save()
    else:
        form = carry_goals()

    args = {
        'form': form,
        'carryQuery': carryQuery,
        'data': data,
        'current_user': current_user
    }
    return render(request, 'carryGoals.html', args)
