#!/usr/bin/env python3
from aws_cdk import aws_lambda, aws_iam, Stack
import aws_cdk.aws_lambda_python_alpha as aws_lambda_python

class LambdaStack(Stack):
    def __init__(self, app, construct_id, **kwargs) -> None:
        super().__init__(app, construct_id, **kwargs)
        self.construct_id = construct_id
        
        data_access_role = aws_iam.Role.from_role_name(self, id='s3-access-role', role_name='s3-access-role')
        
        def create_python_lambda(name, directory, data_access_role, **kwargs):
            aws_lambda_python.PythonFunction(
                scope=self,
                id=name,
                function_name=name,
                entry=directory,
                runtime=aws_lambda.Runtime.PYTHON_3_8,
                index="handler.py",
                handler="handler",
                environment={'DATA_ACCESS_ROLE_ARN': data_access_role.role_arn},
                **kwargs,
            )
            
        # create some role and have the lambda assume it
        lambda_role = aws_iam.Role(self, id='python-lambda-role', role_name="python-lambda-role", assumed_by=aws_iam.ServicePrincipal("lambda.amazonaws.com"))
        
        lambda_function = create_python_lambda(
            "first_request_lambda",
            "..",
            data_access_role,
            role=lambda_role
        )
        
        # inner side of the trust relationship
        data_access_role.grant_assume_role(lambda_role)
        
        