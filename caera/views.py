from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.generic import UpdateView

from caera.forms import ProposalForm, TagForm, ProfileCreationForm, ProposalSearchForm, ProjectForm, CommentForm, \
    ProfileUpdateForm
from caera.models import Proposal, User, Tag, Project, Comment, Like, PaidReaction, Donation


@login_required
def profile_view(request):
    return render(request, "accounts/profile.html")


class ProfileCreateView(generic.CreateView):
    model = User
    # fields = "__all__"
    form_class = ProfileCreationForm
    template_name = "accounts/profile_form.html"
    success_url = reverse_lazy('caera:profile')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    # fields = ['username', 'first_name', 'last_name', 'email']
    template_name = 'accounts/profile_update.html'
    # template_name = "accounts/profile_form.html"
    success_url = reverse_lazy('caera:profile')

    def get_object(self, queryset=None):
        return self.request.user


class ProposalListView(generic.ListView):
    model = Proposal

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProposalListView, self).get_context_data(**kwargs)

        title = self.request.GET.get("title", "")
        tag = self.request.GET.get("tags")
        city = self.request.GET.get("city")

        context["search_form"] = ProposalSearchForm(initial={
            "title": title,
            "tags": tag,
            "city": city,
        })

        return context

    def get_queryset(self):
        queryset = Proposal.objects.select_related('author', 'city').prefetch_related('tags').annotate(
            like_count=Count('likes', filter=Q(likes__value='like'))
        ).order_by('-like_count')
        form = ProposalSearchForm(self.request.GET)

        if form.is_valid():
            title = form.cleaned_data["title"]
            tag = form.cleaned_data["tags"]
            city = form.cleaned_data["city"]

            if title:
                queryset = queryset.filter(title__icontains=title.strip())
            if tag:
                queryset = queryset.filter(tags=tag)
            if city:
                queryset = queryset.filter(city=city)

            return queryset
        return queryset


class ProposalDetailView(generic.DetailView):
    model = Proposal

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proposal = self.get_object()

        if self.request.user.is_authenticated:
            context["user_like"] = proposal.get_user_like(self.request.user)
            context["user_paid_reaction"] = proposal.paid_reactions.filter(user=self.request.user).exists()
        else:
            context["user_like"] = None
            context["user_paid_reaction"] = None

        return context


class ProposalCreateView(LoginRequiredMixin, generic.CreateView):
    model = Proposal
    form_class = ProposalForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ProposalUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Proposal
    form_class = ProposalForm


class ProposalDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Proposal
    success_url = reverse_lazy("caera:proposal-list")


class ProjectListView(generic.ListView):
    model = Project

    def get_queryset(self):
        proposal_id = self.kwargs['pk']
        return Project.objects.filter(proposal__id=proposal_id).annotate(
            like_count=Count('likes', filter=Q(likes__value='like'))
        ).order_by('-like_count')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['proposal'] = get_object_or_404(Proposal, pk=self.kwargs['pk'])
        return context


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    form_class = ProjectForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.proposal = get_object_or_404(Proposal, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['proposal'] = get_object_or_404(Proposal, pk=self.kwargs['pk'])
        return context


class ProjectDetailView(generic.DetailView):
    model = Project

    def get_object(self, queryset=None):
        return get_object_or_404(Project, pk=self.kwargs['project_pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        context['proposal'] = get_object_or_404(Proposal, pk=self.kwargs['pk'])

        if self.request.user.is_authenticated:
            context["user_like"] = project.get_user_like(self.request.user)
            context["user_paid_reaction"] = project.paid_reactions.filter(user=self.request.user).exists()
        else:
            context["user_like"] = None
            context["user_paid_reaction"] = None

        return context


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    form_class = ProjectForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['proposal'] = get_object_or_404(Proposal, pk=self.kwargs['pk'])
        return context


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Project

    def get_success_url(self):
        return reverse_lazy("caera:proposal-detail", kwargs={"pk": self.object.proposal.pk})


class TagCreateView(LoginRequiredMixin, generic.CreateView):
    model = Tag
    form_class = TagForm
    success_url = reverse_lazy("caera:proposal-create")


class ProposalCommentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        proposal = get_object_or_404(Proposal, pk=self.kwargs["pk"])
        form.instance.user = self.request.user
        form.instance.content_object = proposal
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.content_object.get_absolute_url()


class ProposalCommentUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = "comment_pk"

    def get_success_url(self):
        return self.object.content_object.get_absolute_url()


class ProposalCommentDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Comment
    pk_url_kwarg = "comment_pk"

    def get_success_url(self):
        return self.object.content_object.get_absolute_url()


class ProjectCommentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs["project_pk"])
        form.instance.user = self.request.user
        form.instance.content_object = project
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.content_object.get_absolute_url()


class ProjectCommentUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = "comment_pk"

    def get_success_url(self):
        return self.object.content_object.get_absolute_url()


class ProjectCommentDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Comment
    pk_url_kwarg = "comment_pk"

    def get_success_url(self):
        return self.object.content_object.get_absolute_url()


class ProposalLikeToggleView(LoginRequiredMixin, View):
    def post(self, request, pk):
        proposal = get_object_or_404(Proposal, pk=pk)
        value = request.POST.get("value")
        content_type = ContentType.objects.get_for_model(Proposal)

        like, created = Like.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=proposal.id,
        )

        if like.value == value:
            like.delete()
        else:
            like.value = value
            like.save()

        return redirect(proposal.get_absolute_url())


class ProjectLikeToggleView(LoginRequiredMixin, View):
    def post(self, request, pk, project_pk):
        project = get_object_or_404(Project, pk=project_pk, proposal_id=pk)
        value = request.POST.get("value")  # "like" або "dislike"
        content_type = ContentType.objects.get_for_model(Project)

        like, created = Like.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=project.id,
        )

        if like.value == value:
            like.delete()  # toggle off
        else:
            like.value = value
            like.save()

        return redirect(project.get_absolute_url())


class ProposalPaidReactionToggleView(LoginRequiredMixin, View):
    def post(self, request, pk):
        proposal = get_object_or_404(Proposal, pk=pk)
        content_type = ContentType.objects.get_for_model(Proposal)

        paid_reaction, created = PaidReaction.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=proposal.id,
        )

        if not created:
            paid_reaction.delete()  # toggle off

        return redirect(proposal.get_absolute_url())


class ProjectPaidReactionToggleView(LoginRequiredMixin, View):
    def post(self, request, pk, project_pk):
        project = get_object_or_404(Project, pk=project_pk, proposal_id=pk)
        content_type = ContentType.objects.get_for_model(Project)

        paid_reaction, created = PaidReaction.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=project.id,
        )

        if not created:
            paid_reaction.delete()  # toggle off

        return redirect(project.get_absolute_url())


class ProjectDonateView(LoginRequiredMixin, View):
    def post(self, request, pk, project_pk):
        proposal = get_object_or_404(Proposal, pk=pk)
        project = get_object_or_404(Project, pk=project_pk)
        amount = request.POST.get("amount")

        try:
            amount = float(amount)
            if amount > 0:
                Donation.objects.create(
                    user=request.user,
                    project=project,
                    amount=amount
                )
        except (ValueError, TypeError):
            pass

        return redirect(project.get_absolute_url())
