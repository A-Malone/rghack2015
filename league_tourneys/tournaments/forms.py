from django import forms

class TournamentForm(forms.Form):
    name                = forms.CharField(label='Tournament Name', max_length=100)
    url                 = forms.CharField(label='Tournament Url', max_length=100)
    tourney_type        = forms.MultipleChoiceField(choices=(
                            ('single elimination', 'Single Elimination'),
                            ('double elimination', 'Double Elimination')
                        ))
    description         = forms.CharField(widget=forms.Textarea)
    signup_cap          = forms.IntegerField()

class TeamForm(forms.Form):
    name                = forms.CharField(label='Team Name', max_length=100)
    members             = forms.CharField(label='Team Members', max_length=200)