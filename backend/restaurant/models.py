from django.db import models
from io import BytesIO
from django.core.files import File
import qrcode
import socket
import requests


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='restaurants/logos/', null=True, blank=True)
    theme_color = models.CharField(max_length=7, default='#ff0000')
    address = models.TextField()
    qr_code = models.ImageField(upload_to='restaurants/qrcodes/', null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Custom save method — always regenerates QR with current ngrok or local IP"""

        super().save(*args, **kwargs)

        # Try to detect ngrok public URL
        try:
            response = requests.get("http://127.0.0.1:4040/api/tunnels")
            data = response.json()
            tunnels = data.get("tunnels", [])
            public_url = None
            for tunnel in tunnels:
                if tunnel.get("proto") == "https":
                    public_url = tunnel.get("public_url")
                    break
        except Exception:
            public_url = None

        # If ngrok URL is not found, fallback to local IP
        if not public_url:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                local_ip = s.getsockname()[0]
                s.close()
                public_url = f"http://{local_ip}:8000"
            except Exception:
                public_url = "http://127.0.0.1:8000"

        # Create full restaurant URL
        qr_data = f"{public_url}/api/restaurants/{self.id}/"

        # Generate QR code
        qr = qrcode.make(qr_data)
        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        filename = f"{self.name}_qr.png"

        # Save QR code image to model field
        self.qr_code.save(filename, File(buffer), save=False)

        # Save changes
        super().save(update_fields=['qr_code'])


class Category(models.Model):
    name = models.CharField(max_length=50)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(upload_to='menu_items/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
