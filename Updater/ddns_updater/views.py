from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Domain
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
                    return HttpResponse("ok",status=200)



