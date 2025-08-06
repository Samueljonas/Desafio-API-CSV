from django.shortcuts import render
from django.core.paginator import Paginator
from .models import State, City, District, Empresa

def home(request):
    return render(request, 'home.html')

def state_list(request):
    states = State.objects.all()

    #paginate
    paginator = Paginator(states,20) #20 states for pages
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'state_list.html', {'page_obj': page_obj})

def city_list(request):
    cities = City.objects.all()

    #filter
    state_id = request.GET.get('state_id')
    if state_id:
        cities = cities.filter(state__ibge_id=state_id)

    #paginate
    paginator = Paginator(cities,50) #50 cities for page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'city_list.html', {'page_obj': page_obj, 'states':State.objects.all()})

def district_list(request):
    districts = District.objects.all()

    # filter
    state_id = request.GET.get('state_id')
    if state_id:
        districts = districts.filter(city__state__ibge_id=state_id)
    # paginate
    paginator = Paginator(districts, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Passa todos os estados para o template, para o formulário de filtro
    states = State.objects.order_by('name')

    return render(request, 'district_list.html', {
        'page_obj': page_obj,
        'states': states, # Agora passamos a lista de estados
        'selected_state_id': state_id # Para manter o estado selecionado no filtro
    })

def company_list(request):
    companies = Empresa.objects.all()

    #filter
    cnpj_search = request.GET.get('cnpj')
    if cnpj_search:
        companies = companies.filter(cnpj_basico__incontains=cnpj_search)

    #paginate
    paginator = Paginator(companies, 25) #25 companies for page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "company_list.html", {'page_obj': page_obj})
