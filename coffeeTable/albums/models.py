from django.db import models
import datetime


class Album (models.Model):
    id = models.AutoField(primary_key = True)
    title = models.CharField(max_length = 50)
    temp_title = models.CharField(max_length = 50, null=True)
    # description = models.TextField(blank = True)
    date_created = models.DateTimeField(auto_now_add = True)
    # userId = models.ForeignKey(User)
    thumbnail = models.OneToOneField('Image', null=True)
    
    def __unicode__(self):
        return self.title
            
    # Returns the number of pages in an album
    def number_of_pages (self):
        pages = Page.objects.filter(album=self)
        return pages.count()
        

class Image (models.Model):
    id = models.AutoField(primary_key = True)
    # title = models.CharField(max_length = 50)
    # description = models.TextField(blank = True)
    # image = models.ImageField(upload_to="images/")
    uri = models.URLField(verify_exists = True)
    page = models.ForeignKey('Page', related_name="images", db_index=True)
    number = models.IntegerField()

    def __unicode__(self):
        return self.uri


class Page (models.Model):
    TEMPLATE_CHOICES = (
        (u'monoB1', u'One large cover'),
        (u'monoS1', u'One small cover'),
        (u'mono3', u'Three on a cover'),
        (u'mono4', u'Four on a cover'),
        (u'duo1', u'One on a double-page'),
        (u'duo2', u'Two on a double-page'),
        (u'duoR3', u'Three on a double-page [detail right]'),
        (u'duoL3', u'Three on a double-page [detail left]'),
        (u'duoR5', u'Five on a double-page [detail right]'),
        (u'duoL5', u'Five on a double-page [detail left]'),
    )
    album = models.ForeignKey('Album', related_name="pages", db_index=True)
    template = models.CharField(max_length=8, choices=TEMPLATE_CHOICES)
    number = models.IntegerField()
    
    def __unicode__(self):
        return self.template
        
    # Returns the number of images allowed in the current page template
    def get_images_allowed (self):
        if self.template == "monoB1" or self.template == "monoS1" or self.template == "duo1":
            return (1)
        if self.template == "duo2":
            return (2)
        if self.template == "mono3" or self.template == "duoR3" or self.template == "duoL3":
            return (3)
        if self.template == "mono4":
            return (4)
        if self.template == "duoR5" or self.template == "duoL5":
            return (5)
        
            

        
        
        
        
        
        
        
        
        
