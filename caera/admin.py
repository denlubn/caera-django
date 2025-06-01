from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from caera.models import User, Tag, Proposal

@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ("title", "get_tags", "description", "author", "created_at")
    list_filter = ("tags", "author")
    search_fields = ("title", "description", "author__username")
    ordering = ("-created_at",)


    def get_tags(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())
    get_tags.short_description = "Tags"


admin.site.register(Tag)
admin.site.register(User, UserAdmin)
