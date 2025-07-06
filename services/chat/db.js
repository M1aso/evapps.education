const { Sequelize, DataTypes } = require('sequelize');
const path = require('path');

// Use SQLite for local development; replace with PostgreSQL in production
const databaseUrl = process.env.CHAT_DATABASE_URL || 'sqlite:' + path.join(__dirname, 'chat.sqlite');

const sequelize = new Sequelize(databaseUrl, {
  logging: false,
});

const Chat = sequelize.define('Chat', {
  id: {
    type: DataTypes.UUID,
    primaryKey: true,
    defaultValue: DataTypes.UUIDV4,
  },
  title: {
    type: DataTypes.STRING,
    allowNull: false,
  },
}, {
  tableName: 'chats',
  timestamps: true,
});

const ChatParticipant = sequelize.define('ChatParticipant', {
  chatId: {
    type: DataTypes.UUID,
    references: {
      model: Chat,
      key: 'id',
    },
  },
  userId: {
    type: DataTypes.UUID,
  },
  joinedAt: {
    type: DataTypes.DATE,
    defaultValue: Sequelize.literal('CURRENT_TIMESTAMP'),
  },
}, {
  tableName: 'chat_participants',
  timestamps: false,
  indexes: [{ unique: true, fields: ['chatId', 'userId'] }],
});

const Message = sequelize.define('Message', {
  id: {
    type: DataTypes.UUID,
    primaryKey: true,
    defaultValue: DataTypes.UUIDV4,
  },
  chatId: {
    type: DataTypes.UUID,
    references: {
      model: Chat,
      key: 'id',
    },
  },
  senderId: {
    type: DataTypes.UUID,
  },
  content: DataTypes.TEXT,
  editedAt: DataTypes.DATE,
  deletedAt: DataTypes.DATE,
}, {
  tableName: 'messages',
  timestamps: true,
});

const Attachment = sequelize.define('Attachment', {
  id: {
    type: DataTypes.UUID,
    primaryKey: true,
    defaultValue: DataTypes.UUIDV4,
  },
  messageId: {
    type: DataTypes.UUID,
    references: {
      model: Message,
      key: 'id',
    },
  },
  url: {
    type: DataTypes.TEXT,
    allowNull: false,
  },
  mimeType: DataTypes.STRING,
  sizeBytes: DataTypes.BIGINT,
}, {
  tableName: 'attachments',
  timestamps: true,
});

Chat.hasMany(Message, { foreignKey: 'chatId' });
Message.belongsTo(Chat, { foreignKey: 'chatId' });

Message.hasMany(Attachment, { foreignKey: 'messageId' });
Attachment.belongsTo(Message, { foreignKey: 'messageId' });

module.exports = {
  sequelize,
  Chat,
  ChatParticipant,
  Message,
  Attachment,
};
