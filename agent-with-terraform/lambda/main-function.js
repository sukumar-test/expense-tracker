// Main Lambda Function
exports.handler = async (event) => {
  console.log('Event received:', JSON.stringify(event, null, 2));
  
  try {
    const AWS = require('aws-sdk');
    const firehose = new AWS.Firehose();
    
    // Extract data from the event (depends on your API structure)
    const body = event.body ? JSON.parse(event.body) : {};
    
    // Prepare the record for Firehose
    const record = {
      id: event.requestContext.requestId,
      timestamp: new Date().toISOString(),
      data: JSON.stringify(body),
      path: event.rawPath,
      method: event.requestContext.http.method,
      sourceIp: event.requestContext.http.sourceIp
    };
    
    // Send data to Firehose
    const firehoseParams = {
      DeliveryStreamName: process.env.FIREHOSE_DELIVERY_STREAM,
      Record: {
        Data: Buffer.from(JSON.stringify(record))
      }
    };
    
    await firehose.putRecord(firehoseParams).promise();
    
    // Return successful response
    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message: 'Data successfully processed',
        requestId: event.requestContext.requestId
      })
    };
  } catch (error) {
    console.error('Error:', error);
    
    // Return error response
    return {
      statusCode: 500,
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message: 'Error processing data',
        error: error.message
      })
    };
  }
};
