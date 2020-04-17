from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from .models import Composite


class SimpleCompositeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Composite
        fields = ('pk', 'name', 'is_dir', 'zip_depth', 'parent')
    
    def validate(self, attrs):
        parent = attrs['parent']
        name = attrs['name']
        is_dir = attrs['is_dir']

        if (self.instance and parent) and (parent.pk == self.instance.pk):
            raise serializers.ValidationError('I am the parent directory.')
        same_names = Composite.objects.filter(parent=parent, name=name)
        if self.instance:
            same_names = same_names.exclude(pk=self.instance.pk)
        if same_names.exists():
            raise serializers.ValidationError('File directory with same name already exists.')
        if 'src' in attrs:
            src = attrs['src']
            if is_dir and src:
                raise serializers.ValidationError('When it is a directory, do not attach a file.')
        if not is_dir and not src:
            raise serializers.ValidationError('If it is a file, please attach the file.')
        else:
            if not self.instance:
                if not is_dir:
                    raise serializers.ValidationError('If it is a file, please attach the file.')
            else:
                src = self.instance.src
                if not is_dir and not src:
                    raise serializers.ValidationError('If it is a file, please attach the file.')
        return attrs

class SimpleCompositeRelation(serializers.RelatedField):

    default_error_messages = {
        'does_not_exist':_('invalid pk "{pk_value}" - object does not exist.'),
        'incorrect_type':_('incorrect type. Expected pk value, received {data_type}.'),
    }

    def to_representation(self, value):
        return SimpleCompositeSerializer(value).data
    
    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(pk=data)
        except ObjectDoesNotExist:
            self.fail('does_not_exist',pk_value=data)
        except (TypeError, ValueError):
            self.fail('incorrect_type', data_type=type(data).__name__)
    
    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            return {}
        
        if cutoff is not None:
            queryset = queryset[:cutoff]
        
        return dict([
            (
                item.pk,
                self.display_value(item)
            )
            for item in queryset
        ])


class CompositeSerializer(serializers.ModelSerializer):
    parent = SimpleCompositeRelation(queryset=Composite.objects.filter(is_dir=True), required=False, allow_null=True)
    composite_set = SimpleCompositeSerializer(many=True, read_only=True)

    class Meta:
        model = Composite
        fields = ('pk', 'name', 'is_dir', 'src',
                  'parent', 'zip_depth', 'composite_set')
