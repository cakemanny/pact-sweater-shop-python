from rest_framework import serializers

from hatter.models import HatOrder

serializers.HyperlinkedRelatedField

class HatOrderSerializer(serializers.ModelSerializer):
    customer = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = HatOrder
        fields = ['customer', 'colour', 'material', 'order_number']

    def create(self, validated_data):
        assert 'request' in self.context, (
            "`%s` requires the request in the serializer"
            " context. Add `context={'request': request}` when instantiating "
            "the serializer." % self.__class__.__name__
        )

        request = self.context['request']
        validated_data['customer_id'] = request.user.id
        order = HatOrder(**validated_data)
        order.save()
        return order
