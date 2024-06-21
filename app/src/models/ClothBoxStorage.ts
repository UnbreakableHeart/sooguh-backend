import Logger from "../config/logger";
import dotenv from "dotenv";
import DatabaseSingleton from "../config/db";

dotenv.config();

interface ClothBoxSchema {
    _id: string;
    address: string;
    providing_name: string;
    loaction: {
        type: string;
        coordinates: number[];
    };
}

class ClothBoxStorage {
    private static instance: ClothBoxStorage;
    private collection: any;

    private constructor(){
        const db = DatabaseSingleton.getInstance().getDb();
        const collection_name = process.env.DB_COLLECTION_CLOTH_BOX || "clothes_box";
        this.collection = db.collection<ClothBoxSchema>(collection_name);
    };

    public static getInstance(): ClothBoxStorage {
        if (!this.instance) {
            this.instance = new ClothBoxStorage();
            Logger.getInstance().info("ClothBoxStorage instance created");
        }
        return this.instance;
    };

    public async getClothBoxes(lat: number, lon: number): Promise<any> {
        Logger.getInstance().info(`Getting cloth boxes, lat: ${lat}, lon: ${lon}`);
        const distance = parseInt(process.env.SEARCH_DISTANCE || `1000`);

        try{
            this.collection.createIndex({location:"2dsphere"});
            const docs = await this.collection.find({
                location: {
                    $near: {
                        $geometry: {
                            type: "Point",
                            coordinates: [lon, lat]
                        },
                        $maxDistance: distance
                    }
                }
            }).toArray();
            Logger.getInstance().info(`Successfully got cloth boxes`);
            return { response: docs };
        } catch (err) {
            Logger.getInstance().error(`Failed to get cloth boxes: ${err}`);
            return { response: { err: err } };
        }
    };
}

export default ClothBoxStorage;