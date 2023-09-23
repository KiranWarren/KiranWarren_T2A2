from controllers.locations_controller import locations
from controllers.countries_controller import countries
from controllers.location_types_controller import location_types
from controllers.currencies_controller import currencies

register_controllers = (
    locations,
    countries,
    location_types,
    currencies,
    )