from django.urls import path, include
from .views import BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView
from .views import BookLoanView
from .views import AboutView, OldBookListRedirectView
from .views import BookListAPIView
from .views import BookListCreateAPIView, BookDetailAPIView
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

app_name = 'books'

router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('new/', BookCreateView.as_view(), name='book_create'),
    path('<int:pk>/edit/', BookUpdateView.as_view(), name='book_update'),
    path('<int:pk>/delete/', BookDeleteView.as_view(), name='book_delete'),
    path('loan/', BookLoanView.as_view(), name='book_loan'),
    path('about/', AboutView.as_view(), name='about'),
    path('old-book-list/', OldBookListRedirectView.as_view(), name='old_book_list'),
    path('api/books/', BookListAPIView.as_view(), name='book-list-api'),
    path('api/books/', BookListCreateAPIView.as_view(), name='book-list-create'),
    path('api/books/<int:pk>/', BookDetailAPIView.as_view(), name='book-detail'),
    path('api/', include(router.urls)),
]