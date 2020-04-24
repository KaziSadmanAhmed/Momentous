const AWS = require("aws-sdk");


exports.handler = async(event, context) => {
    const cognito = new AWS.CognitoIdentityServiceProvider();

    if (event.triggerSource === "PreSignUp_ExternalProvider") {
        try {
            const adminGetUserParams = {
                UserPoolId: event.userPoolId,
                Username: event.request.userAttributes.email
            };
            const user = await cognito.adminGetUser(adminGetUserParams).promise();
            const [socialProviderName, socialUserId] = event.userName.split("_");
            const adminLinkProviderForUserParams = {
                DestinationUser: {
                    ProviderAttributeValue: user.Username,
                    ProviderName: "Cognito"
                },
                SourceUser: {
                    ProviderAttributeName: "Cognito_Subject",
                    ProviderAttributeValue: socialUserId,
                    ProviderName: socialProviderName
                },
                UserPoolId: event.userPoolId
            };
            await cognito.adminLinkProviderForUser(adminLinkProviderForUserParams).promise();
        }
        catch (err) {}
    }
    return event;
}
