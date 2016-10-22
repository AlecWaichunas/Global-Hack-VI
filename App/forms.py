from django import forms

class RegisterForm(forms.Form):
    shelter_name = forms.CharField()
    shelter_email = forms.CharField()
    shelter_password = forms.CharField()
    shelter_support_email = forms.CharField()
    shelter_support_telephone = forms.CharField()
    shelter_address = forms.CharField()
    shelter_city = forms.CharField()
    shelter_state = forms.CharField()
    shelter_desc = forms.CharField()
    shelter_rooms = forms.BooleanField()
    shelter_foods = forms.BooleanField()
    shelter_housing = forms.BooleanField()

'''
class IntakeForm(forms.Form):
    enrollment_date = forms.DateField(blank=True, null=True)
    bed_date = forms.DateField(blank=True, null=True)
    facility_num = forms.CharField()
    room_num = forms.IntegerField()
    bed_num = forms.IntegerField()
    
    subject = forms.CharField()
    email = forms.EmailField(required=False)
    message = forms.CharField()
'''