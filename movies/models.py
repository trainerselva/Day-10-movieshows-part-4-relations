from django.db import models
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator

from django.urls import reverse

from django.utils.text import slugify

# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=70)
    code = models.CharField(max_length=2)

    def __str__(self):
        return f"{ self.name } ({ self.code })"

    class Meta:
        verbose_name_plural = "Countries"


class Address(models.Model):
    street = models.CharField(max_length=75)
    postal_code = models.CharField(max_length=6)
    city = models.CharField(max_length=50)

    def __str__(self):
        return f"{ self.street }, { self.postal_code }, { self.city }"

    class Meta:
        verbose_name_plural = "Address Entries"


class Actor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    address = models.OneToOneField(
        Address, on_delete=models.CASCADE, null=True)

    # Adding utility methods
    def full_name(self):
        return f"{ self.first_name } { self.last_name }"

    def __str__(self):
        return self.full_name()


class Movie(models.Model):
    title = models.CharField(max_length=100)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])

    # mainactor = models.CharField(max_length=50, null=True)
    # Connect Actor class through the mainactor field

    mainactor = models.ForeignKey(
        Actor, on_delete=models.CASCADE, null=True, related_name="movies")

    is_boxofficehit = models.BooleanField(default=False)

    # Adding a slug field in the model
    slug = models.SlugField(default="", blank=True, null=False, db_index=True)

    # Adding Many-to-Many field relation
    released_countries = models.ManyToManyField(Country)

    def __str__(self):
        # return f"(Title: { self.title } Rating: { self.rating })"
        # return f"{ self.title } - { self.rating }"
        stars = '*' * self.rating
        return f"{ self.title } { stars }"

    # def get_absolute_url(self):
    #     return reverse("movie-detail", args=[self.id])

    # Changing the method get_absolute_url to generate
    # url based on slug and not id

    def get_absolute_url(self):
        return reverse("movie-detail", args=[self.slug])

    # Overriding the default save method to add a
    # proper slug value to the slug field of the
    # model instance

    # Import a helper function called 'slugify'
    # for generating proper slugs

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
