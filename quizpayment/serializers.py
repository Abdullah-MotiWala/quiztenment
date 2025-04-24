# from rest_framework import serializers
# from .models import QuizpaymentModel

# class QuizpaymentSerializer(serializers.Serializer):

# 	# quizstart = serializers.ForeignKey(read_only=Truemany=True, )
# 	# users = serializers.ForeignKey(User, on_delete=models.CASCADE)
# 	# quizopen = serializers.ForeignKey(QuizopenModel, on_delete=models.CASCADE)
# 	# status = serializers.CharField(max_length=1055, choices= STATUS ,  default = 'UNPAID' ,   null=True, blank=True)
# 	# payment_game_status = serializers.CharField(max_length=1055, choices= PYAMENT_GAME_STATUS ,  default = 'UNPLAYED'   ,  null=True, blank=True)
# 	ip_address = serializers.CharField(max_length=1055, null=True, blank=True)
# 	# payment_type_value = serializers.CharField( default = '1' ,  max_length=1055, null=True, blank=True)



# 	def create(self, validated_data):
# 		return QuizpaymentModel.objects.create(**validated_data)
