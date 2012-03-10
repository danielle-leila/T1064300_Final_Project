from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext

from albums.models import *



def index (request):
    """ New user is directed to Welcome page
        Authenticated user views a home page with his albums
            returns a list of album titles and thumbnails
    """
    album_list = Album.objects.all().order_by('-date_created')
    return render_to_response('albums.html', {'album_list': album_list})
    

def initiate_album (request):
    
    # If temp doesn't exist, create temp album and first page
    try:
        Album.objects.get(title="temp")
    except Album.DoesNotExist:
        a = Album(title="temp")
        a.save()
    
        p = initiate_page(request, a)
        
    # Otherwise, get album and page objects
    else:
        a = Album.objects.get(title="temp")
        no_of_pages = Page.objects.filter(album=a).count()
        p = Page.objects.get(album=a, number=no_of_pages)
        
    return create_page(request, p.number, p.template)
        
def initiate_page (request, a, page_no="1", template="monoB1"):

    p = a.pages.create(
        number=page_no, 
        template=template
    )
    return p

def initiate_image (request, p):
    i = p.images.create(
        uri=request.POST.get('image_url'),
        number=request.POST.get('image_number')
    )
    return i

# Template is not passed from back or forward buttons, get template:
def get_template (request, page_no):
    a = Album.objects.get(title="temp")
    p = Page.objects.get(album=a, number=page_no)
    return create_page(request, p.number, p.template)

# Output create a page template
def create_page (request, page_no, template):
    """ Authenticated user creates an album (working album = temp)
    """
    a = Album.objects.get(title="temp")
    
    # Make sure current page exists
    try:
        Page.objects.get(album=a, number=page_no)
    except Page.DoesNotExist:
        # Create current page
        p = initiate_page(request, a, page_no, template)
    else:
        p = Page.objects.get(album=a, number=page_no)
        # Check that template has not changed
        if p.template != template:
            p.template = template
            p.save()
    
    # If an image was added, save it to the current page
    if request.POST:
        try:
            Image.objects.get(page=p, 
            number=request.POST.get('image_number'))
        except Image.DoesNotExist:
            # Create Image
            i = initiate_image (request, p)
        else:
            # Update Image
            i = Image.objects.get(page=p,
            number=request.POST.get('image_number'))
            
            i.uri = request.POST.get('image_url')
            i.save()
    
    # Number of images the template allows
    images_allowed = Page.get_images_allowed(p)
    
    # Count images existing on page
    images_existing = p.images.count()
    
    if images_existing >= 1:
        i_list = Image.objects.filter(page=p)
    else:
        i_list = {}
    
    template_name = template + '.html'
    
    # Render all details to the template
    return render_to_response( 
        template_name, 
        {'p' : p, 'i_list' : i_list, 
        'h' : images_existing, 'j' : images_allowed}, 
        context_instance=RequestContext(request)
    )





