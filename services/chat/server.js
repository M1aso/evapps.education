const express = require('express');
const { sequelize, Chat, Message, ChatParticipant, Attachment } = require('./db');
const { v4: uuidv4 } = require('uuid');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const WebSocket = require('ws');

const PORT = process.env.PORT || 3000;
const upload = multer({ dest: path.join(__dirname, 'uploads') });

async function init() {
  await sequelize.sync();

  const app = express();
  app.use(express.json());

  app.post('/api/chats', async (req, res) => {
    const chat = await Chat.create({ title: req.body.title || 'New Chat' });
    res.status(201).json(chat);
  });

  app.get('/api/chats', async (req, res) => {
    const chats = await Chat.findAll();
    res.json(chats);
  });

  app.post('/api/chats/:chatId/participants', async (req, res) => {
    const { chatId } = req.params;
    const { userId } = req.body;
    const participant = await ChatParticipant.create({ chatId, userId });
    res.status(201).json(participant);
  });

  app.delete('/api/chats/:chatId/participants/:userId', async (req, res) => {
    const { chatId, userId } = req.params;
    await ChatParticipant.destroy({ where: { chatId, userId } });
    res.sendStatus(204);
  });

  app.get('/api/chats/:chatId/messages', async (req, res) => {
    const { chatId } = req.params;
    const limit = parseInt(req.query.limit) || 50;
    const offset = parseInt(req.query.offset) || 0;
    const messages = await Message.findAll({
      where: { chatId },
      include: Attachment,
      limit,
      offset,
      order: [['createdAt', 'ASC']],
    });
    res.json(messages);
  });

  app.post('/api/chats/:chatId/messages', upload.single('file'), async (req, res) => {
    const { chatId } = req.params;
    const { senderId, content } = req.body;
    const message = await Message.create({ chatId, senderId, content });

    if (req.file) {
      const attachment = await Attachment.create({
        messageId: message.id,
        url: '/uploads/' + req.file.filename,
        mimeType: req.file.mimetype,
        sizeBytes: req.file.size,
      });
      message.dataValues.attachments = [attachment];
    }

    broadcast(chatId, { type: 'message.new', data: message });
    res.status(201).json(message);
  });

  app.put('/api/chats/:chatId/messages/:messageId', async (req, res) => {
    const { chatId, messageId } = req.params;
    const message = await Message.findOne({ where: { id: messageId, chatId } });
    if (!message) return res.sendStatus(404);

    const maxEditTime = 15 * 60 * 1000;
    if (Date.now() - new Date(message.createdAt).getTime() > maxEditTime) {
      return res.status(400).json({ error: 'Edit window expired' });
    }

    message.content = req.body.content;
    message.editedAt = new Date();
    await message.save();

    broadcast(chatId, { type: 'message.update', data: message });
    res.json(message);
  });

  app.delete('/api/chats/:chatId/messages/:messageId', async (req, res) => {
    const { chatId, messageId } = req.params;
    const message = await Message.findOne({ where: { id: messageId, chatId } });
    if (!message) return res.sendStatus(404);
    message.deletedAt = new Date();
    await message.save();
    broadcast(chatId, { type: 'message.delete', data: { id: messageId } });
    res.sendStatus(204);
  });

  const server = app.listen(PORT, () => {
    console.log(`Chat service listening on port ${PORT}`);
  });

  setupWebSocketServer(server);
}

const chatRooms = new Map();

function broadcast(chatId, payload) {
  const clients = chatRooms.get(chatId) || [];
  for (const ws of clients) {
    if (ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(payload));
    }
  }
}

function setupWebSocketServer(server) {
  const wss = new WebSocket.Server({ noServer: true });

  server.on('upgrade', (req, socket, head) => {
    const urlParts = req.url.split('/');
    const chatIndex = urlParts.indexOf('ws');
    if (chatIndex === -1 || urlParts[chatIndex + 1] !== 'chats') {
      socket.destroy();
      return;
    }
    const chatId = urlParts[chatIndex + 2];

    wss.handleUpgrade(req, socket, head, (ws) => {
      ws.chatId = chatId;
      wss.emit('connection', ws, req);
    });
  });

  wss.on('connection', (ws) => {
    const { chatId } = ws;
    if (!chatRooms.has(chatId)) chatRooms.set(chatId, new Set());
    chatRooms.get(chatId).add(ws);

    ws.on('close', () => {
      chatRooms.get(chatId).delete(ws);
    });
  });
}

init().catch((err) => {
  console.error(err);
  process.exit(1);
});
