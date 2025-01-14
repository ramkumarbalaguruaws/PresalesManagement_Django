from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, URLValidator
import csv
from django.http import HttpResponse


class User(AbstractUser):
    ROLES = (
        ("ADMIN", "Administrator"),
        ("SALES", "Sales"),
        ("PRESALES", "Presales"),
        ("VIEWER", "Viewer"),
    )

    role: str = models.CharField(max_length=20, choices=ROLES, default="VIEWER")
    phone: str = models.CharField(max_length=20, blank=True)
    department: str = models.CharField(max_length=100, blank=True)
    is_active: bool = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.username} ({self.get_role_display()})"

    def is_admin(self) -> bool:
        return self.role == "ADMIN"

    def is_presales(self) -> bool:
        return self.role == "PRESALES"

    def can_edit_proposals(self) -> bool:
        return self.role in ["ADMIN", "PRESALES"]

    def can_view_all_proposals(self) -> bool:
        return self.role in ["ADMIN", "PRESALES", "SALES"]

    def can_create_proposals(self) -> bool:
        return self.role in ["ADMIN", "PRESALES"]


class Customer(models.Model):
    name: str = models.CharField(max_length=200)
    contact_details: str = models.TextField()
    remarks: Optional[str] = models.TextField(blank=True, null=True)
    created_at: datetime = models.DateTimeField(auto_now_add=True)
    updated_at: datetime = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    def delete(self, *args, **kwargs) -> None:
        if self.projects.exists():
            raise models.ProtectedError(
                "Cannot delete customer with linked projects", self
            )
        super().delete(*args, **kwargs)


class Project(models.Model):
    project_name: str = models.CharField(max_length=200)
    customer: models.ForeignKey[Customer] = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="projects"
    )
    country: str = models.CharField(max_length=100)
    link: str = models.URLField(validators=[URLValidator()])
    created_at: datetime = models.DateTimeField(auto_now_add=True)
    updated_at: datetime = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.project_name} ({self.customer.name}, {self.country})"

    class Meta:
        ordering = ["-created_at"]


class Proposal(models.Model):
    PRIORITY_CHOICES = (
        ("P1", "P1 - Critical"),
        ("P2", "P2 - High"),
        ("P3", "P3 - Medium"),
    )

    STATUS_CHOICES = (
        ("ONGOING", "Ongoing"),
        ("BLOCKED", "Blocked"),
        ("CLOSED", "Closed"),
    )

    GATEWAY_CHOICES = (
        ("JAV", "JAV"),
        ("SUB", "SUB"),
        ("BHI", "BHI"),
        ("PAK", "PAK"),
    )

    TERMINAL_CHOICES = (
        ("1m2_3W_MDM2510", "1m2 3W MDM2510"),
        ("1m8_5W_MDM2510", "1m8 5W MDM2510"),
        ("2m4_8W_MDM2510", "2m4 8W MDM2510"),
    )

    # Basic Information
    project: models.ForeignKey[Project] = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="proposals",
        help_text="Select the project this proposal belongs to",
    )
    priority: str = models.CharField(max_length=20, choices=PRIORITY_CHOICES)

    # Technical Details
    bandwidth: str = models.CharField(max_length=100, default="100Mbps")
    gateway: str = models.CharField(
        max_length=20, choices=GATEWAY_CHOICES, default="JAV"
    )
    terminal_count: int = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], default=1
    )
    terminal_type: str = models.CharField(
        max_length=50, choices=TERMINAL_CHOICES, default="1m2_3W_MDM2510"
    )

    # Business Information
    sales_director: str = models.CharField(max_length=200)
    presales_owner: str = models.EmailField(default="admin@example.com")
    submission_date: date = models.DateField()
    proposal_link: str = models.URLField(
        validators=[URLValidator()], default="https://example.com"
    )
    commercial_value: Decimal = models.DecimalField(
        max_digits=15, decimal_places=2, validators=[MinValueValidator(0)]
    )
    status: str = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="ONGOING"
    )
    remarks: Optional[str] = models.TextField(blank=True, null=True)

    # Metadata
    created_by: models.ForeignKey[User] = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="proposals"
    )
    created_at: datetime = models.DateTimeField(auto_now_add=True)
    updated_at: datetime = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-submission_date"]
        permissions = [
            ("can_view_all_proposals", "Can view all proposals"),
            ("can_edit_all_proposals", "Can edit all proposals"),
        ]

    def __str__(self) -> str:
        return f"{self.project.project_name} ({self.get_status_display()})"

    @classmethod
    def export_to_csv(cls, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="proposals.csv"'

        writer = csv.writer(response)
        writer.writerow(
            [
                "Project",
                "Priority",
                "Bandwidth",
                "Gateway",
                "Terminal Count",
                "Terminal Type",
                "Sales Director",
                "Presales Owner",
                "Submission Date",
                "Proposal Link",
                "Commercial Value",
                "Status",
                "Remarks",
            ]
        )

        for proposal in queryset:
            writer.writerow(
                [
                    proposal.project.project_name,
                    proposal.get_priority_display(),
                    proposal.bandwidth,
                    proposal.get_gateway_display(),
                    proposal.terminal_count,
                    proposal.get_terminal_type_display(),
                    proposal.sales_director,
                    proposal.presales_owner,
                    proposal.submission_date.strftime("%Y-%m-%d"),
                    proposal.proposal_link,
                    str(proposal.commercial_value),
                    proposal.get_status_display(),
                    proposal.remarks or "",
                ]
            )

        return response


class Product(models.Model):
    item = models.CharField(max_length=200)
    description = models.TextField()
    links = models.URLField(validators=[URLValidator()])

    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="products", null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.item
