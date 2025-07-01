# Get started using thejobdb.com API

Browse the api with swagger-ui: https://thejobdb.com/api/schema/swagger-ui/

## Authenticate
To post jobs for https://myawesomecompanydomain.com, you need to authenticate to thejobdb by signing a challenge with your private key and cert, this way we can ensure you control the domain.
The [jobdb.py snippet](snippets/jobdb.py) can do it for you.

```python
$ pip install requests cryptography
>> from jobdb import get_session, JOBS_URL
>> s = get_session("/path/to/server-key.pem", "/path/to/server-cert.pem", "https://my-company.com")
```
Which is equivalent to:

```
$ curl https://thejobdb.com/api/login/ -s | jq .challenge -rj | openssl smime -sign -out smime.msg -signer server-cert.pem -inkey server-key.pem
```
And sending the smime.msg back to thejobdb for log-in. The challenge is only valid for a session.

## Post a job entry

```python
>> r = s.post(JOBS_URL, json={
  "locations": [
    {
      "postal_code": "75001",
      "country_code": "FR"
    },
    {
      "postal_code": "60601",
      "country_code": "US"
    }
  ],
  "expires_at": "2025-09-30",
  "company_job_id": "JOB12345",
  "title": "Software Engineer",
  "salary_min": 80000,
  "salary_max": 120000,
  "salary_currency": "USD",
  "salary_period": "Yearly",
  "years_of_experience": 3,
  "contact_email": "hr@myawesomecompanydomain.com",
  "apply_url": "https://myawesomecompanydomain.com/careers/apply?job=JOB12345",
  "work_model": "Hybrid",
  "contract_type": "Permanent",
  "description": "We are looking for a skilled Software Engineer to join our team",
  "NAICS_code": 541511
})
```

## Bonus: delete entry
```python
>> id = r.json()["id"]
>> r = s.delete(JOBS_URL + id)
>> assert r.status_code == 204
```

## Current limitations
10 jobs per url

50 max job items per search

## Browse job board
https://thejobdb.com/boards/?company=thejobdb.com
![Alt text](doc/images/job-board-example.png?raw=true "Title")

