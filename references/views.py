from django.views.generic import TemplateView

class WoodTypesView(TemplateView):
    template_name = 'references/wood_types.html'

class ScrewChartView(TemplateView):
    template_name = 'references/screw_chart.html'

class NominalActualView(TemplateView):
    template_name = 'references/nominal_actual.html'

class JointTypesView(TemplateView):
    template_name = 'references/joint_types.html'
