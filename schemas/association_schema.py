from main import ma

class AssociationSchema(ma.Schema):
    class Meta:
        fields = ("curriculum_id", "tutorial_id")

association_schema = AssociationSchema()
associations_schema = AssociationSchema(many=True)