# AWS style rules — apply to both genres

Drawn from the AWS style conventions enforced by AWS blog and APN reviewers,
and from corrections made on real posts. `scripts/check_blog.py` enforces the
mechanical ones; the judgment ones are here for the author.

## Service names

Full official name on first mention, short form in parentheses, short form
thereafter. Services whose official name is already an abbreviation are used
as-is and never expanded.

| Write on first mention | Then |
|---|---|
| Amazon Simple Storage Service (Amazon S3) | Amazon S3 |
| Amazon Elastic Container Service (Amazon ECS) | Amazon ECS |
| Amazon Elastic Kubernetes Service (Amazon EKS) | Amazon EKS |
| Amazon Relational Database Service (Amazon RDS) | Amazon RDS |
| Amazon Simple Queue Service (Amazon SQS) | Amazon SQS |
| Amazon Simple Notification Service (Amazon SNS) | Amazon SNS |
| Amazon Elastic Compute Cloud (Amazon EC2) | Amazon EC2 |
| Amazon Virtual Private Cloud (Amazon VPC) | Amazon VPC |
| AWS Identity and Access Management (IAM) | IAM |
| AWS Key Management Service (AWS KMS) | AWS KMS |
| Amazon Bedrock, Amazon Bedrock Knowledge Bases, Amazon Bedrock Guardrails, Amazon Bedrock AgentCore | as-is |
| Amazon OpenSearch Serverless, Amazon DynamoDB, AWS Lambda, AWS Step Functions, Amazon EventBridge, Amazon CloudWatch, Amazon Cognito, Amazon API Gateway, Amazon CloudFront, Amazon SageMaker | as-is |
| Elastic Load Balancing / Application Load Balancer | as-is |

Capitalise product features exactly as AWS does: "Knowledge Bases", not
"knowledge bases", when naming the feature; lowercase when describing an
instance ("an Amazon Bedrock knowledge base is queried").

Third-party and open source: "Strands Agents, an open source agent SDK from
AWS" on first mention. Model names as the provider writes them:
"OpenAI's gpt-oss-120b", "Cohere Embed v3 Multilingual", "Anthropic's Claude".

## Acronyms

Expand on first use, acronym in parentheses, acronym thereafter. Includes the
ones everyone knows: ETL, CORS, SSE, kNN, OTP, CVE, CSV, RAG, SDK, API is
exempt.

## Numbers

- Thousands separators: 1,234,567
- Percentages to two decimals if the source has them: 0.45%
- Every figure carries its window: "between 31 December 2025 and 21 September 2026"
- Improvements as trends with both endpoints: "fell from 0.90% to 0.45%"
- Ranges with an en dash: 15,000–16,000
- Dates: 21 September 2026 (day month year, no ordinal)

## Vocabulary

**Banned everywhere:** leading, best-in-class, world-class, seamless(ly),
revolutionary, cutting-edge, robust, game-changing, effortless, "we believe",
state-of-the-art, powerful, simply, easily.

**Banned in the partner genre, allowed in builder:** bypass, exploit, jailbreak,
attack, breach, "the platform couldn't", "X is blocked".

**Replace:** "the cloud" → "the AWS Cloud"; "platform"/"ecosystem" as vague
nouns → the specific thing.

## Structure

- Sentence-case headings
- One idea per paragraph; paragraphs ≤ 5 sentences
- Bullets for enumerations, prose for reasoning
- Tables for metrics, never for prose
- Code blocks ≤ 25 lines, with the file path as the first comment line
- One figure per major section at most; every figure captioned *Figure N: …*

## Security section

Always end with the shared-responsibility sentence, adapted:

> As with any workload on the AWS Cloud, security is a shared responsibility:
> AWS secures the underlying infrastructure, while <customer> and <partner>
> secure the operating system, applications, and data running on it.

Never name specific cipher modes (CBC, GCM) or key lengths for a regulated
customer's production systems — "the encryption scheme each core system
requires" is the right level.

## Things that must never appear

AWS account IDs, ARNs, VPC CIDRs, hostnames, IAM role names, S3 bucket names
that are not deliberately public, SSM parameter names, internal resource names
(the guardrail's resource ID, the cluster name), API keys, or any customer PII.
`check_blog.py` scans the SVG and the post for the common shapes.
