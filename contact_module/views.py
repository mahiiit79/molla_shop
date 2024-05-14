from contact_module.models import ContactUs
from django.shortcuts import render,redirect
from django.urls import reverse
from .forms import  ContactUsModelForm, ProfileForm
from django.views import View
from django.views.generic.edit import FormView,CreateView
from .models import ContactUs,UserProfile
from site_module.models import SiteSetting


class ContactUsView(CreateView):
    model = ContactUs
    form_class = ContactUsModelForm
    template_name = 'contact_module/contact_us_page.html'
    success_url = '/contact-us/'
    #'inja dg khodsh save mikone'
    # 'html be jaye contact_form mishe form'

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        setting : SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
        context['site_setting'] = setting
        return context



#
# class ContactUsView(FormView):
#     template_name = 'contact_module/contact_us_page.html'
#     form_class = ContactUsModelForm
#     success_url = '/contact-us/'
#     #'html be jaye contact_form mishe form'
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)


# class ContactUsView(View):
#     def get(self,request):
#         contact_form = ContactUsModelForm()
#         return render(request, 'contact_module/contact_us_page.html', {
#             'contact_form': contact_form
#         })
#
#
#     def post(self,request):
#         contact_form = ContactUsModelForm(request.POST)
#         if contact_form.is_valid():
#             contact_form.save()
#             return redirect('home_page')
#         return render(request, 'contact_module/contact_us_page.html', {
#             'contact_form': contact_form
#         })



# def contact_us_page(request):
#     if request.method == 'POST':
#         #contact_form = ContactUsForm(request.POST)
#         contact_form = ContactUsModelForm(request.POST)
#         if contact_form.is_valid():
#             contact_form.save()
#             return redirect('home_page')
#     else:
#         #contact_form = ContactUsForm()
#         contact_form = ContactUsModelForm()
#
#     return render(request,'contact_module/contact_us_page.html',{
#         'contact_form' : contact_form
#     })


def store_file(file):
    with open('temp/image.jpg',"wb+") as dest :
        for chunk in file.chunks():
            dest.write(chunk)

class CreateProfileView(CreateView):
    template_name = 'contact_module/create_profile_page.html'
    model = UserProfile
    fields = '__all__'
    success_url = '/contact-us/create-profile'



# class CreateProfileView(View):
#     def get(self,request):
#         form = ProfileForm()
#         return render(request,'contact_module/create_profile_page.html',{
#             'form': form
#         })
#
#     def post(self,request):
#         submitted_form = ProfileForm(request.POST,request.FILES)
#
#         if submitted_form.is_valid():
#             #store_file(request.FILES['profile'])
#             profile = UserProfile(image=request.FILES['user_image'])
#             profile.save()
#             return redirect('/contact-us/create-profile')
#         return render(request,'contact_module/create_profile_page.html',{
#             'form' : submitted_form
#         })