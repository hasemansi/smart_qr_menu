from rest_framework import serializers
from .models import Restaurant, Category, MenuItem
import socket
import requests

class RestaurantSerializer(serializers.ModelSerializer):
    qr_url = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'logo', 'theme_color', 'address', 'qr_code', 'qr_url']

    def get_qr_url(self, obj):
        """
        Returns the full restaurant API URL using ngrok or local IP
        """
        # Try to get the ngrok public URL
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

        # Fallback to local IP if ngrok not running
        if not public_url:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                local_ip = s.getsockname()[0]
                s.close()
                public_url = f"http://{local_ip}:8000"
            except Exception:
                public_url = "http://127.0.0.1:8000"

        # Return the complete URL to access this restaurant
        return f"{public_url}/api/restaurants/{obj.id}/"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'
