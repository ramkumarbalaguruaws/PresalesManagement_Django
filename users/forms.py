from django import forms
from .models import User, Proposal, Customer, Project, Product


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "role", "is_active"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "role": forms.Select(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "role", "is_active"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "role": forms.Select(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class ProposalForm(forms.ModelForm):
    created_by = forms.ModelChoiceField(
        queryset=User.objects.all(), widget=forms.HiddenInput(), required=True
    )
    project = forms.ModelChoiceField(
        queryset=Project.objects.select_related("customer").all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=True,
        help_text="Select a project with an associated customer",
    )

    class Meta:
        model = Proposal
        fields = "__all__"
        exclude = ["created_by"]
        widgets = {
            "project": forms.Select(attrs={"class": "form-control"}),
            "submission_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "bandwidth": forms.TextInput(
                attrs={"class": "form-control", "value": "100Mbps"}
            ),
            "terminal_count": forms.NumberInput(
                attrs={"class": "form-control", "value": 1}
            ),
            "proposal_link": forms.URLInput(
                attrs={"class": "form-control", "value": "https://example.com"}
            ),
            "commercial_value": forms.NumberInput(
                attrs={"class": "form-control", "value": 0}
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["presales_owner"].required = False
        self.fields["remarks"].required = False

        if user:
            self.fields["created_by"].initial = user


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "contact_details", "remarks"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "contact_details": forms.TextInput(attrs={"class": "form-control"}),
            "remarks": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["project_name", "customer", "country", "link"]
        widgets = {
            "project_name": forms.TextInput(attrs={"class": "form-control"}),
            "customer": forms.Select(attrs={"class": "form-control"}),
            "country": forms.TextInput(attrs={"class": "form-control"}),
            "link": forms.URLInput(attrs={"class": "form-control"}),
        }


class ProductForm(forms.ModelForm):
    created_by = forms.ModelChoiceField(
        queryset=User.objects.all(), widget=forms.HiddenInput(), required=True
    )

    class Meta:
        model = Product
        fields = ["item", "description", "links", "created_by"]
        widgets = {
            "item": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "links": forms.URLInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["created_by"].initial = user
