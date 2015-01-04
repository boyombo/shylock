#!/usr/bin/env python
from django import template
from django.template.context import Context
from django.db.models import fields

register = template.Library()

class ReportNode(template.Node):
    def __init__(self, obj_list, field_names):
        self.obj_list = template.Variable(obj_list)
        self.field_names = [name.strip() for name in field_names.split(',')] if field_names else []
    
    def render(self, context):
        qset = self.obj_list.resolve(context)
        _names = [i.name for i in qset.model._meta.local_fields if i.name != 'id']#hackish hardcoding of id
        fields = self.field_names if self.field_names else _names
        headings = map(lambda x: x.replace('_', ' ').title(), fields)
        #recursive attribute lookup/reduction to support things like sale.item.description
        data = [([reduce(lambda x,y: getattr(x,y), f.split('.'), obj) for f in fields]) for obj in qset]
        t = template.loader.get_template('simplereports/report_list.html')
        return t.render(Context({'headings': headings,'fields': fields, 'obj_list': data}, autoescape=context.autoescape))

@register.tag
def show_report(parser, token):
    contents = token.split_contents()
    if len(contents) not in (2,3):#default report does not include the field names
        raise template.TemplateSyntaxError, "%r requires two or three arguments" % token.contents.split()[0]
    obj_list = contents[1]
    if len(contents) == 3:
        field_names = contents[2]
        if not (field_names[0] == field_names[-1] and field_names[0] in ('"', "'")):
            raise template.TemplateSyntaxError, "%r tag's arguments should be in quotes" % tag_name
        field_names = field_names[1:-1]
    else:
        field_names = []
    return ReportNode(obj_list, field_names)

class GraphDataNode(template.Node):
    def __init__(self, series, dates):
        self.series_name = '%s_data' % series
        self.dates = template.Variable(dates)
        #import pdb;pdb.set_trace()
        self.series = template.Variable(series)
    
    def render(self, context):
        series = self.series.resolve(context)
        #import pdb;pdb.set_trace()
        dates = self.dates.resolve(context)
        data = map(lambda (x,y): [y.strftime('%b %d'), int(x)], zip(series, dates))
        context['sales_data'] = 'sales data you say?'
        context['sales_datas'] = str({
            'label': self.series_name,
            'data': data
        })
        return ''

@register.tag
def graph_data(parser, token):
    try:
        tag_name, series, dates = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag's arguments should be in quotes" % token.contents.split()[0]
    return GraphDataNode(series, dates)