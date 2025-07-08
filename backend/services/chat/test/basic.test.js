const db = require('../db');
if (!db.Chat) {
  throw new Error('Chat model not exported');
}
console.log('ok');
