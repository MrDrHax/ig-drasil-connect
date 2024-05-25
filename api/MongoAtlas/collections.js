db.createCollection("notes", {
  validator: {
      $jsonSchema: {
          bsonType: "object",
          title: "notes",
          required: ["_id", "date", "id_creator", "creator_type", "notes", "created_at", "updated_at"],
          properties: {
              _id: { bsonType: "objectId" },
              date: { bsonType: "date" },
              id_creator: { bsonType: "string" }, // ID of the agent or supervisor creating the note
              creator_type: { 
                  enum: ["agent", "supervisor"], // Type of the creator: agent or supervisor
                  description: "Type of the creator - either agent or supervisor"
              },
              notes: {
                  bsonType: "array",
                  items: {
                      bsonType: "object",
                      required: ["message", "timestamp", "created_by"],
                      properties: {
                          message: { bsonType: "string" },
                          timestamp: { bsonType: "date" },
                          created_by: {
                              bsonType: "string",
                              enum: ["agent", "supervisor"],
                              description: "Indicates if the note was created by an agent or a supervisor"
                          }
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