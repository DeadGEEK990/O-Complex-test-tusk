from django import forms


class GetWeatherForm(forms.Form):
    city = forms.CharField(max_length=50)

    def __str__(self):
        return f"City: {self.city}"
