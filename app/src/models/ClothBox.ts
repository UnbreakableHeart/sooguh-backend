import Logger from "../config/logger";
import ClothBoxStorage from "./ClothBoxStorage";

class ClothBox {
    private body: any;

    constructor(body: any) {
        this.body = body;
    }

    public async search(){
        try{
            const response = await ClothBoxStorage.getClothBoxs(this.body.lat, this.body.lon);
            return response;
        }
        catch(error: any){
            Logger.getInstance().error(error.message);
            return error;
        }
    }

}

export default ClothBox;