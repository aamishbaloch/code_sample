from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as OrigUserAdmin
from django.utils.translation import ugettext_lazy as _


User = get_user_model()


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone', 'email', 'first_name', 'last_name', 'verification_code', 'is_staff', 'is_superuser',
                  'verified')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdmin(OrigUserAdmin):
    add_form = UserCreationForm
    search_fields = ('email',)
    list_filter = ('verified',)
    list_display = (
        'id', 'first_name', 'last_name', 'verified', 'phone', 'email', 'gender', 'active', 'address',
        'is_staff', 'is_superuser', 'last_login', 'joined_on')
    ordering = ('first_name',)
    fieldsets = (
        (_('Personal Info'), {
            'fields': (
                'phone', 'verified', 'email', 'first_name', 'last_name', 'gender', 'address', 'verification_code'
            )
        }),
        (_('Permissions Info'), {'fields': ('active', 'is_superuser',)}),
        (_('Important dates'), {'fields': ('last_login', 'joined_on')}),
        ('Password Info', {'fields': ('password',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'first_name', 'last_name', 'verified', 'email', 'password1', 'password2',
                       'gender', 'verification_code')}
         ),
    )


admin.site.register(User, UserAdmin)

