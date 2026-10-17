from django.db import models
from django.contrib.auth.models import AbstractUser


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    active = models.BooleanField(default=True, verbose_name="Активна")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Слаг")
    logo = models.ImageField(upload_to="brands/logos/", blank=True, null=True, verbose_name="Логотип")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    crated = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"

    def __str__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название филиала")

    class Meta:
        verbose_name = "Филиал"
        verbose_name_plural = "Филиалы"

    def __str__(self):
        return self.name


class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


class Item(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="items", verbose_name="Категория")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="items", verbose_name="Филиал")
    desc = models.TextField(blank=True, null=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name="Скидка")
    crated_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses", verbose_name="Пользователь")
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.TextField(verbose_name="Адрес")
    city = models.CharField(max_length=100, verbose_name="Город")
    region = models.CharField(max_length=100, verbose_name="Регион")
    postal_code = models.CharField(max_length=20, verbose_name="Почтовый индекс")
    is_default = models.BooleanField(default=False, verbose_name="Основной адрес")
    crated_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"

    def __str__(self):
        return f"{self.city}, {self.address} ({self.full_name})"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders", verbose_name="Пользователь")
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, verbose_name="Адрес доставки")
    status = models.CharField(max_length=50, default="pending", verbose_name="Статус заказа")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая сумма")
    payment_method = models.CharField(max_length=50, verbose_name="Способ оплаты")
    payment_status = models.CharField(max_length=50, default="unpaid", verbose_name="Статус оплаты")
    crated_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ №{self.id} от {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", verbose_name="Заказ")
    product = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="order_items", verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name="Скидка")
    crated_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Элемент заказа"
        verbose_name_plural = "Элементы заказа"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart", verbose_name="Пользователь")
    crated_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items", verbose_name="Корзина")
    product = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="cart_items", verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    crated_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews", verbose_name="Пользователь")
    product = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="reviews", verbose_name="Товар")
    rating = models.PositiveIntegerField(verbose_name="Рейтинг")
    comment = models.TextField(verbose_name="Комментарий")
    crated_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"Отзыв от {self.user.username} на {self.product.name}"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist", verbose_name="Пользователь")
    product = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="wishlisted_by", verbose_name="Товар")
    crated_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"

    def __str__(self):
        return f"{self.user.username} -> {self.product.name}"
