from django.core.exceptions import ValidationError
from .models import TinyUrls
import re
from django import forms


class UrlForm(forms.ModelForm):
    class Meta:
        model = TinyUrls
        fields = ['full_url','tiny_url']
        widgets = {
            'full_url':forms.widgets.URLInput(attrs={'placeholder':'paste any long urls.. here'}),
            'tiny_url':forms.widgets.TextInput(attrs={'minlength':5}),
            }

    def clean_full_url(self):
        url = self.cleaned_data['full_url']
        # if not str(url).startswith(('http','https',)):
        #     raise ValidationError('url must begin with http , https')
        if len(url) > 2000:
            raise ValidationError('Url exceeded the size limit of 2000 charecters.!')
        if len(url) == 0 or str(url).isspace() :
            raise ValidationError('provide a valid url')
        else:
            return url

    def clean_tiny_url(self):
        tiny_url = self.cleaned_data['tiny_url']
        length = len(tiny_url)
        if length < 5 and length != 0:
            raise ValidationError(f'Atleast 5 charecters required.')
        elif length > 10:
            raise ValidationError(f'Atmost 10 charecters allowed. But got {length}.')
        elif length != 0:
            s2=re.findall('^[a-zA-Z0-9,-]{5,10}$',tiny_url)   # regex to ensure the key given is valid. (some string and digits of 5 to 10 charecters).
            try:
                s=str(s2[0])
                if s.startswith('-') or s.endswith('-'):
                    raise ValueError()
            except IndexError:
                raise ValidationError(f'Use letters and digits and -.')
            except ValueError:
                raise ValidationError(f"Hyphen ' - ' cannot begin or end a tiny url")
        if TinyUrls.objects.filter(tiny_url = tiny_url).exists():
            raise ValidationError(f'{tiny_url} exists.Choose another tiny url.')
        return tiny_url

        
