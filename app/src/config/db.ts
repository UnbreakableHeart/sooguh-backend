import { MongoClient, ServerApiVersion } from "mongodb";
import dotenv from "dotenv";
import Logger from "./logger";

dotenv.config();

class DatabaseSingleton {
    private static instance: DatabaseSingleton;
    private client: MongoClient;
    private uri: string = process.env.DB_URI || "mongodb://localhost:27017";
    private dbName: string = process.env.DB_NAME || "test";

    private constructor() {
        this.client = new MongoClient(this.uri, {
            serverApi: {
                version: ServerApiVersion.v1,
                strict: true,
                deprecationErrors: true,
            },
        });
    }


    public static getInstance(): DatabaseSingleton {
        if (!DatabaseSingleton.instance) {
        DatabaseSingleton.instance = new DatabaseSingleton();
        }
        return DatabaseSingleton.instance;
    }

    public async connect() {
        try {
            await this.client.connect();
            await this.ping();
            Logger.getInstance().info("Successfully connected to MongoDB.");
        } catch (error) {
            Logger.getInstance().error(`Failed to connect to MongoDB: ${error}`);
        }
    }

    public async disconnect() {
        try {
            await this.client.close();
            Logger.getInstance().info("Disconnected from MongoDB.");
        } catch (error) {
            Logger.getInstance().error(`Failed to disconnect from MongoDB: ${error}`);
        }
    }

    public getDb() {
        return this.client.db(this.dbName);
    }

    private async ping() {
        try {
            await this.client.db("admin").command({ ping: 1 });
            Logger.getInstance().info("Pinged MongoDB successfully.");
        } catch (error) {
            Logger.getInstance().error(`Failed to ping MongoDB: ${error}`);
        }
    }
}

export default DatabaseSingleton;