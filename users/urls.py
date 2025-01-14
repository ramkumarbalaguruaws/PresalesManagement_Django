from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("users/", views.user_list, name="user_list"),
    path("users/create/", views.create_user, name="create_user"),
    path("users/<int:pk>/edit/", views.edit_user, name="edit_user"),
    path("users/<int:pk>/delete/", views.delete_user, name="delete_user"),
    path("change-password/", views.change_password, name="change_password"),
    path("proposals/", views.proposals, name="proposals"),
    path("proposals/create/", views.create_proposal, name="create_proposal"),
    path("proposals/<int:pk>/edit/", views.edit_proposal, name="edit_proposal"),
    path("proposals/<int:pk>/delete/", views.delete_proposal, name="delete_proposal"),
    path(
        "save-column-preferences/",
        views.save_column_preferences,
        name="save_column_preferences",
    ),
    path("products/", views.product_list, name="product_list"),
    path("products/create/", views.create_product, name="product_create"),
    path("products/<int:pk>/update/", views.edit_product, name="product_update"),
    path("products/<int:pk>/delete/", views.delete_product, name="product_delete"),
    path("customers/", views.customer_list, name="customer_list"),
    path("customers/create/", views.create_customer, name="create_customer"),
    path("customers/<int:pk>/edit/", views.edit_customer, name="edit_customer"),
    path("customers/<int:pk>/delete/", views.delete_customer, name="delete_customer"),
    path("projects/", views.project_list, name="project_list"),
    path("projects/create/", views.create_project, name="create_project"),
    path("projects/<int:pk>/edit/", views.edit_project, name="edit_project"),
    path("projects/<int:pk>/delete/", views.delete_project, name="delete_project"),
    path(
        "export-proposals-csv/", views.export_proposals_csv, name="export_proposals_csv"
    ),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html", redirect_authenticated_user=True
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "api/projects/<int:project_id>/customer/",
        views.get_project_customer,
        name="get_project_customer",
    ),
]
