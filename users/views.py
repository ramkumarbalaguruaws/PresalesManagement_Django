from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import ProtectedError, Q
from .models import User, Proposal, Customer, Project, Product
from .forms import (
    UserForm,
    ProposalForm,
    CustomerForm,
    ProjectForm,
    ProductForm,
    UserCreationForm,
)
import random


def get_queryset_for_user(model, request, created_by_field="created_by"):
    """Helper function to filter querysets based on user role"""
    if request.user.role == "admin":
        return model.objects.all()

    # Only apply created_by filter for Proposal model
    if model == Proposal:
        return model.objects.filter(**{created_by_field: request.user})

    # For all other models, return all objects
    return model.objects.all()


@login_required
def dashboard(request):
    from django.db.models import Count, Sum
    from django.db.models.functions import TruncMonth
    from datetime import datetime, timedelta

    # Get filter parameters
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    sales_director = request.GET.get("sales_director")
    country = request.GET.get("country")

    # Base queryset with filters
    proposals = get_queryset_for_user(Proposal, request)
    if start_date:
        proposals = proposals.filter(submission_date__gte=start_date)
    if end_date:
        proposals = proposals.filter(submission_date__lte=end_date)
    if sales_director:
        proposals = proposals.filter(sales_director=sales_director)
    if country:
        proposals = proposals.filter(project__country=country)

    # Get all unique values for filters
    all_sales_directors = (
        proposals.values_list("sales_director", flat=True)
        .distinct()
        .order_by("sales_director")
    )
    all_countries = (
        Project.objects.values_list("country", flat=True).distinct().order_by("country")
    )

    # Calculate summary statistics
    total_proposals = proposals.count()
    blocked_proposals = proposals.filter(status__iexact="blocked").count()
    ongoing_proposals = proposals.filter(status__iexact="ongoing").count()
    closed_proposals = proposals.filter(status__iexact="closed").count()
    total_value = proposals.aggregate(total=Sum("commercial_value"))["total"] or 0

    # Status distribution for pie chart
    status_distribution = {
        "labels": ["Blocked", "Ongoing", "Closed"],
        "values": [blocked_proposals, ongoing_proposals, closed_proposals],
    }

    # Country distribution for bar chart
    country_distribution = {"labels": [], "datasets": []}
    country_data = (
        proposals.values("project__country")
        .annotate(
            total=Count("id"),
            blocked=Count("id", filter=Q(status__iexact="blocked")),
            ongoing=Count("id", filter=Q(status__iexact="ongoing")),
            closed=Count("id", filter=Q(status__iexact="closed")),
        )
        .order_by("-total")[:10]
    )

    # Prepare dataset for each status
    blocked_data = []
    ongoing_data = []
    closed_data = []

    for item in country_data:
        if item["project__country"]:  # Only add if country exists
            country_distribution["labels"].append(item["project__country"])
            blocked_data.append(item["blocked"])
            ongoing_data.append(item["ongoing"])
            closed_data.append(item["closed"])

    country_distribution["datasets"] = [
        {"label": "Blocked", "data": blocked_data, "backgroundColor": "#ff6384"},
        {"label": "Ongoing", "data": ongoing_data, "backgroundColor": "#36a2eb"},
        {"label": "Closed", "data": closed_data, "backgroundColor": "#4bc0c0"},
    ]

    # Sales Director Performance
    sales_director_performance = {"labels": [], "datasets": []}
    sales_data = (
        proposals.values("sales_director")
        .annotate(
            blocked=Count("id", filter=Q(status__iexact="blocked")),
            ongoing=Count("id", filter=Q(status__iexact="ongoing")),
            closed=Count("id", filter=Q(status__iexact="closed")),
        )
        .order_by("-closed")
    )

    # Prepare dataset for each status
    blocked_counts = []
    ongoing_counts = []
    closed_counts = []

    for item in sales_data:
        if item["sales_director"]:  # Only add if sales director exists
            sales_director_performance["labels"].append(item["sales_director"])
            blocked_counts.append(item["blocked"])
            ongoing_counts.append(item["ongoing"])
            closed_counts.append(item["closed"])

    sales_director_performance["datasets"] = [
        {
            "label": "Blocked",
            "data": blocked_counts,
            "backgroundColor": "#ff6384",
        },
        {
            "label": "Ongoing",
            "data": ongoing_counts,
            "backgroundColor": "#ffcd56",
        },
        {
            "label": "Closed",
            "data": closed_counts,
            "backgroundColor": "#4bc0c0",
        },
    ]

    import json

    context = {
        "total_proposals": total_proposals,
        "blocked_proposals": blocked_proposals,
        "ongoing_proposals": ongoing_proposals,
        "closed_proposals": closed_proposals,
        "total_value": total_value,
        "status_distribution": json.dumps(status_distribution),
        "country_distribution": json.dumps(country_distribution),
        "sales_director_performance": json.dumps(sales_director_performance),
        "all_sales_directors": all_sales_directors,
        "all_countries": all_countries,
    }

    return render(request, "users/dashboard.html", context)


@login_required
def user_list(request):
    if request.user.role == "admin":
        users = User.objects.all()
    else:
        users = User.objects.filter(id=request.user.id)
    return render(request, "users/user_list.html", {"users": users})


@login_required
def create_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully")
            return redirect("user_list")
    else:
        form = UserCreationForm()
    return render(request, "users/user_form.html", {"form": form})


@login_required
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.user.role != "admin" and user.id != request.user.id:
        messages.error(request, "You can only edit your own profile")
        return redirect("user_list")

    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated successfully")
            return redirect("user_list")
    else:
        form = UserForm(instance=user)
    return render(request, "users/user_form.html", {"form": form})


@login_required
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.user.role != "admin":
        messages.error(request, "Only admins can delete users")
        return redirect("user_list")

    if request.method == "POST":
        user.delete()
        messages.success(request, "User deleted successfully")
        return redirect("user_list")
    return render(request, "users/confirm_delete_user.html", {"user": user})


@login_required
def proposals(request):
    proposals = get_queryset_for_user(Proposal, request)
    return render(request, "users/proposals.html", {"proposals": proposals})


@login_required
def create_proposal(request):
    if request.method == "POST":
        form = ProposalForm(request.POST, user=request.user)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.created_by = request.user
            proposal.save()
            messages.success(request, "Proposal created successfully")
            return redirect("proposals")
    else:
        form = ProposalForm(user=request.user)
        form.fields["created_by"].initial = request.user
        form.fields["project"].queryset = get_queryset_for_user(Project, request)
    return render(request, "users/proposal_form.html", {"form": form})


@login_required
def edit_proposal(request, pk):
    proposal = get_object_or_404(Proposal, pk=pk)
    if request.user.role != "admin" and proposal.created_by != request.user:
        messages.error(request, "You can only edit your own proposals")
        return redirect("proposals")

    if request.method == "POST":
        form = ProposalForm(request.POST, instance=proposal, user=request.user)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.created_by = request.user
            proposal.save()
            messages.success(request, "Proposal updated successfully")
            return redirect("proposals")
    else:
        form = ProposalForm(instance=proposal, user=request.user)
        form.fields["created_by"].initial = request.user
    return render(request, "users/proposal_form.html", {"form": form})


@login_required
def delete_proposal(request, pk):
    proposal = get_object_or_404(Proposal, pk=pk)
    if request.user.role != "admin" and proposal.created_by != request.user:
        messages.error(request, "You can only delete your own proposals")
        return redirect("proposals")

    if request.method == "POST":
        proposal.delete()
        messages.success(request, "Proposal deleted successfully")
        return redirect("proposals")
    return render(request, "users/confirm_delete.html", {"proposal": proposal})


@login_required
def customer_list(request):
    customers = get_queryset_for_user(Customer, request)
    return render(request, "users/customer_list.html", {"customers": customers})


@login_required
def create_customer(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.created_by = request.user
            customer.save()
            messages.success(request, "Customer created successfully")
            return redirect("customer_list")
    else:
        form = CustomerForm()
    return render(request, "users/customer_form.html", {"form": form})


@login_required
def edit_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.user.role != "admin" and customer.created_by != request.user:
        messages.error(request, "You can only edit your own customers")
        return redirect("customer_list")

    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer updated successfully")
            return redirect("customer_list")
    else:
        form = CustomerForm(instance=customer)
    return render(request, "users/customer_form.html", {"form": form})


@login_required
def delete_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.user.role != "admin" and customer.created_by != request.user:
        messages.error(request, "You can only delete your own customers")
        return redirect("customer_list")

    if request.method == "POST":
        try:
            customer.delete()
            messages.success(request, "Customer deleted successfully")
        except ProtectedError:
            messages.error(
                request,
                "Cannot delete customer with linked projects. Delete projects first.",
            )
        return redirect("customer_list")
    return render(request, "users/confirm_delete.html", {"customer": customer})


@login_required
def project_list(request):
    projects = get_queryset_for_user(Project, request)
    return render(request, "users/project_list.html", {"projects": projects})


@login_required
def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            messages.success(request, "Project created successfully")
            return redirect("project_list")
    else:
        form = ProjectForm()
    return render(request, "users/project_form.html", {"form": form})


@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.user.role != "admin" and project.created_by != request.user:
        messages.error(request, "You can only edit your own projects")
        return redirect("project_list")

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Project updated successfully")
            return redirect("project_list")
    else:
        form = ProjectForm(instance=project)
    return render(request, "users/project_form.html", {"form": form})


@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.user.role != "admin" and project.created_by != request.user:
        messages.error(request, "You can only delete your own projects")
        return redirect("project_list")

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project deleted successfully")
        return redirect("project_list")
    return render(request, "users/confirm_delete.html", {"project": project})


@login_required
def product_list(request):
    products = get_queryset_for_user(Product, request)
    return render(request, "users/product_list.html", {"products": products})


@login_required
def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            messages.success(request, "Product created successfully")
            return redirect("product_list")
    else:
        form = ProductForm()
    return render(request, "users/product_form.html", {"form": form})


@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.user.role != "admin" and product.created_by != request.user:
        messages.error(request, "You can only edit your own products")
        return redirect("product_list")

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully")
            return redirect("product_list")
    else:
        form = ProductForm(instance=product)
    return render(request, "users/product_form.html", {"form": form})


@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.user.role != "admin" and product.created_by != request.user:
        messages.error(request, "You can only delete your own products")
        return redirect("product_list")

    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully")
        return redirect("product_list")
    return render(request, "users/confirm_delete_product.html", {"product": product})


def change_password(request):
    return render(request, "users/change_password.html")


def save_column_preferences(request):
    return render(request, "users/save_column_preferences.html")


def export_proposals_csv(request):
    return render(request, "users/export_proposals_csv.html")


from django.http import JsonResponse


@login_required
def get_project_customer(request, project_id):
    try:
        project = Project.objects.get(pk=project_id)
        return JsonResponse(
            {
                "name": project.customer.name,
                "country": project.country,
            }
        )
    except Project.DoesNotExist:
        return JsonResponse({"error": "Project not found"}, status=404)
