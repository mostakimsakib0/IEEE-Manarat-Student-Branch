from django.contrib import admin
from .models import UserProfile, Session, WebDetails


admin.site.register(
    [
        Session,
        WebDetails,  
    ]
)
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user__first_name",
        "designation_display",
        "session",
        "is_valid",
        "timestamp",
    )
    list_filter = ("is_valid", "session", "designation")
    search_fields = ("user__first_name", "user__last_name", "user__email")

    def designation_display(self, obj):
        return obj.get_designation_display()

    designation_display.short_description = "Designation"
