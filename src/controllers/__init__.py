from controllers.locations_controller import locations
from controllers.countries_controller import countries
from controllers.location_types_controller import location_types
from controllers.currencies_controller import currencies
from controllers.users_controller import users
from controllers.projects_controller import projects

register_controllers = (
    locations,
    countries,
    location_types,
    currencies,
    users,
    projects
    )