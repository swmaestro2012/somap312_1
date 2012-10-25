from models import Book

from django.forms import ModelForm

class BookCreationForm(ModelForm):
    class Meta:
        model = Book
        fields = ('creator', 'coverimg', 'title', 'genre', 'synopsis', )

