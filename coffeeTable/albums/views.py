from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import logout_then_login
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext

from albums.models import *



def index (request):
    """ New user is directed to Welcome page
        Authenticated user views a home page with his albums
            returns a list of album titles and thumbnails
    """
    if not request.user.is_authenticated():
        #return render_to_response('login.html',{'is_auth':False})
        #return render_to_response('welcome.html',{'is_auth':False})
        return HttpResponseRedirect(reverse(login_django))#show Django login with other options

    album_list = Album.objects.all().order_by('-date_created')
    
    # Check for a currently unsaved album
    if Album.objects.filter(title="temp"):
        working_album = True
    else:
        working_album = False
        
    return render_to_response('albums.html', {'album_list': album_list, 
        'working_album': working_album})
    

def initiate_album (request, album_id=0):
    
    if album_id != 0 or request.POST:
        return edit_album(request, album_id)
    
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
        no_of_pages = Album.number_of_pages(a)
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
    
def album_has_next_page (a, p):
    pages_in_album = Album.number_of_pages(a)
    if pages_in_album > p.number:
        return True
    else:
        return False

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
    
    # Check if next page exists
    next_page = album_has_next_page(a, p)
    
    if images_existing >= 1:
        i_list = Image.objects.filter(page=p).order_by('number')
    else:
        i_list = {}
    
    template_name = template + '.html'
    
    print_view = False
    
    # Render all details to the template
    return render_to_response( 
        template_name, 
        {'a' : a, 'p' : p, 'i_list' : i_list, 
        'next_page' : next_page, 'j' : images_allowed, 
        'print_view' : print_view}, 
        context_instance=RequestContext(request)
    )


@login_required
def require_authentication(request):
    return HttpResponse('This page requires authentication')


def sign_up(request):
    #user sent a form with data
    if request.method == 'POST':
        form = UserCreationForm(data = request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data['username'],
					password=form.cleaned_data['password1'])
            #user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))#go to the main page
    #user visited the page first time
    form = UserCreationForm()
    return render_to_response('registration.html',{'form':form},context_instance=RequestContext(request))


@login_required
def logout(request, **kwargs):
	return logout_then_login(request)

#log in with a django account
def login_django(request):
    user = None
    #user sent a form with data
    if request.method == 'POST':
        authForm = AuthenticationForm(data=request.POST)
        if authForm.is_valid():
            user = authenticate(username=authForm.cleaned_data['username'],
					password=authForm.cleaned_data['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))#go to the main page
    #user visited the page first time
    return render_to_response("welcome.html",{'form':AuthenticationForm(),'is_auth':False},context_instance=RequestContext(request))


def save_album (request, album_id=0, tried_to_edit=False):
    
    a = Album.objects.get(title="temp")
    
    # If title was submitted, check and save name
    if request.POST:
        
        # TO-DO: Check that title is not empty
        
        a.title = request.POST.get('title')
        
        # Get first image of first page and assign as thumbnail
        p_list = Page.objects.filter(album=a).order_by('number')
        i_list = Image.objects.filter(page=p_list[0]).order_by('number')
        
        if len(i_list) < 1:
            a.save()
        else:
            a.thumbnail = i_list[0]
            a.save()
        
        if request.POST.get('tried_to_edit'):
            return initiate_album(request, album_id)
        else:
            return index(request)
       
    return render_to_response("save_album.html", {'a' : a,
        'tried_to_edit' : tried_to_edit}, 
        context_instance=RequestContext(request))



def edit_album (request, album_id):
    
    a = Album.objects.get(id=album_id)
    
    # Can't have two working albums, save existing temp album
    if Album.objects.filter(title="temp"):
        tried_to_edit = True
        return save_album(request, album_id, tried_to_edit)
    else:
        a.temp_title = a.title
        a.title = "temp"
        a.save
    
    return initiate_album(request, album_id)
    
        
def view_album (request, album_id, page_no="1"):
    
    a = Album.objects.get(id=album_id)
    p = Page.objects.get(album=a, number=page_no)
    
    template_name = p.template + '.html'
    
    i_list = Image.objects.filter(page=p).order_by('number')
    
    # Check if next page exists
    next_page = album_has_next_page(a, p)
    
    print_view = True

    # render dynamic request url for facebook like button
    album_url = 'http://group021.webcourse.niksula.hut.fi/albums/' + album_id + '/'
    
    return render_to_response( 
        template_name, 
        {'a' : a, 'p' : p, 'i_list' : i_list, 
        'next_page' : next_page, 'print_view' : print_view, 'album_url' : album_url},
        context_instance=RequestContext(request)
    )
    
    
    


