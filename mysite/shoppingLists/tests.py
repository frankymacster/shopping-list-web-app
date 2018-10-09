from django.test import TestCase
from django.urls import reverse

from .models import Item

def create_item(name):
    """
    Create an item with the given `name`.
    """
    return Item.objects.create(name=name)

class ItemIndexViewTests(TestCase):
    def test_no_items(self):
        """
        If no items exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No items are available.")
        self.assertQuerysetEqual(
            response.context['item_list'],
            []
        )
    
    def test_add_item(self):
        create_item(name="onion")
        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(
            response.context['item_list'],
            ['<Item: onion>']
        )

    def test_delete_item(self):
        newItem = create_item(name="onion")
        response = self.client.get(reverse('index'))
        deletedItem = Item.objects.filter(id = newItem.id)
        deletedItem.delete()
        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(
            response.context['item_list'],
            []
        )
