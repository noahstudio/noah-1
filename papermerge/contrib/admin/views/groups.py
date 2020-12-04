from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from papermerge.contrib.admin.forms import GroupForm
from papermerge.contrib.admin.views import mixins as mix


class GroupsView(
    LoginRequiredMixin,
    mix.CommonListMixin
):
    # only superuser can access this view
    only_superuser = True
    model = Group
    form_class = GroupForm
    success_url = action_url = reverse_lazy('admin:groups')
    new_object_url = reverse_lazy('admin:group-add')

    def dispatch(self, request, *args, **kwargs):

        if self.request.user.is_authenticated:
            if not self._is_allowed(request):
                raise PermissionDenied()

        ret = super().dispatch(request, *args, **kwargs)

        return ret

    def _is_allowed(self, request):
        if hasattr(self, 'only_superuser'):
            if getattr(self, 'only_superuser'):
                return request.user.is_superuser

        return True


class GroupsListView(
    GroupsView,
    mix.PaginationMixin,
    mix.DeleteEntriesMixin,
    generic.ListView
):
    title = _("Groups")
    table_header_row = [
        _('Name'),
    ]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_header_row'] = self.table_header_row
        return context


class GroupCreateView(GroupsView, generic.CreateView):

    title = _("New")
    action_url = reverse_lazy('admin:group-add')
    template_name = "admin/object_form.html"

class GroupUpdateView(GroupsView, generic.UpdateView):

    title = _("Edit")
    template_name = "admin/object_form.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['action_url'] = reverse_lazy(
            'admin:group-update',
            args=(self.object.pk,)
        )

        return context
