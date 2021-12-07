from loader import dp
from .is_admin import AdminFilter
from .is_moderator import ModeratorFilter
from .is_registrated import RegistratedFilter

if __name__ == "filters":
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(ModeratorFilter)
    dp.filters_factory.bind(RegistratedFilter)
