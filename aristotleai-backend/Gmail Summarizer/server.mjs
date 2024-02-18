  import express from 'express';
  import cors from 'cors';
  import fetch from 'node-fetch';

  const app = express();

  app.use(cors({ origin: 'http://localhost:3000' }));

  app.get('/gmail-api', async (req, res) => {
    try {
      // Fetch list of messages
      const listResponse = await fetch('https://www.googleapis.com/gmail/v1/users/me/messages?maxResults=3', {
        headers: {
          Authorization: req.headers.authorization,
        },
      });

      const listData = await listResponse.json();
    
      console.log(listData);
      // Array to store individual messages
      const messages = [];

      // Fetch individual messages using IDs
      for (const { id, threadId } of listData.messages) {
        const individualMessageResponse = await fetch(`https://www.googleapis.com/gmail/v1/users/me/messages/${id}`, {
          headers: {
            Authorization: req.headers.authorization,
          },
        });

        const individualMessageData = await individualMessageResponse.json();
        
        // Add individual message data to the array
        messages.push({
          
          individualMessageData
        });
      }

      // Respond with the array of individual messages
      res.json(messages);
    } catch (error) {
      console.error('Error fetching Gmail messages:', error);
      res.status(500).json({ error: 'Internal Server Error' });
    }
  });

  app.listen(8000, () => {
    console.log('Server is running on port 8000');
  });
