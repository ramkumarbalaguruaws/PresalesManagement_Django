from django.contrib import admin
from .models import User, Proposal, Product, Customer, Project


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role", "is_active")
    list_filter = ("role", "is_active")
    search_fields = ("username", "email")
    ordering = ("-date_joined",)


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = (
        "get_project_name",
        "priority",
        "get_country",
        "get_customer",
        "sales_director",
        "submission_date",
    )

    def get_project_name(self, obj):
        return obj.project.project_name

    get_project_name.short_description = "Project Name"

    def get_country(self, obj):
        return obj.project.country

    get_country.short_description = "Country"

    def get_customer(self, obj):
        return obj.project.customer

    get_customer.short_description = "Customer"
    list_filter = ("priority", "project__country", "sales_director")
    search_fields = ("project__project_name", "customer")
    date_hierarchy = "submission_date"
    ordering = ("-submission_date",)
    fieldsets = (
        (
            "Project Details",
            {"fields": ("project", "priority", "customer")},
        ),
        (
            "Technical Details",
            {"fields": ("bandwidth", "gateway", "terminal_count", "terminal_type")},
        ),
        (
            "Commercial Details",
            {
                "fields": (
                    "sales_director",
                    "submission_date",
                    "proposal_link",
                    "commercial_value",
                )
            },
        ),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("item", "created_at", "updated_at")
    search_fields = ("item", "description")
    ordering = ("-created_at",)
    fieldsets = (("Product Details", {"fields": ("item", "description", "links")}),)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name", "contact_details")
    ordering = ("-created_at",)
    fieldsets = (
        (
            "Customer Details",
            {"fields": ("name", "contact_details", "remarks")},
        ),
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("project_name", "customer", "country", "link")
    list_filter = ("customer", "country")
    search_fields = ("project_name", "customer__name")
    ordering = ("-created_at",)
    fieldsets = (
        (
            "Project Details",
            {"fields": ("project_name", "customer", "country", "link")},
        ),
    )
