# SMA
stock market analysis

## DEMO
### Add new email
```
curl -X POST -H "Authorization: Bearer $(gcloud auth print-identity-token)" "https://consumer-5qu6lob4wq-no.a.run.app/email"
```
### Send emails
```
curl -X POST -H "Authorization: Bearer $(gcloud auth print-identity-token)" "https://consumer-5qu6lob4wq-no.a.run.app/emails?new_email=<NEW_EMAL>"
```
