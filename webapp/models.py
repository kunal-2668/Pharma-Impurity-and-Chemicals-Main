from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.utils.translation import gettext_lazy as _
from autoslug import AutoSlugField
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = models.CharField(max_length=255,null=True)
    email = models.EmailField(_('email address'), unique=True)
    mobile = PhoneNumberField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Product_Category(models.Model):
    Category_name = models.CharField(max_length=255,verbose_name='Category Name')
    category_slug = AutoSlugField(populate_from='Category_name',unique=True)

    def __str__(self):
        return self.Category_name


class Impurity_Chemicals(models.Model):
    category = models.ForeignKey(Product_Category,on_delete=models.CASCADE)
    product_name = models.CharField(max_length=300,verbose_name="Product Name",unique=True)
    product_image = models.ImageField(upload_to="images",null=True,blank=True)
    cat_no = models.CharField(max_length=300,verbose_name="Cat No." ,default="N.A.")
    chemical_name = models.CharField(max_length=300,verbose_name="Chemical Name" ,default="N.A.")
    molecular_formula = models.CharField(max_length=300,verbose_name='Molecular Formula' ,default="N.A.")
    molecular_weight = models.CharField(max_length=100,verbose_name='Molecular Weight',null=True)
    cas_number = models.CharField(max_length=300,verbose_name='CAS Number')
    solubility = models.CharField(max_length=300,verbose_name='Solubility' ,default="N.A.")
    storage = models.CharField(max_length=300,verbose_name='Storage' ,default="N.A.")
    keywords = models.CharField(max_length=300,verbose_name='Keywords' ,default="N.A.")
    purity_by_HPLC = models.CharField(max_length=100,verbose_name='Purity by HPLC',null=True)
    slug_id = AutoSlugField(populate_from='product_name',unique=True)
    inventory_status = models.CharField(max_length=50,default="In Stock")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name


class Contact_Us(models.Model):
    name = models.CharField(max_length=255,verbose_name="Name")
    email = models.EmailField(verbose_name="Email")
    phone_no = PhoneNumberField(verbose_name="Phone No.")
    message = models.TextField(verbose_name='Message')

    def __str__(self):
        return f"{self.name},{self.email}"


class Get_online_quote(models.Model):
    full_name = models.CharField(max_length=255,verbose_name="Full Name")
    email_id = models.EmailField(verbose_name="Email ID")
    company_name = models.CharField(max_length=300,verbose_name="Company Name")
    contact_no = PhoneNumberField(verbose_name="Contact No")
    product_name = models.CharField(max_length=300,verbose_name="Product Name")
    chemical_name = models.CharField(max_length=300,verbose_name="Chemical Name")
    cas_number = models.CharField(max_length=300,verbose_name='CAS No.')
    structure = models.ImageField(upload_to="online_quote",null=True,blank=True)
    quantity = models.CharField(max_length=60,verbose_name="Quantity")
    generated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name},{self.product_name}"
    

class RFQ_list(models.Model):
    product_name = models.CharField(max_length=255)
    quantity = models.CharField(max_length=222,default=1)
    ordered_by = models.ForeignKey(User,on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return f"{self.product_name},{self.ordered_by}"