from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import UpdateView

from caera.forms import ProposalForm, TagForm, ProfileCreationForm, ProposalSearchForm
from caera.models import Proposal, User, Tag, Project


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
    queryset = Proposal.objects.select_related('author').prefetch_related('tags')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProposalListView, self).get_context_data(**kwargs)

        title = self.request.GET.get("title", "")

        context["search_form"] = ProposalSearchForm(initial={
            "title": title,
        })

        return context

    def get_queryset(self):
        form = ProposalSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(
                title__icontains=form.cleaned_data["title"].strip()
            )
        return self.queryset

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


class ProposalsProjectsListView(generic.ListView):
    model = Project

    def get_queryset(self):
        proposal_id = self.kwargs['pk']
        return Project.objects.filter(proposal__id=proposal_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['proposal'] = get_object_or_404(Proposal, pk=self.kwargs['pk'])
        return context


class TagCreateView(LoginRequiredMixin, generic.CreateView):
    model = Tag
    form_class = TagForm
    success_url = reverse_lazy("caera:proposal-create")
