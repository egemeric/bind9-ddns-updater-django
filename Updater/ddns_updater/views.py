from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.conf import settings
from .models import Domain
from .system import reload_config
from .errors import RootRecordChange, RecordNotFound
# Create your views here.
def get_record(request, domain_name):

    try:
        dom_obj = Domain.objects.get(Domain_Name=domain_name)
    except Domain.DoesNotExist:
        raise Http404("domain is not found")

    json_response = {'Client_Ip4': dom_obj.Client_Ip4,
                     'last_change': dom_obj.Last_Change.isoformat(),
                     'Client_LAN': dom_obj.Client_LAN,
                     'Client_Type': dom_obj.Client_Type,
                     }
    return JsonResponse(json_response, status=200)


@csrf_exempt
def update_record(request, domain_name):
    if request.method == 'POST':
        secret_key=request.POST.get('secret', False)
        if not secret_key:
            return HttpResponse('Not authorized', status=401)
        else:
            try:
                dom_obj=Domain.objects.get(Domain_Name=domain_name)
            except Domain.DoesNotExist:
                raise Http404("domain is not found")
            if dom_obj.Domain_Secret != secret_key:
                return HttpResponse('Not authorized', status=401)
            else:
                request_ip = request.META.get('HTTP_X_FORWARDED_FOR', '') or request.META.get('REMOTE_ADDR')
                request_ip_local = request.POST.get('Client_LAN', None)
                request_ip_client_type= request.POST.get('Client_Type', None)
                if dom_obj.Client_Ip4 == request_ip:
                    return HttpResponse("No changes",status=204)
                else:
                    dom_obj.Client_Ip4 = request_ip
                    dom_obj.Client_LAN = request_ip_local
                    dom_obj.Client_Type = request_ip_client_type
                    dom_obj.save(update_fields=['Client_Ip4', 'Client_LAN', 'Client_Type', 'Last_Change'])
                    if not settings.DEBUG:
                        reload_out = reload_config()
                        print(reload_out)
                    return HttpResponse("ok", status=200)
    else:
        return HttpResponse('Http Method is not allowed', status=405)

@csrf_exempt
def add_domain(request, domain_name):
    if request.method == 'POST':
        usr = request.POST.get('username', None)
        pwd = request.POST.get('password', None)
        if not(usr and pwd):
            return HttpResponse('Bad request', status=400)
        user = authenticate(username=usr, password=pwd)
        if user is not None:
            try:
                dom_obj=Domain(Domain_Name=domain_name)
            except:
                pass
            dom_obj.Client_Ip4 = request.META.get('HTTP_X_FORWARDED_FOR', '') or request.META.get('REMOTE_ADDR')
            dom_obj.Client_LAN = request.POST.get('Client_LAN', None)
            dom_obj.Client_Type = request.POST.get('Client_Type', None)
            dom_obj.save(add_to_config=True)
            if not settings.DEBUG:
                reload_out = reload_config()
                print(reload_out)
            return HttpResponse("ok", status=200)
        else:
            return HttpResponse('Not authorized', status=401)
    else:
        return HttpResponse('Bad request', status=400)


