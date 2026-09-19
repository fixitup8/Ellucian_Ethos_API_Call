# This file contains generators for sample responses


def get_minimum_resource_mock_result(
    guid,
    version,
    use_guid_as_id_key=False
):
    response_headers = {"x-hedtech-media-type": "application/vnd.hedtech.integration.v" + version + "+json"}
    guid_key = "guid" if use_guid_as_id_key else "id"

    response = {
        guid_key: guid,
    }
    return response, response_headers, 200


def get_person_mock_result(
    person_guid,
    version,
    first_name="Joe"
):
    response_headers = {"x-hedtech-media-type": "application/vnd.hedtech.integration.v" + version + "+json"}
    response = {
        "addresses": [],
        "credentials": [],
        "dateOfBirth": "1996-04-11",
        "emails": [],
        "gender": "male",
        "id": person_guid,
        "names": [
            {"firstName": first_name, "fullName": "Joe Blogs", "lastName": "Blogs", "preference": "preferred", "title": "Mr",
             "type": {"category": "personal"}}],
        "privacyStatus": {"privacyCategory": "unrestricted"},
        "roles": [{"role": "student", "startOn": "2020-01-01T00:00:00+00:00"}]
    }
    return response, response_headers, 200


def get_person_not_found_mock_result(
    person_guid,
    version
):
    response_headers = {"x-hedtech-media-type": "application/vnd.hedtech.integration.errors.v2+json"}
    response = {"errors": [{"code": "Global.SchemaValidation.Error", "description": "Errors parsing input JSON.", "message": "Person not found"}]}
    return response, response_headers, 404


def get_person_hold_mock_result(
    person_hold_guid,
    person_guid,
    person_hold_category_guid,
    version
):
    response_headers = {"x-hedtech-media-type": "application/vnd.hedtech.integration.v" + version + "+json"}
    response = {
        "endOn": "2099-12-31T00:00:00Z",
        "id": person_hold_guid,
        "person": {"id": person_guid},
        "startOn": "2020-01-17T00:00:00Z",
        "type": {
            "category": "academic",
            "detail": {"id": person_hold_category_guid}
        }
    }

    return response, response_headers, 200
