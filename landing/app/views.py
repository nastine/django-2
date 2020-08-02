from collections import Counter
from django.http import Http404
from django.shortcuts import render

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    from_landing = request.GET.get('from-landing')
    counter_click[from_landing] += 1
    return render(request, 'index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    ab_test_arg = request.GET.get('ab-test-arg')
    counter_show[ab_test_arg] += 1

    if ab_test_arg == 'original':
        landing_page = 'landing.html'
    elif ab_test_arg == 'test':
        landing_page = 'landing_alternate.html'
    else:
        raise Http404()
    
    return render(request, landing_page)


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Чтобы отличить с какой версии лендинга был переход
    # проверяйте GET параметр marker который может принимать значения test и original
    # Для вывода результат передайте в следующем формате:

    return render(request, 'stats.html', context={
        'test_conversion': counter_click['test'] / counter_show['test'],
        'original_conversion': counter_click['original'] / counter_show['original'],
    })
