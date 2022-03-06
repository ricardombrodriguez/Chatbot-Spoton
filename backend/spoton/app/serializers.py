from app.models import Message, Booking
from rest_framework import serializers

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id','body','is_me','tag','username','created_at')


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('id','username','flight_id','created_at')
