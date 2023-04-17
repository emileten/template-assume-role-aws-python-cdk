#!/usr/bin/env python3

from aws_cdk import Stack, App, aws_iam
from lambda_stack import LambdaStack

class TestStack(Stack):
    def __init__(self, app, construct_id, **kwargs) -> None:
        super().__init__(app, construct_id, **kwargs)
        self.construct_id = construct_id
        
        # create some role with S3 buckets permissions
        s3_access_role = aws_iam.Role(self,id="s3-access-role", role_name="s3-access-role", assumed_by=aws_iam.ServicePrincipal("lambda.amazonaws.com"), description="role to read/write buckets")
        s3_access_role.attach_inline_policy(aws_iam.Policy(self, id="Policy", statements=[aws_iam.PolicyStatement(effect=aws_iam.Effect.ALLOW, actions=["s3:Get*", "s3:List*"], resources=["arn:aws:s3:::test-emile-tenezakis"])]))
        
        # create the lambda stack
        lambda_stack = LambdaStack(app, construct_id="LambdaStack")

        # grant data access to the role used by the lambda...
        lambda_role = aws_iam.Role.from_role_name(self, "python-lambda-role", "python-lambda-role")
        s3_access_role.assume_role_policy.add_statements(
            aws_iam.PolicyStatement(
                actions=["sts:AssumeRole"],
                effect=aws_iam.Effect.ALLOW,
                principals=[aws_iam.ArnPrincipal(lambda_role.role_arn)],
            )
        )
        

app = App()
test_stack = TestStack(app, "TestStack")
app.synth()