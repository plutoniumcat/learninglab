from main import ma

class CurriculumSchema(ma.Schema):
    class Meta:
        fields = ("id", "user_id", "title", "description")

curriculum_schema = CurriculumSchema()
curriculums_schema = CurriculumSchema(many=True)