from main import ma

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "email", "password", "profile", "admin")

user_schema = UserSchema()
users_schema = UserSchema(many=True)