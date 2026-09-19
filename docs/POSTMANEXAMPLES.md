# Postman Collection Examples

The repo root includes
[`Ethos Integration Examples.postman_collection.json`](../Ethos%20Integration%20Examples.postman_collection.json),
Ellucian's sample Postman collection of common Ethos API calls. Every request in that
collection has a matching Python script under [`utils/`](../utils), so you can open the
collection and the script side by side. Each script's header comment names the exact
Postman folder/request it corresponds to.

Most scripts use the `EthosClient` library's high-level methods (the same ones covered
in [Quickstart](./QUICKSTART.md), [Resource Iterator Guide](./RESOURCEITERATORS.md) and
[Poller Guide](./POLLERGUIDE.md)). A few use direct calls instead (see
[Direct Call](./DIRECTCALL.md)), because the library doesn't wrap that endpoint or
because the wrapper's behavior doesn't match the example exactly - each of those notes
why in its header comment.

Before running any of these, set the `ETHOSAPIKEY` environment variable to an Ethos
application API key, and run the script from inside `utils/` (they add the repo root to
`sys.path` so they pick up the local `EthosClient` source rather than an installed copy).
Some scripts also hardcode example resource ids from Ellucian's demo tenant - those are
marked `# TODO: replace with a real id` and will need a real id from your own
environment before the call will succeed.


| [get_access_token.py](../utils/get_access_token.py) | Use API Key to get Access Token |
| [list_email_types.py](../utils/list_email_types.py) | Read all email-types resource |
| [list_courses.py]    (../utils/list_courses.py)  | Read all courses resource |
| [list_persons.py]    (../utils/list_persons.py)  | Read all persons resource |
| [update_person.py]   (../utils/update_person.py) | Update a persons resource |
| [create_person.py]   (../utils/create_person.py) | Create a persons resource |
| [publish_change_notification.py]       (../utils/publish_change_notification.py) | Publish single change-notification |
| [publish_change_notifications_batch.py](../utils/publish_change_notifications_batch.py) | Publish array of change-notifications |
| [consume_change_notifications.py]      (../utils/consume_change_notifications.py) | Retrieve change-notifications (subscriptions) |

| [get_person_by_id.py]            (../utils/get_person_by_id.py) | GET Single Persons version-less |
| [get_person_by_id_versioned.py]  (../utils/get_person_by_id_versioned.py) | GET Single Persons version-specific |
| [list_courses_filter_by_title.py](../utils/list_courses_filter_by_title.py) | Read courses filter on title |
| [list_courses_filter_by_subject.py](../utils/list_courses_filter_by_subject.py) | Read courses filter by subject |
| [list_persons_paging_page1.py]   (../utils/list_persons_paging_page1.py) | Read all persons paging 1 |
| [list_persons_paging_page2.py]   (../utils/list_persons_paging_page2.py) | Read all persons paging 2 |
| [list_persons_paging_page3.py]   (../utils/list_persons_paging_page3.py) | Read all persons paging 3 |
| [list_persons_filter_by_credential.py](../utils/list_persons_filter_by_credential.py) | Read persons filter on credential |
| [list_institution_jobs_filter_by_person.py](../utils/list_institution_jobs_filter_by_person.py) | GET institution-jobs filter for person |
| [list_sections_filter_by_period_and_course.py](../utils/list_sections_filter_by_period_and_course.py) | GET sections filter for academic-period and course |
| [list_persons_filter_by_person_filter.py](../utils/list_persons_filter_by_person_filter.py) | Read persons filter on person-filters |
| [list_persons_filter_by_role.py](../utils/list_persons_filter_by_role.py) | Read persons filter on role |
