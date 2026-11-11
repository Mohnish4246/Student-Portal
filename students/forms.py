from django import forms 
from .models import Student
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from pypdf import PdfReader
from pypdf.errors import PdfReadError

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "name",
            "age",
            "email",
            "phone",
            "marks",
            "city",
            "course",
            "skills",
            "profile_image",
            "document"
        ] 


    def clean_document(self):
        document = self.cleaned_data.get("document")

        if document:
            if not document.name.lower().endswith(".pdf"):
                raise forms.ValidationError(
                    "Only PDF files are allowed."
                )

            if document.size > 5 * 1024 * 1024:
                raise forms.ValidationError(
                    "File size must be less than 5 MB."
                )

            try:
                document.seek(0)
                reader = PdfReader(document)

                if reader.is_encrypted:
                    raise forms.ValidationError(
                        "Encrypted PDF files are not allowed."
                    )

                if not reader.pages:
                    raise forms.ValidationError(
                        "The PDF must contain at least one page."
                    )

            except PdfReadError:
                raise forms.ValidationError(
                    "Please upload a valid PDF file."
                )
            except Exception as exc:
                if isinstance(exc, forms.ValidationError):
                    raise
                raise forms.ValidationError(
                    "The uploaded PDF could not be read."
                )
            finally:
                document.seek(0)

        return document




    def clean_age(self):
        age = self.cleaned_data["age"]
        if age<18 or age>60:
            raise forms.ValidationError(
                "Age must be between 18 and 60."
            )
        return age

    def clean_marks(self):
        marks = self.cleaned_data["marks"]
        if marks<0 or marks>100:
            raise forms.ValidationError(
                "Marks must be between 0 and 100"
            )
        return marks

    def clean(self):
        return super().clean()

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")

        if phone:
            if not phone.isdigit():
                raise forms.ValidationError(
                    "Phone number must contain only digits."
                )

            if len(phone) != 10:
                raise forms.ValidationError(
                    "Phone number must contain exactly 10 digits."
                )

        return phone

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if email:
            if email.lower().endswith("@example.com"):
                raise forms.ValidationError(
                    "This email domain is not allowed."
                )

        return email

class RegisterForm(UserCreationForm): # username = xyz, assword = abc@1234

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User

        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ] 

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "An account with this email address already exists."
            )

        return email
