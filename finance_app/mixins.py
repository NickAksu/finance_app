from rest_framework.serializers import ModelSerializer

class SerializerMixin:
    
    serializer_class = None
    
    serializer_classes_for_actions = {}
    
    def get_serializer_class(self) -> ModelSerializer:
        return self.serializer_classes_for_actions.get(
            self.action, self.serializer_class
            )