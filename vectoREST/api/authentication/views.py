from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class TokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        #lifetime = datetime.timedelta(seconds=10)
        #token.payload['exp'] = datetime_to_epoch(token.current_time + lifetime)

        return token

class TokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
