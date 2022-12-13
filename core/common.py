from .models import Service,Agency
def get_agency_info(site_id):
	C=Service.objects.filter(site_id=site_id).values_list('agency',flat=True);D=None
	if C:E=Agency.objects.filter(id=C[0])[0];F=E.get_current_language();D=Agency.objects.language(F).filter(id=C[0])
	A={}
	if D:
		for B in D:A['uuid']=B.uuid;A['name']=B.name;A['email']=B.email;A['phone']=B.phone;A['fax']=B.fax;A['whatsapp']=B.whatsapp;A['address']=B.address;A['notes']=B.notes
	return A