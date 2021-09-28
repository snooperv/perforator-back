from django.http import HttpResponse

def basicView(request):
    html = "<html><body>Hello!</body></html>"
    return HttpResponse(html)

#Можно вставлять и настоящие HTML-файлы, посмотрите в Django