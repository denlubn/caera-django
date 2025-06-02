from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import UpdateView

from caera.forms import ProposalForm, TagForm, ProfileCreationForm, ProposalSearchForm, ProjectForm, CommentForm
from caera.models import Proposal, User, Tag, Project, Comment


@login_required
def profile_view(request):
    return render(request, "accounts/profile.html")


class ProfileCreateView(generic.CreateView):
    model = User
    # fields = "__all__"
    form_class = ProfileCreationForm
    template_name = "accounts/profile_form.html"


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    template_name = 'accounts/profile_update.html'
    success_url = reverse_lazy('caera:profile')

    def get_object(self, queryset=None):
        return self.request.user


class ProposalListView(generic.ListView):
    model = Proposal

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProposalListView, self).get_context_data(**kwargs)

        title = self.request.GET.get("title", "")
        tag = self.request.GET.get("tags")

        context["search_form"] = ProposalSearchForm(initial={
            "title": title,
            "tags": tag,
        })

        return context

    def get_queryset(self):
        queryset = Proposal.objects.select_related('author', 'city').prefetch_related('tags')
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


class ProposalCreateView(LoginRequiredMixin, generic.CreateView):
    model = Proposal
    form_class = ProposalForm


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
        return Project.objects.filter(proposal__id=proposal_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['proposal'] = get_object_or_404(Proposal, pk=self.kwargs['pk'])
        return context


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    form_class = ProjectForm


class ProjectDetailView(generic.DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['proposal'] = get_object_or_404(Proposal, pk=self.kwargs['pk'])
        return context


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    form_class = ProjectForm


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
