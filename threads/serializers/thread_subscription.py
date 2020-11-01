from rest_framework import serializers

from threads.models.thread_subscription import ThreadSubscription


class ThreadSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThreadSubscription
        fields = '__all__'

    def validate_subscriber(self, value):
        if self.context['request'].user.id != value.id:
            raise serializers.ValidationError(
                "The authenticated user and thread subscriber should be the same.")
        return value
