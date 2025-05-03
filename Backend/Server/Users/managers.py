from django.contrib.auth.models import BaseUserManager




class UserManager(BaseUserManager):

    def create_user(self, phone, username, email, user_type, full_name, password=None, **extra_fields):
        
        if not email:
            raise ValueError("ایمیل باید وارد شود")
        if not username:
            raise ValueError("نام کاربری باید وارد شود")        
        if not phone:
            raise ValueError("شماره تلفن باید وارد شود")

        email = self.normalize_email(email)

        user = self.model(
            phone=phone, 
            username=username,
            email=email, 
            user_type=user_type,
            full_name=full_name,
            **extra_fields
        )

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, phone, username, email, full_name, password=None, **extra_fields):

        user = self.create_user(
            phone=phone,
            username=username,
            email=self.normalize_email(email),
            full_name=full_name,
            password=password,
            user_type="AD"
        )

        user.is_admin = True

        user.is_superuser = True

        user.save(using=self._db)
        return user
