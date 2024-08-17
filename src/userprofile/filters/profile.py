from django_filters import FilterSet

from userprofile.models import UserProfile


class UserProfileFilter(FilterSet):

    class Meta:
        model = UserProfile
        fields = ()

