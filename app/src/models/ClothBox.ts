import Logger from "../config/logger";
import ClothBoxStorage from "./ClothBoxStorage";

interface ClothBoxItem {
    _id: string;
    address: string;
    location: {
        coordinates: [number, number];
    };
}

class ClothBox {
    private body: any;

    constructor(body: any) {
        this.body = body;
    }

    public async search(){
        try{
            const result = await ClothBoxStorage.getInstance().getClothBoxes(this.body.coordinates.lat, this.body.coordinates.lon, this.body.distance);
            const response = result.map((item: ClothBoxItem) => ({
                _id: item._id,
                address: item.address,
                coordinates: {
                    lon: item.location.coordinates[0],
                    lat: item.location.coordinates[1]
                }
            }));
            return response
        }
        catch(error: any){
            Logger.getInstance().error(error.message);
            return error;
        }
    }

}

export default ClothBox;