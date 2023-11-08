from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


def product_directory_path(instance, filename):
    return f"products/{instance.name}/{filename}"


class Role(models.Model):
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.role


def user_directory_path(instance, filename):
    return f"profile-images/{instance.user.username}/{filename}"


class CustomUser(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    profile_image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username


def product_directory_path(instance, filename):
    return f"products/{instance.name}/{filename}"


class Product(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to=product_directory_path, null=True, blank=True)
    artist = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    price = models.FloatField()
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Reviews(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.content


class PaymentMethod(models.Model):
    card_owner = models.CharField(max_length=255)
    card_number = models.IntegerField()
    expiry_date = models.DateField
    cvv = models.CharField(max_length=3)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_ordered = models.BooleanField(default=False)

    def total_price(self):
        cart_items = self.cartitem_set.all()
        total = sum(item.product.price * item.quantity for item in cart_items)
        return total


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.product.price * self.quantity


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.pk} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Order Item {self.pk} - {self.order}"


class Discount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    number_of_products = models.PositiveIntegerField(default=4)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.05)

    def total_discount(self, cart):
        eligible_products = cart.cartitem_set.filter(product=self.product)
        total_quantity = sum(item.quantity for item in eligible_products)

        if total_quantity >= self.number_of_products:
            return total_quantity * self.product.price * self.discount_percentage
        else:
            return 0
