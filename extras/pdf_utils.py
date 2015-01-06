from django.template.loader import get_template
from django.http import HttpResponse
import ho.pisa as pisa
from django.conf import settings

def render_to_pdf(context, filename, template_name):
	response = HttpResponse(mimetype='application/pdf')
	response['Content-Disposition'] = 'attachment;filename=%s' % filename
	t = get_template(template_name)
	context.update({
		'company_name': settings.COMPANY_NAME,
		'company_address': settings.COMPANY_ADDRESS,
		'company_phones': settings.COMPANY_PHONE_NUMBERS,
		'company_slogan': settings.COMPANY_SLOGAN
		})
	html = t.render(context)
	pdf = pisa.CreatePDF(html, response)
	if not pdf.err:
		return response
	return HttpResponse('There are some errors<pre>%s</pre>' % pdf.err)