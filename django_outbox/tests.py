from django.test import SimpleTestCase
from django.urls import reverse
from datetime import datetime,timedelta
from django_outbox.common import get_natural_datetime
class HomepageTests(SimpleTestCase):
	def test_url_exists_at_correct_location(D):
		A=datetime.now();print('tgl posting = ',A)
		for B in range(0,70):C=A-timedelta(days=B);print(B,' ',C,' ---- ',get_natural_datetime(C,A))