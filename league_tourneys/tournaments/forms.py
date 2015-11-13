from django import forms

class TournamentForm(forms.Form):
    name                = forms.CharField(label='Tournament Name', max_length=100)    
    tournament_type     = forms.MultipleChoiceField(choices=(
                            ('single elimination', 'Single Elimination'),
                            ('double elimination', 'Double Elimination'),
                            ('round robin', 'Round Robin')
                        ))
    description         = forms.CharField(widget=forms.Textarea, required=False)
    signup_cap          = forms.IntegerField(min_value=0, required=False)

class TeamForm(forms.Form):
    name                = forms.CharField(label='Team Name', max_length=100)
    members             = forms.CharField(label='Team Members', max_length=200)

