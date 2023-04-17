example CDK construct code where we grant to an imported, external role the right to assume the role we create internally (in this example the internal role is being given the right to access an S3 bucket).

### Deployment from your local machine CLI

requirements : 

- `docker` is running.
- the AWS CDK (the CLI) is installed.
- your AWS credentials are configured.

To deploy, run `cdk deploy --all --require-approval "never"`. 

