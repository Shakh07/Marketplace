from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from rest_framework import generics, permissions, filters
from rest_framework.pagination import PageNumberPagination
from .models import Category, Brand, Product, Tag, ProductQuestion, Wishlist
from .serializers import (
    CategorySerializer, BrandSerializer, ProductListSerializer,
    ProductDetailSerializer, TagSerializer, ProductQuestionSerializer, WishlistSerializer
)


# ═══════════════════════════════════════
# API Views
# ═══════════════════════════════════════

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.filter(is_active=True, parent_category__isnull=True)
    serializer_class = CategorySerializer


class BrandListAPIView(generics.ListAPIView):
    queryset = Brand.objects.filter(is_active=True)
    serializer_class = BrandSerializer


class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductListSerializer

    def get_queryset(self):
        qs = Product.objects.filter(product_status='active')
        category = self.request.query_params.get('category')
        brand = self.request.query_params.get('brand')
        search = self.request.query_params.get('search')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        featured = self.request.query_params.get('featured')

        if category:
            qs = qs.filter(category__slug=category)
        if brand:
            qs = qs.filter(brand__id=brand)
        if search:
            qs = qs.filter(Q(product_name__icontains=search) | Q(description__icontains=search))
        if min_price:
            qs = qs.filter(base_price__gte=min_price)
        if max_price:
            qs = qs.filter(base_price__lte=max_price)
        if featured:
            qs = qs.filter(is_featured=True)

        return qs


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'


class WishlistListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WishlistDeleteAPIView(generics.DestroyAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)


# ═══════════════════════════════════════
# Template Views
# ═══════════════════════════════════════

def home_view(request):
    from .models import HeroSection
    hero = HeroSection.get_instance()
    featured_products = Product.objects.filter(product_status='active', is_featured=True)[:8]
    categories = Category.objects.filter(is_active=True, parent_category__isnull=True)[:8]
    latest_products = Product.objects.filter(product_status='active').order_by('-created_at')[:8]
    brands = Brand.objects.filter(is_active=True)[:12]
    return render(request, 'home.html', {
        'hero': hero,
        'featured_products': featured_products,
        'categories': categories,
        'latest_products': latest_products,
        'brands': brands,
    })


def product_list_view(request):
    products = Product.objects.filter(product_status='active')

    # Filters
    search_q      = request.GET.get('q')
    category_slug = request.GET.get('category')
    sort          = request.GET.get('sort', '-created_at')
    min_price     = request.GET.get('min_price')
    max_price     = request.GET.get('max_price')
    in_stock      = request.GET.get('in_stock')

    # Category filter
    current_category = None
    if category_slug:
        try:
            current_category = Category.objects.get(slug=category_slug, is_active=True)
            # Include products from this category AND its subcategories
            descendant_ids = [current_category.id]
            children = Category.objects.filter(parent_category=current_category, is_active=True)
            for child in children:
                descendant_ids.append(child.id)
                grandchildren = Category.objects.filter(parent_category=child, is_active=True)
                descendant_ids.extend(grandchildren.values_list('id', flat=True))
            products = products.filter(category__id__in=descendant_ids)
        except Category.DoesNotExist:
            pass

    if search_q:
        products = products.filter(
            Q(product_name__icontains=search_q) |
            Q(description__icontains=search_q)
        ).distinct()
    from django.db.models import Min, Max
    
    products_before_price = products # capture base before price filtering

    if min_price:
        try: products = products.filter(base_price__gte=float(min_price))
        except ValueError: pass
    if max_price:
        try: products = products.filter(base_price__lte=float(max_price))
        except ValueError: pass
    if in_stock == '1':
        try:
            products = products.filter(inventory__quantity_available__gt=0).distinct()
        except Exception:
            pass  # skip if inventory table is empty/missing

    allowed_sorts = ['base_price', '-base_price', '-created_at', '-average_rating', '-total_sales']
    if sort in allowed_sorts:
        products = products.order_by(sort)

    # Price bounds for slider (based on current filters, before price filters)
    price_bounds = products_before_price.aggregate(lo=Min('base_price'), hi=Max('base_price'))
    price_lo = int(price_bounds['lo'] or 0)
    price_hi = int(price_bounds['hi'] or 0)

    # Build cart map
    cart_qtys = {}
    if request.user.is_authenticated:
        from apps.orders.models import ShoppingCart
        for ci in ShoppingCart.objects.filter(user=request.user).values('product_id', 'quantity', 'id'):
            cart_qtys[ci['product_id']] = {'qty': ci['quantity'], 'item_id': ci['id']}

    all_categories = Category.objects.filter(is_active=True, parent_category__isnull=True)

    return render(request, 'catalog/product_list.html', {
        'products': products,
        'search_q': search_q or '',
        'current_sort': sort,
        'current_min_price': min_price or '',
        'current_max_price': max_price or '',
        'current_in_stock': in_stock or '',
        'current_category': current_category,
        'category_slug': category_slug or '',
        'all_categories': all_categories,
        'price_lo': price_lo,
        'price_hi': price_hi,
        'cart_qtys': cart_qtys,
        'cart_total_items': sum(v['qty'] for v in cart_qtys.values()),
    })


def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(
        category=product.category, product_status='active'
    ).exclude(id=product.id)[:4]
    reviews = product.reviews.filter(is_approved=True).order_by('-created_at')

    # Check cart status
    cart_item = None
    cart_total_items = 0
    if request.user.is_authenticated:
        from apps.orders.models import ShoppingCart
        cart_item = ShoppingCart.objects.filter(user=request.user, product=product).first()
        cart_total_items = ShoppingCart.objects.filter(user=request.user).count()

    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'cart_item': cart_item,
        'cart_total_items': cart_total_items,
    }
    return render(request, 'catalog/product_detail.html', context)


from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from apps.reviews.models import Review

@login_required
def submit_review_view(request, slug):
    if request.method == 'POST':
        product = get_object_or_404(Product, slug=slug)
        rating_val = request.POST.get('rating')
        comment_val = request.POST.get('comment', '')

        # Basic validation
        if not rating_val:
            messages.error(request, "Iltimos, yulduzchalar orqali baholang.")
            return redirect('product_detail', slug=slug)

        try:
            rating_val = int(rating_val)
        except ValueError:
            rating_val = 5

        # Create or update review
        # In this simplistic setup, we will allow 1 review per user per product, or update current
        review, created = Review.objects.update_or_create(
            user=request.user,
            product=product,
            defaults={
                'rating': rating_val,
                'comment': comment_val,
                'is_approved': True  # auto-approve for demonstration
            }
        )
        
        messages.success(request, "Sharhingiz muvaffaqiyatli saqlandi!")
    return redirect('product_detail', slug=slug)

def help_page_view(request):
    """ View for displaying the global help page """
    return render(request, 'catalog/help_page.html')
