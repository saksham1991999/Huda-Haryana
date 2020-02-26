from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout

from . import models, forms


def SignupView(request):
    logout(request)
    if request.method=='POST':
        form = forms.SingupForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            firstname = form.cleaned_data['first_name']
            lastname = form.cleaned_data['last_name']
            mobile = form.cleaned_data['mobile']
            profile_pic = form.cleaned_data['profile_pic']
            user = models.User.objects.create_user(username=username.lower(), email=email,password=password,
                                            first_name=firstname, mobile=mobile, profile_pic=profile_pic,
                                            last_name=lastname)
            user.save()
            user = authenticate(request, username=username.lower(), password=password)
            messages.success(request, 'Thanks for registering {}'.format(user.first_name))
            return redirect('core:home')
        else:
            form = forms.SingupForm(request.POST, request.FILES)
            messages.error(request, form.errors)
    else:
        form = forms.SingupForm()
    return render(request, 'account/signup.html', {'form': form})


def HomeView(request):
    properties = models.property.objects.all()[:4]

    if request.method == 'POST':
        form = forms.EnquiryForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.save()
            messages.success(
                request,
                'Enquiry sent Successfully',
                extra_tags='alert alert-success alert-dismissible fade show'
            )
            return redirect('core:home')
        else:
            return redirect('core:home')

    form = forms.MainEnquiryForm()
    context = {
        'properties': properties,
        'form':form,
    }
    return render(request, 'index.html', context)


def PropertiesView(request):
    allProperties = models.property.objects.all()
    search_term = ''
    city = ''

    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        allProperties = allProperties.filter(bedrooms=bedrooms)

    if 'search' in request.GET:
        search_term = request.GET['search']
        allProperties = allProperties.filter(property_name__icontains= search_term, additional_features__icontains=search_term)

    if 'city' in request.GET:
        city = request.GET['city']
        allProperties = allProperties.filter(city__icontains=city)

    paginator = Paginator(allProperties, 25)
    page = request.GET.get('page')
    allProperties = paginator.get_page(page)

    get_dict_copy = request.GET.copy()
    params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()
    context = {
        'properties': allProperties,
        'params': params,
        'search_term': search_term,
        'city': city,
    }
    return render(request, 'properties.html', context)

def AgentsView(request):
    properties = models.property.objects.all()[:4]
    agents = models.agent.objects.all()[:4]
    context = {
        'properties': properties,
        'agents': agents,
    }
    return render(request, 'agents.html', context)

def ContactView(request):
    if request.method == 'POST':
        form = forms.contactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Message sent Successfully',
                extra_tags='alert alert-success alert-dismissible fade show'
            )
            print('_______________________FORM WAS VALID _____________________')
            return redirect('core:home')
        else:
            print(form.errors)
            print('_______________________FORM WAS INVALID _____________________')
            return redirect('core:contact')
    else:
        form = forms.contactForm
        context = {
            'form':form,
        }
        return render(request, 'contact.html', context)

def PropertyView(request, id):
    property = get_object_or_404(models.property, id = id)
    property.views = int(property.views+1)
    property.save()

    if request.method == 'POST':
        form = forms.EnquiryForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.property = property
            new_form.save()
            messages.success(
                request,
                'Enquiry sent Successfully',
                extra_tags='alert alert-success alert-dismissible fade show'
            )
            return redirect('core:property', id)
        else:

            return redirect('core:property', id)
    else:
        enquiryform = forms.EnquiryForm()
        context = {
            'property': property,
            'enquiryform': enquiryform,
        }
        return render(request, 'property.html', context)

@login_required
def UserProfileView(request):
    if request.method == "POST":
        form = forms.UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Changes Saved Successfully',
                extra_tags='alert alert-success alert-dismissible fade show'
            )
        return redirect('core:userprofile')
    else:
        form = forms.UserProfileForm(instance=request.user)
        context = {
            'form': form,
        }
        return render(request, 'dashboard/userprofile.html', context)

@login_required
def myProperties(request):
    properties = models.property.objects.filter(owner = request.user)
    context = {
        'properties': properties,
    }
    return render(request, 'dashboard/myproperties.html', context)

@login_required
def editProperty(request, id):
    property = get_object_or_404(models.property, id=id)
    if property.owner == request.user:
        if request.method == 'POST':
            form = forms.propertyForm(request.POST, instance=property)
            if form.is_valid():
                form.save()
                messages.success(
                    request,
                    'Property Details Saved Successfully',
                    extra_tags='alert alert-success alert-dismissible fade show'
                )
                return redirect('core:myproperties')
            else:
                return redirect('core:myproperties')
        else:
            form = forms.propertyForm(instance=property)
            context = {
                'form': form,
            }
            return render(request, 'dashboard/addproperty.html', context)
    else:
        messages.success(
            request,
            'You are not allowed to edit the Property Details',
            extra_tags='alert alert-success alert-dismissible fade show'
        )
        return redirect('core:myproperties')

@login_required
def addProperty(request):
    if request.method == "POST":
        form = forms.propertyForm(request.POST, request.FILES)

        imagesform = forms.ImagesForm(request.POST, request.FILES)
        uploadedimages = request.FILES.getlist('image')

        if form.is_valid():
            new_form = form.save(commit = False)
            new_form.owner = request.user
            new_form.save()

            if imagesform.is_valid():
                for image in uploadedimages:
                    imageinput = models.images(property=new_form, image = image)
                    imageinput.save()

            messages.success(
                            request,
                            'Property Added Successfully',
                            extra_tags='alert alert-success alert-dismissible fade show'
                            )
            return redirect('core:myproperties')
    else:
        form = forms.propertyForm()
        imagesform = forms.ImagesForm()
        context = {
            'form': form,
            'imagesform': imagesform,
        }
        return render(request, 'dashboard/addproperty.html', context)

@login_required
def deleteProperty(request, id):

    property = get_object_or_404(models.property, id = id )
    if property.owner == request.user:
        property.delete()
        messages.success(
            request,
            'Property Deleted Successfully',
            extra_tags='alert alert-success alert-dismissible fade show'
        )
    else:
        messages.error(
            request,
            'You can not delete the property',
            extra_tags='alert alert-danger alert-dismissible fade show'
        )
    return redirect('core:myproperties')

@login_required
def hideProperty(request, id):
    property = get_object_or_404(models.property, id=id)
    if property.owner == request.user:
        property.visible = False
        property.save()
    return redirect('core:myproperties')

@login_required
def showProperty(request, id):
    property = get_object_or_404(models.property, id=id)
    if property.owner == request.user:
        property.visible = True
        property.save()
    return redirect('core:myproperties')

@login_required
def BookmarkView(request):
    bookmarks = models.bookmark.objects.filter(user=request.user).first()
    context = {
        'bookmark': bookmarks,
    }
    return render(request, 'dashboard/bookmarks.html', context)

@login_required
def add_to_bookmark(request, id):
    property = get_object_or_404(models.property, id = id)
    bookmark_qs = models.bookmark.objects.filter(user = request.user)
    if bookmark_qs.exists():
        bookmark = bookmark_qs[0]
        if bookmark.properties.filter(id = id).exists():
            messages.info(request, "Property Already Bookmarked")
        else:
            bookmark.properties.add(property)
            messages.info(request, "Successfully Bookmarked")
    else:
        bookmark = models.bookmark.objects.create(user=request.user)
        bookmark.properties.add(property)
        messages.info(request, "Successfully Bookmarked")
    return redirect("core:bookmarks")

@login_required
def remove_from_bookmark(request, id):
    property = get_object_or_404(models.property, id = id)
    bookmark_qs = models.bookmark.objects.filter(user = request.user)
    if bookmark_qs.exists():
        bookmark = bookmark_qs[0]
        if bookmark.properties.filter(id = id).exists():
            bookmark.properties.remove(property)
            messages.info(request, "Property removed from your Bookmarks")
    else:
        messages.info(request, "Property does not exist in your Bookmarks")
    return redirect("core:bookmarks")

@login_required
def ComparisonView(request):
    print("Comparison view")

    compare_qs = models.Compare.objects.filter(user=request.user)
    print(compare_qs)

    if compare_qs.exists():
        compare_qs = compare_qs[0]
        properties = compare_qs.properties.all()
        print(properties)
        if len(properties) > 1:
            property1 = None
            property2 = None
            property3 = None
            try:
                property1 = properties[0]
            except:
                pass
            try:
                property2 = properties[1]
            except:
                pass
            try:
                property3 = properties[2]
            except:
                pass

            print("ready to open compare list")
            features = models.features.objects.all()
            context = {
                'properties': properties,
                'property1':property1,
                'property2':property2,
                'property3':property3,
                'features':features,
            }

            return render(request, 'dashboard/compareproperties.html', context)
        else:
            messages.info(request, "You just have 1 property to compare")
            return redirect('core:properties')
    else:

        messages.info(request, "Add to Properties to Compare list to compare")
        return redirect('core:properties')

@login_required
def add_to_compare(request, id):
    property = get_object_or_404(models.property, id = id)
    compare_qs = models.Compare.objects.filter(user = request.user)
    if compare_qs.exists():
        compare = compare_qs[0]
        if compare.properties.filter(id = id).exists():
            messages.info(request, "Property Already Added to Compare List")
        else:
            compare.properties.add(property)
            messages.info(request, "Successfully Added to Compare")
    else:
        compare = models.Compare.objects.create(user=request.user)
        compare.properties.add(property)
        messages.info(request, "Successfully Added to Compare")
    return redirect("core:compare")

@login_required
def remove_from_compare(request, id):
    property = get_object_or_404(models.property, id = id)
    compare_qs = models.Compare.objects.filter(user = request.user)
    if compare_qs.exists():
        compare = compare_qs[0]
        if compare.properties.filter(id = id).exists():
            compare.properties.remove(property)
            messages.info(request, "Property removed from your Compare List")
    else:
        messages.info(request, "Property does not exist in your Compare List")
    return redirect("core:compare")
