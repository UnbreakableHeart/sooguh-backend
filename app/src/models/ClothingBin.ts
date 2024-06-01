import Logger from "../config/logger";
import ClothingBinStorage from "./ClothingBinStorage";

class ClothingBin {
    private body: any;

    constructor(body: any) {
        this.body = body;
    }

    public async search(){
        try{
            const response = await ClothingBinStorage.getClothingBins(this.body.lat, this.body.lon);
            return response;
        }
        catch(error: any){
            Logger.getInstance().error(error.message);
            return error;
        }
    }

}

export default ClothingBin;