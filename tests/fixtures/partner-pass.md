# Example Co modernises claims intake on the AWS Cloud with Example Partner

Example Co, an insurer, worked with Example Partner to move claims document
intake to the AWS Cloud. Documents land in Amazon Simple Storage Service
(Amazon S3) and are processed by AWS Lambda. Between 1 January 2026 and
30 June 2026 the system handled 12,345 claims.

![Figure 1](figure-1.png)

*Figure 1: Example Co solution architecture — Amazon S3 events trigger AWS
Lambda, which writes results to Amazon DynamoDB.*

## Security

Access is governed by AWS Identity and Access Management (IAM) roles scoped
to each function. As with any workload on the AWS Cloud, security is a shared
responsibility: AWS secures the underlying infrastructure, while Example Co
and Example Partner secure the applications and data running on it.
