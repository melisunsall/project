from django.shortcuts import render
from django.utils import timezone
from django.contrib import messages
# Create your views here.
from django.views import generic
from datetime import datetime
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Intern, Advisor, Department
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.generic import View
from .forms import UserForm, SearchForm, EventForm, CommentForm, FileForm
from django.contrib.auth.models import Permission, User
from django.utils.safestring import mark_safe
from .models import *
from .utils import Calendar
import calendar
from django.core.files.storage import FileSystemStorage


class DetailView(generic.DetailView):
    model = Department
    template_name = 'forum/detail.html'


def AboutView(request):
    return render(request, 'forum/about.html', {})





class InternView(generic.DetailView):
    model = Intern
    template_name = 'forum/intern.html'

    # def get_context_data(self, **kwargs):
    # context = super(InternView, self).get_context_data(**kwargs)
    # context['comments'] = Comment.objects.filter(intern=self.object)


class DepartmentView(generic.ListView):
    model = Department
    template_name = 'forum/department.html'
    context_object_name = 'department_list'

    def get_queryset(self):
        return Department.objects.all()


# @method_decorator(login_required(login_url='forum:login'), name='dispatch')
class InternsView(LoginRequiredMixin, generic.ListView):
    login_url = 'forum:login'
    template_name = 'forum/interns.html'
    context_object_name = 'intern_list'

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            intern_list = Intern.objects.filter(name__icontains=query)
        else:
            intern_list = Intern.objects.order_by('-votes')

        return intern_list


@method_decorator(login_required(login_url='forum:login'), name='dispatch')
class InternCreate(CreateView):
    model = Intern
    fields = ['department', 'name', 'advisor', 'profile_photo', 'resume', 'technical_skills', 'team_work', 'experience']


class InternUptade(UpdateView):
    model = Intern
    fields = ['department', 'name', 'advisor', 'profile_photo', 'resume']


class InternDelete(DeleteView):
    model = Intern
    success_url = reverse_lazy('forum:interns')


class UserFormView(View):
    form_class = UserForm
    template_name = 'forum/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)
            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('forum:departments')

        return render(request, self.template_name, {'form': form})


def loginview(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if user .is_superuser:
                    return redirect('forum:interns')
                else:
                    return redirect('forum:about')
            else:
                return render(request, 'forum/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'forum/login.html', {'error_message': 'Invalid login'})
    return render(request, 'forum/login.html')


def logoutview(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'forum/login.html', context)


def vote(request, pk):
    intern = Intern.objects.get(pk=pk)
    intern.votes += 1
    intern.save()
    return redirect('forum:interns')


def accept(request, pk):
    intern = Intern.objects.get(pk=pk)
    intern.is_accepted = 1
    intern.save()
    return redirect('forum:interns')


@login_required
def profile(request):
    return render(request, 'forum/profile.html')


@login_required
def search_view(request):
    interns = Intern.objects.all()
    form = SearchForm(request.GET)

    if form.is_valid():
        if form.cleaned_data["q"]:
            interns = interns.filter(name_startswith=form.cleaned_data["q"])
        elif form.cleaned_data["name"]:
            interns = interns.filter(name_startswith=form.cleaned_data["name"])

    return render(request, "forum/search.html", {"form": form, "intern_list": interns})


class CalendarView(generic.ListView):
    model = Appointment
    template_name = 'forum/calendar.html'

    def get_queryset(self):
        return Appointment.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(d.year, d.month, withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return datetime.date(year, month, day=1)
    return datetime.date.today()


def prev_month(d):
    first = d.replace(day=1)
    prev = first - timedelta(days=1)
    month = 'month=' + str(prev.year) + '-' + str(prev.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next = last + timedelta(days=1)
    month = 'month=' + str(next.year) + '-' + str(next.month)
    return month


class EventFormView(View):
    form_class = EventForm
    template_name = 'forum/event_form.html'

    def get(self, request, event_id=None):
        instance = Appointment()
        user = self.request.user
        form = self.form_class(user, None, instance=instance)
        return render(request, self.template_name, {'form': form})

    def post(self, request, event_id=None):
        instance = Appointment()
        user = self.request.user
        form = self.form_class(user, request.POST, instance=instance)
        if form.is_valid():
            form.save()
        else:
            return render(request, self.template_name, {'form': form})

        return HttpResponseRedirect(reverse('forum:calendar'))


class FileFormView(View):

    def get(self, request):
        return render(request, 'intern.html', {})

    def post(self, request, pk):
        uploaded_file = request.FILES['document']
        """fs = FileSystemStorage()
        name=fs.save(uploaded_file.name,uploaded_file)
        url = fs.url(name)"""
        File.objects.create(
            intern_id=pk,
            file=uploaded_file
        )
        return redirect('forum:intern', pk=pk)


class AddComent(View):

    def get(self, request, pk):
        return redirect('forum:intern', pk=pk)

    def post(self, request, pk):
        text = request.POST['textcomment']
        this = Intern.objects.get(pk=pk)
        Comment.objects.create(intern_id=pk, text=text, user_id=request.user.id)

        return redirect('forum:intern', pk=pk)


class DeleteComment(View):
    def get(self, comment_id):
        comment = Comment.objects.get(pk=comment_id)
        return redirect('forum:intern', pk=comment.intern.pk)

    def post(self, request, comment_id):
        print(comment_id)
        comment = Comment.objects.get(pk=comment_id)
        comment.delete()
        return redirect('forum:intern', pk=comment.intern.pk)


class VoteComment(View):
    def get(self, request, comment_id):
        comment = Comment.objects.get(pk=comment_id)
        comment.like += 1
        comment.save()
        return redirect('forum:intern', pk=comment.intern.pk)

    def post(self, request, comment_id):
        comment = Comment.objects.get(pk=comment_id)
        comment.like += 1
        comment.save()
        return redirect('forum:intern', pk=comment.intern.pk)


class SearchView(generic.ListView):
    template_name = 'forum/interns.html'
    model = Intern

    def get_queryset(self):
        try:
            name = self.kwargs['name']
        except:
            name = ''
        if (name != ''):
            object_list = self.model.objects.filter(name__icontains=name)
        else:
            object_list = self.model.objects.all()
        return object_list
