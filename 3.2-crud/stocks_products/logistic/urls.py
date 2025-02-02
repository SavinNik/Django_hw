from operator import index

from rest_framework.routers import DefaultRouter

from logistic.views import ProductViewSet, StockViewSet, home_view

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('stocks', StockViewSet)
router.register('home', home_view)
urlpatterns = router.urls
