from django.db import models
from django.core.validators import URLValidator
from hashlib import sha256
import random , string

# Create your models here.


class TinyUrls(models.Model):
    full_url = models.URLField(verbose_name='URL',max_length=2000)
    entry_hash = models.CharField(max_length=64)
    url_hash = models.CharField(max_length=64)
    tiny_url = models.CharField(max_length=10,blank=True)
    clicks = models.PositiveIntegerField(default=0)
    added = models.DateTimeField(auto_now_add=True)

    def clicked(self):
        self.clicks+=1
        self.save()

    def save(self, *args, **kwargs):
        if not self.id:
            self.url_hash = sha256(str(self.full_url).encode('utf-8')).hexdigest()
            if self.tiny_url == '' or self.tiny_url.isspace():  # to generate a tiny key if nothing provided by the user
                random.seed(self.url_hash)
                self.tiny_url = ''.join(random.choices(string.ascii_letters+string.digits,k=6)) # generated tiny url
            combined_string = str(self.full_url + self.tiny_url)
            self.entry_hash = sha256(combined_string.encode('utf-8')).hexdigest()  # to make a unique hash value,that not solely depend on the full_url.
            d = TinyUrls.objects.filter(entry_hash=self.entry_hash) # get the entry with the extact same hash.
            if len(d) == 1:  # to prevent duplication of same url with an exact same tiny tail (aka tiny_url)
                return TinyUrls.objects.get(entry_hash = self.entry_hash)
        return super().save(*args,**kwargs)
