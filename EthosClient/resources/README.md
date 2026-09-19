# Resource wrappers

`client.get_resource(...)`, resource iterators, and change notifications all return
data wrapped in one of these classes rather than a plain dict.

- `base.py` - `BaseResourceWrapper`, the generic wrapper every resource gets. It holds
  the raw JSON in `.data` and provides `.save()`, `.delete()` and `.refresh()`.
- `persons.py` - an example of a resource-specific wrapper. `Persons` (and its
  version-specific subclasses `PersonsV6`/`PersonsV8`/`PersonsV12`) add helpers like
  `get_addresses()` and `get_visas()` that aren't part of the generic wrapper.
- `factory.py` - `get_resource_wrapper()` looks up the resource name (e.g.
  `"persons"`) and API version in `KNOWN_RESOURCES` and returns the matching wrapper
  class, falling back to `BaseResourceWrapper` when nothing more specific is
  registered.

## Adding a wrapper for a new resource type

1. Create a new module (e.g. `academic_periods.py`) with a class that subclasses
   `BaseResourceWrapper`, following the pattern in `persons.py`.
2. Give it a `register_known_resources(resource_registry)` function that registers
   your class(es) under the resource name.
3. Call that function from `factory.py`, the same way it calls
   `register_persons_known_resources`.

You only need to do this if you want resource-specific helper methods. Any resource
without a registered wrapper still works fine through `BaseResourceWrapper`.
