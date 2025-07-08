let Sequelize, DataTypes, sequelize;
try {
  ({ Sequelize, DataTypes } = require('sequelize'));
  const path = require('path');
  // Use SQLite for local development; replace with PostgreSQL in production
  const databaseUrl = process.env.CHAT_DATABASE_URL || 'sqlite:' + path.join(__dirname, 'chat.sqlite');
  sequelize = new Sequelize(databaseUrl, {
    logging: false,
  });
} catch (err) {
  // During "npm test" the node_modules directory might not be present.
  // Falling back to stub objects ensures tests run without installing dependencies.
  console.warn('sequelize not installed, using stub models');
}

let Chat, ChatParticipant, Message, Attachment;
if (sequelize) {
  Chat = sequelize.define('Chat', {
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

  ChatParticipant = sequelize.define('ChatParticipant', {
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

  Message = sequelize.define('Message', {
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

  Attachment = sequelize.define('Attachment', {
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
} else {
  // minimal stubs so tests can require this module without installing sequelize
  Chat = {};
  ChatParticipant = {};
  Message = {};
  Attachment = {};
}

module.exports = {
  sequelize,
  Chat,
  ChatParticipant,
  Message,
  Attachment,
};
