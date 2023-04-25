from django.views import  generic
from django.contrib.auth.views import LoginView
from .forms import UserRegisterForm, BbForm, AIFormSet
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .forms import ChangeUserInfoForm
from .models import AdvUser, Rubric
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import UpdateView, CreateView, DeleteView
from django.contrib.auth import logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import SearchForm
from .models import SubRubric, Bb


def index(request):
    bbs = Bb.objects.filter(status="confirmed")[:4]
    counter = Bb.objects.filter(status='confirmed').count()
    context = {'bbs': bbs, 'counter': counter}
    return render(request, 'main/index.html', context)


def about(request):
    return render(request, 'main/about.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегестрировались')
            return redirect('/login')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'main/register.html', {"form": form})



class LoginView(LoginView):
    template_name = 'main/login.html'
    success_url = reverse_lazy('main/profile')


class LogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin,
                         UpdateView):
    model = AdvUser
    template_name = 'main/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('main/profile')
    success_message = 'Личные данные пользователя изменены'

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class PasswordChangeView(SuccessMessageMixin, LoginRequiredMixin,
                         PasswordChangeView):
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('main/profile')
    success_message = 'Пароль пользователя изменен'


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy('main/index')

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удален')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


def by_rubric(request, pk):
    rubric = get_object_or_404(SubRubric, pk=pk)
    bbs = Bb.objects.filter(is_active=True, rubric=pk)
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(title__icontains=keyword) | Q(content__icontains=keyword)
        bbs = bbs.filter(q)
    else:
        keyword = ''
    form = SearchForm(initial={'keyword': keyword})
    paginator = Paginator(bbs, 2)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'rubric': rubric, 'page': page, 'bbs': page.object_list, 'form': form}
    return render(request, 'rubric/by_rubric.html', context)


def detail(request, rubric_pk, pk):
    bb = get_object_or_404(Bb, pk=pk)
    ais = bb.additionalimage_set.all()
    context = {'bb': bb, 'ais': ais}
    return render(request, 'rubric/detail.html', context)


@login_required
def profile(request):
    STATUS_CHOISES = [
        ('new', 'новый'),
        ('confirmed', 'Принято в работу'),
        ('canceled', 'Выполнено')
    ]
    status = request.GET.get('status')

    if status:
        bbs = Bb.objects.filter(author=request.user.pk, status=status)
    else:
        bbs = Bb.objects.filter(author=request.user.pk)
    return render(request, 'main/profile.html', context={
        'status': STATUS_CHOISES,
        'bbs': bbs
    })


@login_required
def profile_bb_add(request):
    if request.method == 'POST':
        form = BbForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author_id = request.user.pk
            bb = form.save()
            messages.add_message(request, messages.SUCCESS,
                                    'Заявка создана')
            return redirect('profile')
    else:
        form = BbForm(initial={'author': request.user.pk})
    context = {'form': form}
    return render(request, 'rubric/profile_bb_add.html', context)


@login_required
def profile_bb_change(request, pk):
    bb = get_object_or_404(Bb, pk=pk)
    if not request.user.is_author(bb):
        messages.error(request,
                             'Это не ваша заявка ее трогать нельзя')
        return redirect('profile')
    if request.method == 'POST':
        form = BbForm(request.POST, request.FILES, instance=bb)
        if form.is_valid():
            bb = form.save()
            messages.add_message(request, messages.SUCCESS,
                                     'Заявка изменена')
            return redirect('profile')
    else:
        form = BbForm(instance=bb)

    context = {'form': form}
    return render(request, 'rubric/profile_bb_change.html', context)


@login_required
def profile_bb_delete(request, pk):
    bb = get_object_or_404(Bb, pk=pk)
    if not request.user.is_author(bb):
        messages.error(request,
                             'Чужое!!!!, трогать нельзя')
        return redirect('profile')
    if request.method == 'POST':
        bb.delete()
        messages.add_message(request, messages.SUCCESS,
                             'Заявка удалена')
        return redirect('profile')
    else:
        context = {'bb': bb}
        return render(request, 'rubric/profile_bb_delete.html', context)
