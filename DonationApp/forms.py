from django import forms

class DonationForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=10,
        label="Donation Amount (BDT)"
    )
