// Consumer Lambda Function
exports.handler = async (event) => {
  console.log('Consumer Event received:', JSON.stringify(event, null, 2));
  
  try {
    const AWS = require('aws-sdk');
    const dynamodb = new AWS.DynamoDB.DocumentClient();
    
    // Process records from Firehose
    const output = event.records.map((record) => {
      try {
        // Decode and parse the data
        const payload = Buffer.from(record.data, 'base64').toString('utf-8');
        const data = JSON.parse(payload);
        
        // Store data in DynamoDB
        const params = {
          TableName: process.env.DYNAMODB_TABLE,
          Item: {
            id: data.id || `record-${Date.now()}`,
            timestamp: data.timestamp || new Date().toISOString(),
            data: data.data,
            path: data.path,
            method: data.method,
            sourceIp: data.sourceIp
          }
        };
        
        // Put item in DynamoDB
        dynamodb.put(params).promise()
          .catch(err => console.error('Error putting item in DynamoDB:', err));
        
        // Return success for this record
        return {
          recordId: record.recordId,
          result: 'Ok',
          data: record.data // Return the original data for further processing
        };
      } catch (err) {
        console.error('Error processing record:', err);
        
        // Return failure for this record
        return {
          recordId: record.recordId,
          result: 'ProcessingFailed',
          data: record.data
        };
      }
    });
    
    console.log('Processing completed, records processed:', output.length);
    return { records: output };
    
  } catch (error) {
    console.error('Error in consumer lambda:', error);
    throw error;
  }
};
