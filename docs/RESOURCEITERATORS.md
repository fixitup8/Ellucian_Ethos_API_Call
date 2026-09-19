# Using Ethos Resource Iterators

The library has features which automatically handle the standard pagination process. It does this by generating resource
iterators that can be used just like python list structures.

## Simple iterator

The following sample will list all the academic periods.

```
academic_period_iterator = ethos_client.get_resource_iterator(
  login_session=login_session,
  resource_name="academic-periods",
  version=None,
  params=None,
  page_size=25
)

cur = 0
for period in academic_period_iterator:
  cur += 1
  print(cur, "period", period.data)
```

In this example the iterator will collect periods 25 at a time, it then produces each academic period individually and
once 25 have been used up it will request the next page.

## Iterator with Parameters

There are various ways that Ethos API's accept criteria for selecting individual records.
e.g. for academic-periods this is documented [here](https://resources.elluciancloud.com/bundle/academic-periods/page/16.1.0/index.html)

The library caters for this by allowing you to send a dictionary of query paramaters which are added to the query 
requests. So for academic periods we can restrict to just listing open preiods:

```
params["criteria"] = "{\"registration\":\"open\"}"

academic_period_iterator = ethos_client.get_resource_iterator(
  login_session=login_session,
  resource_name="academic-periods",
  version=None,
  params=params,
  page_size=25
)

cur = 0
for period in academic_period_iterator:
  cur += 1
  print(cur, "period", period.data)
```

You should refer to the Ethos documentation for the valid parameters that can be set for each resrouce type.

## Iterators from Resource Wrapper Objects

The libarary will recognise particular resource types and return custom resource weapper objects. If a custom resource
wrapper object is returned it may contain functions which return iterators for other related recources.

One example of this is getting a all visas for a person:
```
person = ethos_client.get_resource(
  login_session=login_session,
  resource_name="persons",
  resource_id=person_resource_id,
  version=None
)
print("Found:", person.data["names"][0]["fullName"])

cur = 0
for cur_visa in person.get_visas(login_session=login_session):
  cur += 1
  print(cur, "visa", cur_visa.data)
```

## Samples

 - Example program that lists academic periods - [list_academic_periods.py](../samples/list_academic_periods.py)
 - Example program that lists a persons addresses - [list_person_addresses.py](../samples/list_person_addresses.py)
