from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Book
from .forms import BookForm
from django.db.models import Q
from .forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import StaffRequiredMixin
from django.views.generic.edit import FormView
from django.contrib import messages
from .forms import BookLoanForm
from django.views.generic import TemplateView,RedirectView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BookSerializer
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrReadOnly

class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    ordering = ['-publication_date']
    paginate_by = 10
    

class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

# 기존의 ListView와 DetailView는 그대로 둡니다.

class BookCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('books:book_list')
    login_url = '/login/'  # 로그인되지 않은 사용자를 리다이렉트할 URL

class BookUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'
    login_url = '/login/'

    def get_success_url(self):
        return reverse_lazy('books:book_detail', kwargs={'pk': self.object.pk})

class BookDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Book
    template_name = 'books/book_confirm_delete.html'
    success_url = reverse_lazy('books:book_list')
    login_url = '/login/'

class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    paginate_by = 5  # 한 페이지에 표시할 도서 수
    ordering = ['-publication_date']

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(author__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class BookLoanView(LoginRequiredMixin, FormView):
    template_name = 'books/book_loan.html'
    form_class = BookLoanForm
    success_url = reverse_lazy('books:book_list')

    def form_valid(self, form):
        # 여기서 실제 대여 로직을 구현할 수 있습니다.
        # 예를 들어, 대여 기록을 데이터베이스에 저장하는 등의 작업
        book = form.cleaned_data['book']
        loan_date = form.cleaned_data['loan_date']
        return_date = form.cleaned_data['return_date']

        messages.success(self.request, f"{book.title}의 대여가 신청되었습니다. 대여 기간: {loan_date} - {return_date}")
        return super().form_valid(form)

class AboutView(TemplateView):
    template_name = 'books/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '도서관 소개'
        return context

class OldBookListRedirectView(RedirectView):
    url = reverse_lazy('books:book_list')
    permanent = True


class BookListAPIView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
