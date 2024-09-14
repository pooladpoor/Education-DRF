from rest_framework import serializers
from .models import Todo
from django.contrib.auth import get_user_model


User = get_user_model()

# همه چیش مثل فرم ها توی خود جنگو هست
class TodoSerializer(serializers.ModelSerializer):
    
    # اعتبار سنجی برای هر فیلد خواص
    def validate_priority(self, priority):
        if priority < 10 or priority > 20:
            raise serializers.ValidationError('priority is not ok')
        return priority
    
    #  اینجا به همه فیلد ها دسرسی داری و میشه اعتبار سنجی کرد
    # def validate(self, attrs):
    #     print(attrs)
    #     return super().validate(attrs)
    
    # مثل مودل فرم_____
    class Meta:
        model = Todo
        fields = '__all__'



class UserSerialzier(serializers.ModelSerializer):
    # برای اون فیلدی که ریلیتد نیم هست (فارنکی خوده)
    # باید اینجوری سریالایزش رو بدی که بتونه تو جیسان این, لیست اونا رو نشون بده
    todos = TodoSerializer(read_only=True, many=True)
    # ریلیتد نیم توی مدل تودو         ^^^^
    
    class Meta:
        model = User
        fields = '__all__'