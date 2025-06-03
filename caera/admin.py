from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from caera.models import User, Tag, Proposal, Comment, Project, Donation, City


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ("title", "get_tags", "description", "author", "created_at")
    list_filter = ("tags", "author", "created_at")
    search_fields = ("title", "description", "author__username")
    ordering = ("-created_at",)


    def get_tags(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())
    get_tags.short_description = "Tags"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title", "proposal", "author", "created_at",
        "fundraising_goal", "get_total_donated", "get_progress_percent"
    )
    list_filter = ("tags", "author", "created_at")
    search_fields = ("title", "description", "author__username", "proposal__title")
    ordering = ("-created_at",)
    filter_horizontal = ("tags",)

    def get_total_donated(self, obj):
        return f"${obj.total_donated:,.2f}"
    get_total_donated.short_description = "Накопичено"

    def get_progress_percent(self, obj):
        return f"{obj.fundraising_progress_percent:.1f}%"
    get_progress_percent.short_description = "Прогрес збору"


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ("user", "project", "amount", "created_at")
    list_filter = ("user", "project", "created_at")
    search_fields = ("user__username", "project__title")
    ordering = ("-created_at",)


admin.site.register(City)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(User, UserAdmin)
