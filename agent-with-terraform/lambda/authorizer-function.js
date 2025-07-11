// Authorizer Lambda Function
exports.handler = async (event) => {
  console.log('Auth Event received:', JSON.stringify(event, null, 2));
  
  try {
    // Extract the Authorization header
    const authHeader = event.headers.authorization || event.headers.Authorization;
    
    if (!authHeader) {
      console.log('No authorization header present');
      return generatePolicy('user', 'Deny', event.routeArn);
    }
    
    // In a real-world scenario, you would validate the token against your authentication system
    // Here we're doing a simple check for demo purposes
    if (authHeader.startsWith('Bearer ')) {
      const token = authHeader.split(' ')[1];
      
      // Simple token validation (replace with actual validation logic)
      if (token && token !== 'invalid') {
        // If validation is successful, return an Allow policy
        return generatePolicy('user', 'Allow', event.routeArn);
      }
    }
    
    // If validation fails, return a Deny policy
    console.log('Invalid token');
    return generatePolicy('user', 'Deny', event.routeArn);
    
  } catch (error) {
    console.error('Error in authorizer:', error);
    return generatePolicy('user', 'Deny', event.routeArn);
  }
};

// Helper function to generate IAM policy
function generatePolicy(principalId, effect, resource) {
  const authResponse = {
    principalId: principalId,
    policyDocument: {
      Version: '2012-10-17',
      Statement: [
        {
          Action: 'execute-api:Invoke',
          Effect: effect,
          Resource: resource
        }
      ]
    },
    context: {
      // Additional context data if needed
      stringKey: 'string value',
      numberKey: 123,
      booleanKey: true
    }
  };
  
  return authResponse;
}
