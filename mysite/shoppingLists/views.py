from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect

from .models import Item

def index(request):
    item_list = Item.objects.all()
    template = loader.get_template('shoppingLists/index.html')
    context = {
        'item_list': item_list,
    }

    if request.method == 'POST':
        newItemName = request.POST.get('name')
        if newItemName:
            newItem = Item.objects.create(name = newItemName)
            newItem.save()
            return redirect('index')

        editedItemNames = request.POST.getlist('edit-name')
        for idx, editedItem in enumerate(Item.objects.all()):
            editedItem.name = editedItemNames[idx]
            editedItem.save()

        purchasedItemIds = request.POST.getlist('purchased')
        for item in Item.objects.all():
            if str(item.id) in purchasedItemIds:
                item.purchased = True
            else:
                item.purchased = False
            item.save()

        deletingItemIds = request.POST.getlist('deleting')
        for deletingItemId in deletingItemIds:
            Item.objects.get(id=deletingItemId).delete()

        return redirect('index')

    return HttpResponse(template.render(context, request))