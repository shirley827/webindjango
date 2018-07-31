from django import forms
from myapp.models import Order, Client,Clientavatar


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('product','client','num_units')
        widgets = {'client':forms.RadioSelect}

class InterestForm(forms.Form):
    interested = forms.IntegerField(widget=forms.RadioSelect(choices=[(1,"Yes"),(0,"No")]))
    quantity = forms.IntegerField(min_value=1,initial=1)
    comment = forms.CharField(widget=forms.Textarea(),required=False,label="Additional Comments")

class ClientForm(forms.ModelForm):

    class Meta:
        model  = Client
        fields = ('username','password','email','first_name','last_name','company','shipping_address','city','province','interested_in')
        widgets = {'password':forms.PasswordInput,'email':forms.EmailInput,'interested_in':forms.CheckboxSelectMultiple}


