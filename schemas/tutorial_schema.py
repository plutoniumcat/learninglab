from main import ma

class TutorialSchema(ma.Schema):
    class Meta:
        fields = ("id", "url", "user_id", "title", "author", "description", "level", "prerequisites", "pricing", "length")

tutorial_schema = TutorialSchema()
tutorials_schema = TutorialSchema(many=True)