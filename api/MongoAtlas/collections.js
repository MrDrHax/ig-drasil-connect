db.createCollection("agent_notes", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            title: "Agent Notes",
            required: ["_id", "date", "id_agent", "notes", "created_at", "updated_at"],
            properties: {
                _id: { bsonType: "objectId" },
                date: { bsonType: "date" },
                id_agent: { bsonType: "string" },
                notes: {
                    bsonType: "array",
                    items: {
                        bsonType: "object",
                        required: ["message", "timestamp"],
                        properties: {
                            message: { bsonType: "string" },
                            timestamp: { bsonType: "date" }
                        }
                    }
                },
                created_at: { bsonType: "date" },
                updated_at: { bsonType: "date" }
            }
        }
    }
});


db.createCollection("supervisor_agent", {
    validator: {
      $jsonSchema: {
        bsonType: "object",
        title: "Supervisor and Agent conversations",
        required: ["_id", "id_agent", "id_supervisor", "created_at", "updated_at", "messages"],
        properties: {
          _id: { bsonType: "objectId" },
          id_agent: { bsonType: "string" },
          id_supervisor: { bsonType: "string" },
          created_at: { bsonType: "date" },
          updated_at: { bsonType: "date" },
          messages: {
            bsonType: "array",
            items: {
              bsonType: "object",
              required: ["sender", "timestamp", "content"],
              properties: {
                sender: { enum: ["supervisor", "agent"] },
                timestamp: { bsonType: "date" },
                content: { bsonType: "string" }
              }
            }
          }
        }
      }
    }
  }); 

  db.createCollection("Resume-Transcrip",{
    validator: {
      $jsonSchema: {
        bsonType: "object",
        title: "Transcrip "
      }
    }
  });