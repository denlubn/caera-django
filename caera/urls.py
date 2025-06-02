from django.urls import path

from caera.views import ProposalListView, ProposalDetailView, profile_view, ProfileUpdateView, ProposalCreateView, \
    TagCreateView, ProposalUpdateView, ProposalDeleteView, ProfileCreateView, \
    ProjectCreateView, ProjectListView, ProjectDetailView, ProjectUpdateView, ProjectDeleteView

urlpatterns = [
    path("tag/create/", TagCreateView.as_view(), name="tag-create"),

    path("", ProposalListView.as_view(), name="proposal-list"),
    path("proposals/<int:pk>/", ProposalDetailView.as_view(), name="proposal-detail"),
    path("proposals/create/", ProposalCreateView.as_view(), name="proposal-create"),
    path("proposals/<int:pk>/update/", ProposalUpdateView.as_view(), name="proposal-update"),
    path("proposals/<int:pk>/delete/", ProposalDeleteView.as_view(), name="proposal-delete"),

    path("proposals/<int:pk>/projects/", ProjectListView.as_view(), name="project-list"),
    path("proposals/<int:pk>/projects/create/", ProjectCreateView.as_view(), name="project-create"),
    path("proposals/<int:pk>/projects/<int:project_pk>", ProjectDetailView.as_view(), name="project-detail"),
    path("proposals/<int:pk>/projects/<int:project_pk>/update/", ProjectUpdateView.as_view(), name="project-update"),
    path("proposals/<int:pk>/projects/<int:project_pk>/delete/", ProjectDeleteView.as_view(), name="project-delete"),

    path("accounts/profile/", profile_view, name="profile"),
    path("accounts/create/", ProfileCreateView.as_view(), name="profile-create"),
    path("accounts/profile/update/", ProfileUpdateView.as_view(), name="profile-update"),
]

app_name = "caera"
