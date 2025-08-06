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

    # Filtragem
    state_id = request.GET.get('state_id')
    if state_id:
        cities = cities.filter(state__ibge_id=state_id)
        
    # Paginação
    paginator = Paginator(cities, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Adiciona a ordenação alfabética dos estados
    states = State.objects.order_by('name')
    
    return render(request, 'city_list.html', {'page_obj': page_obj, 'states': states})

def district_list(request):
    districts = District.objects.all()

    # Adiciona a lógica de filtro por estado
    state_id = request.GET.get('state_id')
    if state_id:
        districts = districts.filter(city__state__ibge_id=state_id)
        
    # Paginação
    paginator = Paginator(districts, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Adiciona a ordenação alfabética dos estados
    states = State.objects.order_by('name')
    
    return render(request, 'district_list.html', {
        'page_obj': page_obj,
        'states': states,
        'selected_state_id': state_id
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
