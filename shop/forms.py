from django import forms

from shop.models import Category, Product


class CreateProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['category', 'name', 'icon', 'description', 'price']
        labels = {
            'category': 'Категория',
            'name': 'Название товара',
        }
        help_texts = {
            'category': 'Товар должен относиться к одной из категории',
            'icon': 'Изображение товара способствует лучшим продажам',
            'description': 'Детально опишите товар',
            'price': 'Стоимость товара не должна превышать 100 кредитов'
        }

    def clean(self):
        category = self.cleaned_data.get('category')
        name = self.cleaned_data.get('name')
        price = self.cleaned_data.get('price')
        if not Category.objects.filter(name=category).exists():
            raise forms.ValidationError('Товар должен относиться к одной из имеющихся категорий')
        if Product.objects.filter(name=name).exists():
            raise forms.ValidationError('Товар с таким название уже размещен на торговой площадке')
        if price > 100.0:
            raise forms.ValidationError('Товар не может стоить больше 100 кредитов')
