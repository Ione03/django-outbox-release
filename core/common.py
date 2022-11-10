from .models import Service,Agency
def get_agency_info(site_id):
	D=Service.objects.filter(site_id=site_id).values_list('agency',flat=True);C=None
	if D:C=Agency.objects.filter(id=D[0])
	A={}
	if C:
		for B in C:A['email']=B.email;A['phone']=B.phone;A['fax']=B.fax;A['whatsapp']=B.whatsapp
	return A