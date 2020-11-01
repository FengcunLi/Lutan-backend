from rest_framework import serializers

from threads.models.thread_read import ThreadRead


class ThreadReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThreadRead
        fields = '__all__'

    def validate_reader(self, value):
        if self.context['request'].user.id != value.id:
            raise serializers.ValidationError(
                "The authenticated user and thread reader should be the same.")
        return value
