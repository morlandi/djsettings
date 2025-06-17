from django.http import HttpResponse


def index(request):
    from main.settings.list_main_settings import list_main_settings

    main_settings = list_main_settings()

    html = """
<style>
    table { border-collapse: collapse; }
    td { border: 1px solid #ccc; padding: 2px 4px; }
</style>
<h1>djsettings project</h1>
<h3>main settings:</h3>
"""

    html += '<table>'
    for key, value in main_settings.items():
        html += f'<tr><td>{key}</td><td>{value}</td></tr>'
    html += '</html>'

    return HttpResponse(html)
