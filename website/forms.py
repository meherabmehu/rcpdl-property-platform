import re
from django import forms

class InquiryForm(forms.Form):
    name = forms.CharField(required=False, max_length=100)
    phone = forms.CharField(max_length=30)
    project = forms.ChoiceField(choices=[("1", "Project 01"), ("2", "Project 02")])
    message = forms.CharField(required=False, max_length=2000, widget=forms.Textarea)
    permission = forms.BooleanField(required=False)

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        normalized = re.sub(r"[\s()-]", "", phone).translate(str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789"))
        if not re.fullmatch(r"(?:\+?88)?01[3-9]\d{8}", normalized):
            raise forms.ValidationError("Enter a valid phone number.")
        return normalized
