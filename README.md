#Authorizer example

##Cognito User pool

Se crea un user pool en cognito para administrar los usuarios
Referencia https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html

```yaml
CrediCorpUsersPool:
  Type: AWS::Cognito::UserPool
  Properties:
    UserPoolName: CrediCorpUsersPool
    UsernameAttributes:
      - email
    AutoVerifiedAttributes:
      - email

    Policies:
      PasswordPolicy:
        MinimumLength: 8
        RequireLowercase: True
        RequireNumbers: True
        RequireSymbols: True
        RequireUppercase: True
        TemporaryPasswordValidityDays: 7
```

##Cognito User pool client
Se crea una app o app client que consume el user pool
Referencia https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html

```yaml
CredicorpUserPoolClient:
  Type: AWS::Cognito::UserPoolClient
  Properties:
    ClientName: CredicorpUserPoolClient
    GenerateSecret: True
    ExplicitAuthFlows:
      - ALLOW_CUSTOM_AUTH
      - ALLOW_USER_SRP_AUTH
      - ALLOW_REFRESH_TOKEN_AUTH
    UserPoolId: !Ref CrediCorpUsersPool
    AllowedOAuthFlows:
      - client_credentials
    AllowedOAuthFlowsUserPoolClient: True
    AllowedOAuthScopes:
      - credicorp-test/read
      - credicorp-test/write
```

## Cognito resource server

Al configurar un Resource Server, puedes definir los ámbitos (scopes) que estarán asociados a ese servidor de recursos. Los ámbitos representan los permisos o acciones específicas que un usuario puede solicitar y que deben ser autorizados por el servidor de recursos. Estos ámbitos se definen mediante el objeto Scopes dentro del recurso AWS::Cognito::UserPoolResourceServer y pueden tener nombres descriptivos y descripciones adicionales.

Referencia https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolresourceserver.html

```yaml
CrediCorpResourceServer:
  Type: AWS::Cognito::UserPoolResourceServer
  Properties:
    Identifier: credicorp-test
    Name: credicorp-test
    UserPoolId: !Ref CrediCorpUsersPool
    Scopes:
      - ScopeName: read
        ScopeDescription: Read Access
      - ScopeName: write
        ScopeDescription: Write Access
```

## Asignacion del authorizer al api gateway

Se asigna el authorizer al API en la seccion de **Auth**
Referencia: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-api-apiauth.html

```yaml
Resources:
  CredicorpApi:
    Type: AWS::Serverless::Api
    Properties:
      StageName: Dev
      Cors: "'*'"
      Auth:
        DefaultAuthorizer: CognitoAuthorizer
        Authorizers:
          CognitoAuthorizer:
            UserPoolArn: !GetAtt CrediCorpUsersPool.Arn
            Identity:
              Header: Authorization
              ReauthorizeEvery: 30
            ProviderARNs:
              - !GetAtt CrediCorpUsersPool.Arn
            AuthorizationScopes:
              - credicorp-test/read
              - credicorp-test/write
```
