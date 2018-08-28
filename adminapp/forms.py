from django import forms
from .models import CraneDevices


class AddForm(forms.Form):

	type = forms.IntegerField(
		min_value=0,
		max_value=2,
		required=True,
		help_text='Device Type :',
	)
	
	alias = forms.CharField(
		required=True,
		help_text='Alias :',
	)
	
	
	uuid = forms.CharField(
		required=True,
		help_text='Device uuid :',
	)
	

	field_order = (
		'amount',
		'comment',
		'send_email',
	)

	def form_action(self, account, user):
		return Account.withdraw(
			id=account.pk,
			user=account.user,
			amount=self.cleaned_data['amount'],
			withdrawn_by=user,
			comment=self.cleaned_data['comment'],
			asof=timezone.now(),
		)